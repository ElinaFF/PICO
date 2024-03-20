import pytest as pytest

from ..TestsUtility import (
    METADATA_DATAFRAME,
    SAMPLES_ID_COLUMN,
    TARGETS_COLUMN,
    SAMPLES_ID,
    TARGETS,
    SELECTED_TARGETS_NAME,
    FILTERED_TARGETS,
    FILTERED_SAMPLES_ID,
    ALL_TARGETS_NAMES, CLASSES_DESIGN, PARTIAL_CLASSES_DESIGN, PARTIAL_CLASSES_REPARTITION,
)
from ...metabodashboard.domain.MetaData import MetaData


@pytest.fixture
def input_meta_data():
    return MetaData(METADATA_DATAFRAME.copy())


def test_givenMetadata_whenGetMetadata_thenMetadataIsCorrect(input_meta_data):
    assert input_meta_data.get_metadata().equals(METADATA_DATAFRAME)


def test_givenSampleIDColumn_whenGetSamplesID_thenSamplesIDAreCorrect(input_meta_data):
    input_meta_data.set_id_column(SAMPLES_ID_COLUMN)
    assert input_meta_data.get_samples_id() == SAMPLES_ID


def test_givenNoSampleIDColumn_whenSamplesID_thenEmptyList(input_meta_data):
    assert input_meta_data.get_samples_id() == []


def test_givenTargetColumn_whenGetTargets_thenTargetsAreCorrect(input_meta_data):
    input_meta_data.set_target_columns([TARGETS_COLUMN])
    assert input_meta_data.get_targets().to_list() == TARGETS


def test_givenNoTargetColumn_whenGetTargets_thenEmptyList(input_meta_data):
    assert input_meta_data.get_targets() == []


def test_givenTargetColumn_whenGetSelectedTargets_thenTargetsAreCorrect(
    input_meta_data,
):
    input_meta_data.set_target_columns([TARGETS_COLUMN])
    assert input_meta_data.get_selected_targets(SELECTED_TARGETS_NAME) == FILTERED_TARGETS


def test_givenAllTargets_whenGetSelectedTargets_thenTargetsAreCorrect(input_meta_data):
    input_meta_data.set_target_columns([TARGETS_COLUMN])
    assert input_meta_data.get_selected_targets(ALL_TARGETS_NAMES) == TARGETS


def test_givenSelectedTarget_whenGetSelectedTargetsANDIds_thenIdsAndTargetAreCorrect(
    input_meta_data,
):
    input_meta_data.set_target_columns([TARGETS_COLUMN])
    input_meta_data.set_id_column(SAMPLES_ID_COLUMN)

    assert input_meta_data.get_selected_targets_and_ids(SELECTED_TARGETS_NAME) == (
        tuple(FILTERED_TARGETS),
        tuple(FILTERED_SAMPLES_ID),
    )


def test_givenSelectedTarget_whenGetClassBalance_thenClassBalanceIsCorrect(
    input_meta_data,
):
    input_meta_data.set_target_columns([TARGETS_COLUMN])
    input_meta_data.set_id_column(SAMPLES_ID_COLUMN)
    assert input_meta_data.get_classes_repartition_based_on_design(PARTIAL_CLASSES_DESIGN) == \
           PARTIAL_CLASSES_REPARTITION
