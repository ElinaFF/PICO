from unittest.mock import mock_open, patch

import pytest as pytest

from ...metabodashboard.domain.MetaData import MetaData

from .TestsUtility import METADATA_DATAFRAME, SAMPLES_ID_COLUMN, TARGETS_COLUMN, SAMPLES_ID, TARGETS


@pytest.fixture
def input_meta_data():
    with patch('builtins.open', new_callable=mock_open()):
        return MetaData(METADATA_DATAFRAME)


@patch('pickle.load', return_value=METADATA_DATAFRAME)
@patch('builtins.open', new_callable=mock_open())
def testLoadMetadata(open_mock, pickle_mock, input_meta_data):
    assert input_meta_data.load_metadata().equals(METADATA_DATAFRAME)


@patch('pickle.load', return_value=list(METADATA_DATAFRAME.columns))
@patch('builtins.open', new_callable=mock_open())
def testLoadColumns(open_mock, pickle_mock, input_meta_data):
    assert input_meta_data.load_columns() == list(METADATA_DATAFRAME.columns)


@patch('pickle.load', side_effect=[METADATA_DATAFRAME, SAMPLES_ID])
@patch('builtins.open', new_callable=mock_open())
def testLoadSamplesId(open_mock, pickle_mock, input_meta_data):
    input_meta_data.set_id_column(SAMPLES_ID_COLUMN)
    assert input_meta_data.load_samples_id() == SAMPLES_ID


def testThrowRuntimeErrorWhenLoadSamplesIdBeforeSettingIdColumn(input_meta_data):
    with pytest.raises(RuntimeError):
        input_meta_data.load_samples_id()


@patch('pickle.load', side_effect=[METADATA_DATAFRAME, TARGETS])
@patch('builtins.open', new_callable=mock_open())
def testLoadTargets(open_mock, pickle_mock, input_meta_data):
    input_meta_data.set_target_column(TARGETS_COLUMN)
    assert input_meta_data.load_targets() == TARGETS


def testThrowRuntimeErrorWhenLoadTargetsBeforeSettingTargetsColumn(input_meta_data):
    with pytest.raises(RuntimeError):
        input_meta_data.load_targets()

