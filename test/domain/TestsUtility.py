import random
from typing import List
from unittest.mock import Mock

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier


def _get_samples_id(size: int) -> List[str]:
    return ["patient-" + str(patient_id) for patient_id in range(size)]


def _get_random_data(size: int, number_of_columns: int):
    data = np.random.rand(size, number_of_columns)
    column = np.arange(number_of_columns)
    return pd.DataFrame(data, columns=column)


def _get_targets_and_classes(size: int, classes_design: dict):
    target_list = [target
                   for _, target_list in classes_design.items()
                   for target in target_list]
    number_of_target = len(target_list) - 1
    reversed_classes_design = {target: class_
                               for class_, target_list in classes_design.items()
                               for target in target_list}
    targets = []
    classes = []
    for index in range(size):
        target_index = random.randint(0, number_of_target)
        target = target_list[target_index]
        targets.append(target)
        classes.append(reversed_classes_design[target])

    return targets, classes


def _get_splits(number_of_splits: int, train_test_proportion: float, samples_id: list, classes: list) -> List[
    List[str]]:
    splits = []
    for split_index in range(number_of_splits):
        X_train, X_test, y_train, y_test = train_test_split(samples_id, classes, test_size=train_test_proportion,
                                                            random_state=split_index)
        splits.append([X_train, X_test, y_train, y_test])
    return splits


SIZE = 100
COLUMNS = 1000

EXPERIMENT_NAME = "sick_vs_healthy"
EXPERIMENT_FULL_NAME = "sick (sick, ill) versus healthy (healthy)"

CLASSES_DESIGN = {"sick": ["sick", "ill"], "healthy": ["healthy"]}

NUMBER_OF_SPLITS = 10
TRAIN_TEST_PROPORTION = 0.75

SAMPLES_ID = _get_samples_id(SIZE)
TARGETS, CLASSES = _get_targets_and_classes(SIZE, CLASSES_DESIGN)
DATA = _get_random_data(SIZE, COLUMNS)

SAMPLES_ID_COLUMN = "samples_id"
TARGETS_COLUMN = "target"

METADATA_DATAFRAME = pd.DataFrame({SAMPLES_ID_COLUMN: SAMPLES_ID, TARGETS_COLUMN: TARGETS})
DATAMATRIX = pd.concat([pd.DataFrame({SAMPLES_ID_COLUMN: SAMPLES_ID}), DATA], axis=1)
DATAMATRIX.set_index(SAMPLES_ID_COLUMN, inplace=True)

MOCKED_METADATA_CLASS = Mock()
MOCKED_METADATA = MOCKED_METADATA_CLASS.return_value
MOCKED_METADATA.load_metadata.return_value = METADATA_DATAFRAME
MOCKED_METADATA.load_samples_id.return_value = SAMPLES_ID
MOCKED_METADATA.load_targets.return_value = TARGETS

SPLITS = _get_splits(NUMBER_OF_SPLITS, TRAIN_TEST_PROPORTION, SAMPLES_ID, CLASSES)

SUPPORTED_MODEL = {
    "DecisionTree": {
        "function": DecisionTreeClassifier,
        "ParamGrid": {
            "max_depth": [1, 2, 3, 4, 5, 10],
            "min_samples_split": [2, 4, 6, 8, 10]
        }
    },
    "RandomForest": {
        "function": RandomForestClassifier,
        "ParamGrid": {
            "n_estimators": [1, 2, 4, 10, 30, 70, 100, 500, 1000]
        }
    },
    "SVM_L1": {
        "function": LinearSVC,
        "ParamGrid": {
            "C": np.logspace(-5, 5, 20)
        }
    },
}
