import pytest

from ..TestsUtility import (
    MOCKED_METABOEXPERIMENT,
    MOCKED_METADATA,
    MOCKED_DATAMATRIX,
    NUMBER_OF_SPLITS,
    TRAIN_TEST_PROPORTION,
    EXPERIMENT_DESIGNS,
    CUSTOM_MODELS,
    SELECTED_MODELS_NAME,
    CV_TYPE,
)
from pico.domain.ExperimentDTO import ExperimentDTO


@pytest.fixture
def metabo_experiment_dto():
    return ExperimentDTO(MOCKED_METABOEXPERIMENT)


def test_givenMetaboXpDTO_whenGetMetaData_thenReturnMockedMetaData(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.metadata == MOCKED_METADATA


def test_givenMetaboXpDTO_whenGetDataMatrix_thenReturnMockedDataMatrix(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.data_matrix == MOCKED_DATAMATRIX


def test_givenMetaboXpDTO_whenGetNumberOfSplits_thenReturnMockedNumberOfSplits(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.number_of_splits == NUMBER_OF_SPLITS


def test_givenMetaboXpDTO_whenGetTrainTestProportion_thenReturnMockedTrainTestProportion(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.train_test_proportion == TRAIN_TEST_PROPORTION


def test_givenMetaboXpDTO_whenGetClassificationDesigns_thenReturnMockedClassificationDesigns(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.classification_designs == EXPERIMENT_DESIGNS


def test_givenMetaboXpDTO_whenGetCustomModels_thenReturnMockedCustomModels(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.custom_models == CUSTOM_MODELS


def test_givenMetaboXpDTO_whenGetSelectedModel_thenReturnMockedSelectedModel(
    metabo_experiment_dto,
):
    assert metabo_experiment_dto.selected_models == SELECTED_MODELS_NAME


def test_givenMetaboXpDTO_whenGetCvType_thenReturnMockedCvType(metabo_experiment_dto):
    assert metabo_experiment_dto.selected_cv_type == CV_TYPE
