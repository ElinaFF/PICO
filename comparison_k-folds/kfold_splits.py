"""
Repeated stratified k-folds, stored in the same format as the splits of the pico.

Goal
----
Compare the pico's way of repeating an experiment (N independent random train/test splits)
with the standard way (R repetitions of a k-fold cross-validation, i.e. R x k splits).
Example : 400 repetitions x 5 folds = 2000 splits, comparable with 2000 pico splits
(both have 20% of the samples in the test set).

How it plugs into the pico
--------------------------
The pico only reads the splits through the SplitGroup object of each classification design,
where each split is a list :
    [X_train, X_test, y_train, y_test]                         (no pairing)
    [X_train, X_test, y_train, y_test, train_folds_groups]     (with pairing)
This module computes the k-fold splits in this exact format and puts them in a regular SplitGroup.
Everything after that (models, hyperparameters search, results, saving) is the unchanged pico pipeline.
The saved .mtxp file only contains pico classes, so it can be opened like any other pico file.

Numbering of the splits
-----------------------
split_index = repetition * number_of_folds + fold
e.g. with 5 folds : splits 0-4 are the 5 folds of repetition 0, splits 5-9 those of repetition 1, etc.
Like the pico splits, split number i uses the seed i for the model and its hyperparameters search
(see MetaboExperiment.run_on_model).

Pairing
-------
When a pairing column is set, all samples sharing the same pairing value (e.g. same subject) are kept
in the same fold, using StratifiedGroupKFold, as done by the pico for the folds of the hyperparameters
search (see MetaboModel.train).
"""
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold

from pico.domain import SplitGroup, MetaData
from pico.domain.ClassificationDesign import ClassificationDesign
from pico.service import Utils, init_logger

logger = init_logger()


##############################
#   Split numbering helpers  #
##############################

def get_split_index(repetition: int, fold: int, number_of_folds: int) -> int:
    """
    Return the split number (as used by the pico) of a given fold of a given repetition.
    """
    return repetition * number_of_folds + fold


def get_repetition_and_fold(split_index: int, number_of_folds: int) -> Tuple[int, int]:
    """
    Inverse of get_split_index : return (repetition, fold) of a split number.
    Useful when analysing the results, e.g. to average the 5 folds of each repetition.
    """
    return split_index // number_of_folds, split_index % number_of_folds


##############################
#      Samples selection     #
##############################

def select_design_samples(metadata: MetaData, selected_targets: List[str],
                          uniq_sample_id: List[str]) -> pd.DataFrame:
    """
    Return the metadata lines of the samples used by a classification design.
    Same filters as step 1 of SplitGroup._compute_splits, a sample is kept only if BOTH conditions are true :
        - it has one of the selected targets
        - it is present in the data matrix
    So the samples of the data matrix outside the design are excluded by the first condition,
    and the samples of the metadata absent from the data matrix are excluded by the second one.
    """
    metadata_df = metadata.get_metadata()
    has_selected_target = metadata_df[metadata.get_target_column()].isin(selected_targets)
    is_in_data_matrix = metadata_df[metadata.get_id_column()].isin(uniq_sample_id)
    return metadata_df[has_selected_target & is_in_data_matrix]


##############################
#      Folds computation     #
##############################

def make_fold_splitter(number_of_folds: int, seed: int, is_paired: bool):
    """
    Return the sklearn object dividing the samples in folds for one repetition.
    The seed changes at each repetition, so each repetition gives different folds.
    """
    if is_paired:
        # Same splitter as the one used by the pico for the hyperparameters search with pairing
        return StratifiedGroupKFold(n_splits=number_of_folds, shuffle=True, random_state=seed)
    return StratifiedKFold(n_splits=number_of_folds, shuffle=True, random_state=seed)


