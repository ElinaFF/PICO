import pandas as pd
import pytest as pytest

from metabodashboard.domain.MetaData import MetaData

METADATA_DATAFRAME = pd.DataFrame(data={"meta1": ["11", "12"], "meta2": ["21", "22"], "meta3": ["31", "32"]})
FORMATTED_COLUMNS = [{"label": "None", "value": "None"}, {"label": "meta1", "value": "meta1"}, {"label": "meta2", "value": "meta2"},
                     {"label": "meta3", "value": "meta3"}]
TARGET_COLUMN = "meta2"
FORMATTED_TARGETS = [{"label": "21", "value": "21"},
                     {"label": "22", "value": "22"}]
FORMATTED_REVERTED_TARGETS = [FORMATTED_TARGETS[1], FORMATTED_TARGETS[0]]

ID_COLUMN = "meta1"


@pytest.fixture
def input_meta_data():
    meta_data = MetaData(METADATA_DATAFRAME)
    return meta_data


def testLoadMetadata(input_meta_data):
    assert input_meta_data.loadMetadata().equals(METADATA_DATAFRAME)


def testLoadColumns(input_meta_data):
    assert input_meta_data.loadColumns() == list(METADATA_DATAFRAME.columns)


def testGetFormattedColumns(input_meta_data):
    assert input_meta_data.getFormattedColumns() == FORMATTED_COLUMNS


def testLoadSamplesId(input_meta_data):
    input_meta_data.setIdColumn(ID_COLUMN)
    assert input_meta_data.loadSamplesId() == METADATA_DATAFRAME[ID_COLUMN].tolist()


def testThrowRuntimeErrorWhenLoadSamplesIdBeforeSettingIdColumn(input_meta_data):
    with pytest.raises(RuntimeError) as e_info:
        input_meta_data.loadSamplesId()


def testLoadTargets(input_meta_data):
    input_meta_data.setTargetColumn(TARGET_COLUMN)
    assert input_meta_data.loadTargets() == METADATA_DATAFRAME[TARGET_COLUMN].tolist()


def testThrowRuntimeErrorWhenLoadTargetsBeforeSettingTargetsColumn(input_meta_data):
    with pytest.raises(RuntimeError) as e_info:
        input_meta_data.loadTargets()


def testGetUniqueFormattedTargets(input_meta_data):
    input_meta_data.setTargetColumn(TARGET_COLUMN)
    actual_formatted_targets = input_meta_data.getFormattedUniqueTargets()
    assert actual_formatted_targets == FORMATTED_TARGETS or actual_formatted_targets == FORMATTED_REVERTED_TARGETS
