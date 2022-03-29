import random
from typing import List
from unittest.mock import Mock

import pandas as pd


def _get_samples_id(size: int) -> List[str]:
    return ["patient-" + str(patient_id) for patient_id in range(size)]


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

SIZE = 100

EXPERIMENT_NAME = "sick_vs_healthy"

CLASSES_DESIGN = {"sick": ["sick", "ill"], "healthy": ["healthy"]}
NUMBER_OF_SPLITS = 10
TRAIN_TEST_PROPORTION = 0.75

SAMPLES_ID = _get_samples_id(SIZE)
TARGETS, CLASSES = _get_targets_and_classes(SIZE, CLASSES_DESIGN)

SAMPLES_ID_COLUMN = "samples_id"
TARGETS_COLUMN = "target"

METADATA_DATAFRAME = pd.DataFrame({SAMPLES_ID_COLUMN: SAMPLES_ID, TARGETS_COLUMN: TARGETS})

MOCKED_METADATA_CLASS = Mock()
MOCKED_METADATA = MOCKED_METADATA_CLASS.return_value
MOCKED_METADATA.load_metadata.return_value = METADATA_DATAFRAME
MOCKED_METADATA.load_samples_id.return_value = SAMPLES_ID
MOCKED_METADATA.load_targets.return_value = TARGETS
