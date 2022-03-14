import pandas as pd
import pytest as pytest

from metabodashboard.domain.MetaData import MetaData

METADATA_DATAFRAME = pd.DataFrame(data={"meta1": ["11", "12"], "meta2": ["21", "22"], "meta3": ["31", "32"]})
FORMATTED_COLUMNS = [{"label": "None", "value": "None"}, {"label": "meta1", "value": "meta1"}, {"label": "meta2", "value": "meta2"},
                     {"label": "meta3", "value": "meta3"}]
TESTED_COLUMN = "meta2"
FORMATTED_TARGETS = [{"label": "21", "value": "21"},
                     {"label": "22", "value": "22"}]


@pytest.fixture
def input_meta_data():
    meta_data = MetaData(METADATA_DATAFRAME)
    return meta_data


def testGetFormattedColumns(input_meta_data):
    assert input_meta_data.getFormattedColumns() == FORMATTED_COLUMNS


def testGetSpecificFormattedColumn(input_meta_data):
    input_meta_data.setTargetColumn(TESTED_COLUMN)
    assert input_meta_data.getFormattedTargets() == FORMATTED_TARGETS
