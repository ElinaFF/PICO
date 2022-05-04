import pytest as pytest

from ...metabodashboard.domain.MetaData import MetaData

from .TestsUtility import METADATA_DATAFRAME, SAMPLES_ID_COLUMN, TARGETS_COLUMN, SAMPLES_ID, TARGETS


@pytest.fixture
def input_meta_data():
    meta_data = MetaData(METADATA_DATAFRAME)
    return meta_data


def testLoadMetadata(input_meta_data):
    assert input_meta_data.load_metadata().equals(METADATA_DATAFRAME)


def testLoadColumns(input_meta_data):
    assert input_meta_data.load_columns() == list(METADATA_DATAFRAME.columns)


def testLoadSamplesId(input_meta_data):
    input_meta_data.set_id_column(SAMPLES_ID_COLUMN)
    assert input_meta_data.load_samples_id() == SAMPLES_ID


def testThrowRuntimeErrorWhenLoadSamplesIdBeforeSettingIdColumn(input_meta_data):
    with pytest.raises(RuntimeError) as e_info:
        input_meta_data.load_samples_id()


def testLoadTargets(input_meta_data):
    input_meta_data.set_target_column(TARGETS_COLUMN)
    assert input_meta_data.load_targets() == TARGETS


def testThrowRuntimeErrorWhenLoadTargetsBeforeSettingTargetsColumn(input_meta_data):
    with pytest.raises(RuntimeError) as e_info:
        input_meta_data.load_targets()

