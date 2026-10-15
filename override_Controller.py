import itertools
import types
from collections import Counter

import pandas as pd

from pico.domain import Controller
from pico.domain.MetaboExperiment import X_TRAIN_INDEX, X_TEST_INDEX
from pico.domain.Results import MAX_CARDINALITY_FOR_COOCURENCE
from pico.service import Utils


##############################
#        Informations        #
##############################

# Subclass of Controller whose learn() method only runs on a range of splits
# (e.g. splits 100 to 199 out of 10000) instead of all splits.
# Usage in automate.py : replace "from pico.domain import Controller" by
# "from override_Controller import Controller" and call controller.learn(split_start, split_end).
# The results saved afterwards only contain the selected splits.


def _produce_coocurence_matrix_any_split(self):
    """
    Same as Results.produce_coocurence_matrix, but reads the feature names from the first available split
    instead of split "0" (which does not exist when the range does not start at 0)
    """
    splits = [split for split in self.results.keys() if split.isdigit()]
    features = list(zip(*self.results[splits[0]]["feature_importances"]))[0]

    weight_matrix = pd.DataFrame(0, columns=features, index=splits)
    for split in splits:
        for feature, weight in self.results[split]['feature_importances']:
            if weight > 0:
                weight_matrix.loc[split, feature] = 1
    weight_matrix = weight_matrix.loc[:, (weight_matrix != 0).any(axis=0)]

    # Mean of importance for all features
    mean_importance = weight_matrix.mean(axis=0)
    number_of_nodes = len(mean_importance)
    cardinality = (number_of_nodes * (number_of_nodes - 1)) / 2
    if cardinality > MAX_CARDINALITY_FOR_COOCURENCE:
        return None, None, None, cardinality

    all_pairs = []
    for split in splits:
        split_features = weight_matrix.loc[split][weight_matrix.loc[split] == 1].index
        all_pairs.extend(itertools.combinations(split_features, 2))

    counter = Counter(all_pairs)
    return counter, mean_importance, len(splits), int(cardinality)


class Controller(Controller):

    def learn(self, split_start: int = 0, split_end: int = None):
        """
        Same as Controller.learn (i.e. MetaboExperiment.learn), but only on the splits in range(split_start, split_end)
        split_start : index of the first split to learn on (included)
        split_end : index of the last split (excluded), if None goes up to the last split
        """
        expe = self._metabo_experiment
        number_of_splits = expe.get_number_of_splits()
        if split_end is None:
            split_end = number_of_splits
        if not 0 <= split_start < split_end <= number_of_splits:
            raise ValueError(f"Invalid split range [{split_start}, {split_end}) for {number_of_splits} splits")
        selected_splits = range(split_start, split_end)
        self._logger.info(f"-> Learning on splits {split_start} to {split_end - 1}")

        expe._raise_if_value_for_learning_not_setted()
        cv_algorithm_constructor = expe.get_cv_algorithm_constructor()
        cv_algorithm_config = expe.get_cv_algorithm_configuration()
        expe._check_classification_design()
        expe._data_matrix.load_data()
        assert(expe._data_matrix.data is not None)
        if not expe._data_matrix.data.index.isin(expe._metadata.get_metadata()[expe._metadata.get_id_column()]).all():
            raise ValueError(f"'{expe._metadata.get_id_column()}' seen not to be as valid name of the unique id column.")
        params = []
        for _, classification_design in expe.classification_designs.items():
            self._logger.info("-> Classification design loop ")
            selected_targets_name = classification_design.get_selected_targets_name()
            (selected_targets, selected_ids,) = expe._metadata.get_selected_targets_and_ids(selected_targets_name)
            classes = Utils.load_classes_from_targets(
                classification_design.get_classes_design(), selected_targets
            )
            for split_index in selected_splits:
                split = classification_design._split_group.load_split_with_index(split_index)
                for model_name in expe._selected_models:
                    x_train = expe._data_matrix.load_samples_corresponding_to_IDs_in_splits(
                        split[X_TRAIN_INDEX]
                    )
                    x_test = expe._data_matrix.load_samples_corresponding_to_IDs_in_splits(
                        split[X_TEST_INDEX]
                    )
                    params.append(
                        (model_name, classification_design.get_name(), split_index, split, x_train, x_test,
                         cv_algorithm_constructor, cv_algorithm_config, selected_ids, classes)
                    )
        self._run_learning(params, selected_splits)
        expe._data_matrix.unload_data()

    def _run_learning(self, params: list, selected_splits: range):
        """
        Same as MetaboExperiment.run_learning, but the Results objects are restricted to the selected splits
        before computing the results aggregated over all splits
        """
        expe = self._metabo_experiment
        self._logger.info("-> run_learning function beginning")
        result_params = [expe.run_on_model(*param) for param in params]

        for result_param in result_params:
            (
                classification_design_name,
                model_name,
                best_model,
                scaled_data,
                importance_attribute,
                classes,
                y_train,
                y_train_pred,
                y_test,
                y_test_pred,
                split_index,
                X_train,
                X_test
            ) = result_param
            results = expe.classification_designs[classification_design_name].get_results()
            results[model_name].set_feature_names(X_train) # called multiple times but it's ok
            results[model_name].design_name = classification_design_name
            results[model_name].add_results_from_one_algo_on_one_split(
                best_model, scaled_data, importance_attribute,
                classes, y_train, y_train_pred, y_test, y_test_pred,
                split_index, X_train.index, X_test.index
            )

        selected_splits_names = [str(s) for s in selected_splits]
        for classification_design_name, classification_design in expe.classification_designs.items():
            results = classification_design.get_results()
            _, selected_sample_id = expe._metadata.get_selected_targets_and_ids(
                classification_design.get_selected_targets_name())
            for model_name, result in results.items():
                # Drop the splits that were not learned on, so that aggregated results only use the selected ones
                result.splits_number = selected_splits_names
                result.results = {s: result.results[s] for s in selected_splits_names}
                result.produce_coocurence_matrix = types.MethodType(_produce_coocurence_matrix_any_split, result)
                self._logger.info(f"-> Compute remaining results for {model_name} of {classification_design_name} design")
                result.compute_remaining_results_on_all_splits(selected_sample_id)
                del result.produce_coocurence_matrix  # remove the patch so the Results object stays picklable
            classification_design.set_is_done(True)
