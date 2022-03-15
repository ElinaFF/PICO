from unittest.mock import patch

import pandas as pd
import pytest

from metabodashboard.domain import SplitGroup
from metabodashboard.domain import MetaData

TARGETS = ["sick", "healthy", "ill"]
SAMPLES_ID = ["11", "12", "13"]
TRAIN_TEST_PROPORTION = 0.20
NUMBER_OF_SPLIT = 3
EXPERIMENT_NAME = "sick_vs_healthy_split_group_test"
ID_COLUMN_NAME = "id"
TARGETS_COLUMN_NAME = "state"
METADATA = MetaData(pd.DataFrame({ID_COLUMN_NAME: SAMPLES_ID, TARGETS_COLUMN_NAME: TARGETS}))
METADATA.setIdColumn(ID_COLUMN_NAME)
METADATA.setTargetColumn(TARGETS_COLUMN_NAME)
CLASSES_DESIGN = {"sick": ["sick", "ill"], "healthy": ["healthy"]}


@pytest.fixture
def input_splits():
    splits = SplitGroup(METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLIT, CLASSES_DESIGN,
                        EXPERIMENT_NAME)
    return splits


@patch("metabodashboard.domain.MetaData")
def testGetSplitsWithIndex(mocker, input_splits):
    mc = mocker.return_value
    mc.loadSamplesId.return_value = SAMPLES_ID
    mc.loadTargets.return_value = TARGETS
    for split_index in range(NUMBER_OF_SPLIT):
        X_train, X_test, y_train, y_test = input_splits.loadSplitWithIndex(split_index)
        expected_X_train, expected_X_test, expected_y_train, expected_y_test = input_splits.loadSplitWithIndex(split_index)
        assert X_train == expected_X_train
        assert X_test == expected_X_test
        assert y_train == expected_y_train
        assert y_test == expected_y_test

