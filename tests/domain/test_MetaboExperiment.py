from unittest.mock import patch, mock_open

import pytest as pytest
from sklearn.model_selection import RandomizedSearchCV

from ..TestsUtility import (
    TRAIN_TEST_PROPORTION,
    NUMBER_OF_SPLITS,
    CLASSES_DESIGN,
    EXPERIMENT_NAME,
    MOCKED_METADATA,
    MOCKED_METABOEXPERIMENT_DTO,
    MOCKED_DATAMATRIX,
    EXPERIMENT_DESIGNS,
    CV_TYPE,
    ENCODED_DATAMATRIX_DATAFRAME,
    ENCODED_METADATA_DATAFRAME,
    METADATA_DATAFRAME,
    DATAMATRIX_DATAFRAME,
    assert_dataframe_approximately_equal,
    EXP_RESULTS,
    SELECTED_MODELS_NAME,
    SAMPLES_ID_COLUMN,
    TARGETS_COLUMN,
    ALL_RESULTS,
)
from medic.domain import MetaboExperiment


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment


@pytest.fixture
def input_set_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    metabo_experiment.set_metadata_with_dataframe(
        "metadata.csv", data=ENCODED_METADATA_DATAFRAME
    )
    metabo_experiment.set_data_matrix_remove_rt(False)
    metabo_experiment.set_raw_use_for_data(False)
    metabo_experiment.set_data_matrix("data.csv", data=ENCODED_DATAMATRIX_DATAFRAME)

    metabo_experiment.set_id_column(SAMPLES_ID_COLUMN)
    metabo_experiment.set_target_columns([TARGETS_COLUMN])
    metabo_experiment.add_experimental_design(CLASSES_DESIGN)

    metabo_experiment.set_train_test_proportion(0.2)
    metabo_experiment.set_number_of_splits(2)
    metabo_experiment.create_splits()
    metabo_experiment.set_selected_models(SELECTED_MODELS_NAME)
    return metabo_experiment


def test_givenMetaboExperiment_whenAddExperimentalDesign_thenTheExperimentalDesignsAreCorrect(
    input_metabo_experiment,
):
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    assert list(input_metabo_experiment.get_experimental_designs().keys()) == [
        EXPERIMENT_NAME
    ]


def test_givenMetaboExperiment_whenGetSelectedCvType_thenTheCvTypeIsCorrect(
    input_metabo_experiment,
):
    input_metabo_experiment.set_cv_type("RandomizedSearchCV")
    assert input_metabo_experiment.get_selected_cv_type() == "RandomizedSearchCV"


def test_givenMetaboExperiment_whenChangeCvType_thenTheCvTypeIsCorrect(
    input_metabo_experiment,
):
    input_metabo_experiment.set_cv_type("RandomizedSearchCV")
    assert input_metabo_experiment.get_cv_algorithm_constructor() == RandomizedSearchCV


def test_givenMetaboExperiment_whenChangeCvTypeToIncorrect_thenRaiseValueError(
    input_metabo_experiment,
):
    with pytest.raises(ValueError):
        input_metabo_experiment.set_cv_type("alibaba")

# TODO : if save safe : print save not safe changed to if save safe : save safe proceed... so change this test accordingly
#def test_givenMetaboExperiment_whenFullRestore_thenMetaboExperimentIsUpdated(
#    input_metabo_experiment,
#):
#    input_metabo_experiment.full_restore(MOCKED_METABOEXPERIMENT_DTO)
#    assert input_metabo_experiment.get_metadata() == MOCKED_METADATA
#    assert input_metabo_experiment.get_data_matrix() == MOCKED_DATAMATRIX
#    assert input_metabo_experiment.get_number_of_splits() == NUMBER_OF_SPLITS
#    assert input_metabo_experiment.get_train_test_proportion() == TRAIN_TEST_PROPORTION
#    assert input_metabo_experiment.get_experimental_designs() == EXPERIMENT_DESIGNS
#    assert (
#        input_metabo_experiment.get_experimental_designs()[
#            EXPERIMENT_NAME
#        ].get_results()
#        == EXP_RESULTS
#    )
#    assert input_metabo_experiment.get_selected_cv_type() == CV_TYPE


@patch("builtins.open", new_callable=mock_open)
@patch("pickle.dump", return_value=None)
def test_givenMetaboExperiment_whenPartialRestore_thenMetaboExperimentIsUpdated(
    dump_patch, open_patch, input_metabo_experiment
):
    input_metabo_experiment.partial_restore(
        MOCKED_METABOEXPERIMENT_DTO,
        "metadata.csv",
        "data_matrix.csv",
        data=ENCODED_DATAMATRIX_DATAFRAME,
        metadata=ENCODED_METADATA_DATAFRAME,
    )
    dumped_data_matrix_dataframe = dump_patch.call_args_list[0][0][0]
    assert_dataframe_approximately_equal(
        dumped_data_matrix_dataframe, DATAMATRIX_DATAFRAME
    )
    assert input_metabo_experiment.get_metadata().get_metadata().equals(METADATA_DATAFRAME)
    assert input_metabo_experiment.get_number_of_splits() == NUMBER_OF_SPLITS
    assert input_metabo_experiment.get_train_test_proportion() == TRAIN_TEST_PROPORTION
    assert input_metabo_experiment.get_experimental_designs() == EXPERIMENT_DESIGNS
    assert (
        input_metabo_experiment.get_experimental_designs()[
            EXPERIMENT_NAME
        ].get_results()
        == EXP_RESULTS
    )
    assert input_metabo_experiment.get_selected_cv_type() == CV_TYPE


def test_givenMetaboExperiment_whenLoadResults_thenResultsAreLoaded(
    input_metabo_experiment,
):
    input_metabo_experiment.load_results(MOCKED_METABOEXPERIMENT_DTO)
    assert input_metabo_experiment.get_metadata().get_hash() is None
    assert input_metabo_experiment.get_data_matrix().get_hash() is None
    assert input_metabo_experiment.get_number_of_splits() == NUMBER_OF_SPLITS
    assert input_metabo_experiment.get_train_test_proportion() == TRAIN_TEST_PROPORTION
    assert input_metabo_experiment.get_experimental_designs() == EXPERIMENT_DESIGNS
    assert (
        input_metabo_experiment.get_experimental_designs()[
            EXPERIMENT_NAME
        ].get_results()
        == EXP_RESULTS
    )
    assert input_metabo_experiment.get_selected_cv_type() == CV_TYPE


def test_givenAllParameter_whenGettingUpdatedResults_thenTheResultsAreCorrect(
    input_set_metabo_experiment,
):
    input_set_metabo_experiment.get_experimental_designs()[EXPERIMENT_NAME].set_is_done(
        True
    )

    actual_results = input_set_metabo_experiment.get_all_updated_results()

    assert actual_results.keys() == ALL_RESULTS.keys()
    for key in actual_results.keys():
        assert actual_results[key].keys() == ALL_RESULTS[key].keys()


def test_givenUndoneExperiments_whenGettingUpdatedResults_thenNoResultsAreLoaded(
    input_set_metabo_experiment,
):
    assert input_set_metabo_experiment.get_all_updated_results() == {}
