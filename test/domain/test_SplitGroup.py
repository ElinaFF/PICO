from unittest.mock import patch

import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

from metabodashboard.domain import SplitGroup
from metabodashboard.domain import MetaData

TARGETS = ["sick", "healthy", "healthy", "healthy", "healthy", "healthy", "sick", "sick", "healthy", "healthy"]
SAMPLES_ID = ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9", "id10"]
TRAIN_TEST_PROPORTION = 0.20
NUMBER_OF_SPLIT = 3
EXPERIMENT_NAME = "sick_vs_healthy"
ID_COLUMN_NAME = "id"
TARGETS_COLUMN_NAME = "state"
METADATA = MetaData(pd.DataFrame({ID_COLUMN_NAME: SAMPLES_ID, TARGETS_COLUMN_NAME: TARGETS}))
METADATA.setIdColumn(ID_COLUMN_NAME)
METADATA.setTargetColumn(TARGETS_COLUMN_NAME)

@pytest.fixture
def input_splits():
    splits = SplitGroup(METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLIT,
                        EXPERIMENT_NAME)
    return splits

#TODO: ne marche pas à cause des pd.Series
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
