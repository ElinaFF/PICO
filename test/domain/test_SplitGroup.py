from unittest.mock import patch

import pytest
from sklearn.model_selection import train_test_split

from metabodashboard.domain import SplitGroup

from TestsUtility import MOCKED_METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME, \
    SAMPLES_ID, CLASSES


@pytest.fixture
def input_splits():
    splits = SplitGroup(MOCKED_METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN,
                        EXPERIMENT_NAME)
    return splits


def testGetSplitsWithIndex(input_splits):
    for split_index in range(NUMBER_OF_SPLITS):
        assert input_splits.load_split_with_index(split_index) == train_test_split(SAMPLES_ID,
                                                                                   CLASSES,
                                                                                   test_size=TRAIN_TEST_PROPORTION,
                                                                                   random_state=split_index)