def compute_folds_of_one_repetition(labels: List[str], groups: Union[List[str], None],
                                    number_of_folds: int, repetition: int) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Divide the samples in folds, for one repetition.
    Return a list of (train_positions, test_positions), one per fold.
    The positions refer to the order of the samples in 'labels' (and 'groups').
    Each sample is in the test set of exactly one fold.

    sklearn only uses X to count the samples, so the positions 0..n-1 are given as X.
    splitter.split() returns a generator (it produces the folds one by one and can be
    looped over only once), so it is converted to a list to get all the folds at once.
    """
    splitter = make_fold_splitter(number_of_folds, seed=repetition, is_paired=groups is not None)
    positions = np.arange(len(labels))
    return list(splitter.split(positions, labels, groups))


def build_one_split(ids: List[str], labels: List[str], groups: Union[List[str], None],
                    train_positions: np.ndarray, test_positions: np.ndarray, seed: int) -> list:
    """
    Build one split in the pico format :
        [X_train, X_test, y_train, y_test]                       if groups is None (no pairing)
        [X_train, X_test, y_train, y_test, train_folds_groups]   otherwise

    The samples order is shuffled, as the pico splits are, because some models
    and the folds of the hyperparameters search depend on the order of the samples.
    """
    rng = np.random.default_rng(seed=seed)
    train_positions = rng.permutation(train_positions)
    test_positions = rng.permutation(test_positions)

    X_train = [ids[i] for i in train_positions]
    X_test = [ids[i] for i in test_positions]
    y_train = [labels[i] for i in train_positions]
    y_test = [labels[i] for i in test_positions]

    if groups is None:
        return [X_train, X_test, y_train, y_test]

    train_folds_groups = [groups[i] for i in train_positions]
    return [X_train, X_test, y_train, y_test, train_folds_groups]


def compute_repeated_kfold_splits(ids: List[str], labels: List[str], groups: Union[List[str], None],
                                  number_of_repetitions: int, number_of_folds: int) -> List[list]:
    """
    Compute all the splits : number_of_repetitions x number_of_folds splits, in the pico format.

    ids : the samples ids
    labels : the label (class to predict) of each sample
    groups : the pairing value of each sample, or None if there is no pairing
    """
    splits = []
    for repetition in range(number_of_repetitions):
        folds = compute_folds_of_one_repetition(labels, groups, number_of_folds, repetition)
        for fold, (train_positions, test_positions) in enumerate(folds):
            split_index = get_split_index(repetition, fold, number_of_folds)
            split = build_one_split(ids, labels, groups, train_positions, test_positions, seed=split_index)
            splits.append(split)
    return splits


##############################
#  Integration with the pico #
##############################

def make_split_group(metadata: MetaData, classification_design: ClassificationDesign, pairing_column: str,
                     uniq_sample_id: List[str], splits: List[list]) -> SplitGroup:
    """
    Store already computed splits in a regular pico SplitGroup.

    SplitGroup computes its own splits when created, so it is created with 0 splits
    (which sets all its attributes without computing anything), and then given our splits.
    Using the pico class (and not a subclass) keeps the saved file readable without this folder.
    """
    split_group = SplitGroup(metadata, classification_design.get_selected_targets_name(),
                             train_test_proportion=0.2, number_of_splits=0,
                             classes_design=classification_design.get_classes_design(),
                             pairing_column=pairing_column, uniq_sample_id=uniq_sample_id)

    for split_index, split in enumerate(splits):
        # Same validation as the pico splits (at least 2 classes in train and in test)
        if not split_group._validate_split(split[2], split[3]):
            raise RuntimeError(f"Invalid k-fold split #{split_index}.")

    split_group._splits = splits
    split_group._number_of_split = len(splits)
    return split_group


def create_kfold_splits_for_design(controller, classification_design: ClassificationDesign,
                                   number_of_repetitions: int, number_of_folds: int) -> SplitGroup:
    """
    Compute the repeated k-folds splits of one classification design and return them as a SplitGroup.
    """
    if classification_design.get_balance_correction() > 0:
        raise NotImplementedError("Balance correction is not supported for the k-folds comparison.")

    metadata = controller._metabo_experiment.get_metadata()
    pairing_column = controller.get_pairing_group_column()
    uniq_sample_id = controller.get_samples_id()

    samples = select_design_samples(metadata, classification_design.get_selected_targets_name(), uniq_sample_id)
    ids = samples[metadata.get_id_column()].tolist()
    targets = samples[metadata.get_target_column()].tolist()
    labels = Utils.load_classes_from_targets(classification_design.get_classes_design(), targets)
    groups = samples[pairing_column].tolist() if pairing_column != "" else None

    splits = compute_repeated_kfold_splits(ids, labels, groups, number_of_repetitions, number_of_folds)
    return make_split_group(metadata, classification_design, pairing_column, uniq_sample_id, splits)


def create_repeated_kfold_splits(controller, number_of_repetitions: int, number_of_folds: int = 5) -> None:
    """
    Replacement of controller.create_splits() : create number_of_repetitions x number_of_folds splits
    for each classification design of the experiment.

    The data, metadata, classification designs and pairing column must be set on the controller before,
    exactly as before calling controller.create_splits().
    """
    logger.info(f"Creating {number_of_repetitions} repetitions x {number_of_folds}-folds splits")

    # Keep the experiment parameters coherent with the splits (test set = 1 fold)
    controller.set_number_of_splits(number_of_repetitions * number_of_folds)
    controller.set_train_test_proportion(1 / number_of_folds)

    for design_name, classification_design in controller.get_classification_designs().items():
        logger.info(f"-> k-folds splits for design {design_name}")
        classification_design._split_group = create_kfold_splits_for_design(
            controller, classification_design, number_of_repetitions, number_of_folds
        )
