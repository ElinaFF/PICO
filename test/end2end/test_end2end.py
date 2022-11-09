import pytest

from ...metabodashboard.domain import MetaboController
from ..TestsUtility import (
    ENCODED_DATAMATRIX_DATAFRAME,
    SAMPLES_ID_COLUMN,
    UNIQUE_TARGET_COLUMN,
    CLASSES_DESIGN,
    ALTERNATIVE_CLASSES_DESIGN,
    ENCODED_METADATA_DATAFRAME,
    SELECTED_MODELS_NAME, MULTIPLE_TARGET_COLUMN, CLASSES_DESIGN_FOR_MULTICLASS,
    ALTERNATIVE_CLASSES_DESIGN_FOR_MULTICLASS,
)


@pytest.fixture
def input_controller():
    metabo_controller = MetaboController()
    metabo_controller.set_metadata("metadata.csv", data=ENCODED_METADATA_DATAFRAME)
    metabo_controller.set_data_matrix_remove_rt(False)
    metabo_controller.set_raw_use_for_data(False)
    metabo_controller.set_data_matrix_from_path(
        "DataMatrix.csv", data=ENCODED_DATAMATRIX_DATAFRAME
    )
    return metabo_controller


def _set_splits(input_controller):
    input_controller.set_train_test_proportion(0.2)
    input_controller.set_number_of_splits(2)
    input_controller.create_splits()


def test_givenSingleTarget_whenLearning_thenNoThrow(input_controller):
    input_controller.set_id_column(SAMPLES_ID_COLUMN)
    input_controller.set_target_columns(UNIQUE_TARGET_COLUMN)
    input_controller.add_experimental_design(CLASSES_DESIGN)

    _set_splits(input_controller)

    input_controller.set_selected_models(SELECTED_MODELS_NAME)
    input_controller.set_cv_folds(2)
    input_controller.learn()


def test_givenTwoDesign_whenLearning_thenNoThrow(input_controller):
    input_controller.set_id_column(SAMPLES_ID_COLUMN)
    input_controller.set_target_columns(UNIQUE_TARGET_COLUMN)
    input_controller.add_experimental_design(CLASSES_DESIGN)
    input_controller.add_experimental_design(ALTERNATIVE_CLASSES_DESIGN)

    _set_splits(input_controller)

    input_controller.set_selected_models(SELECTED_MODELS_NAME)
    input_controller.set_cv_folds(2)
    input_controller.learn()


def test_givenTwoTargetColumn_whenLearning_thenNoThrow(input_controller):
    input_controller.set_id_column(SAMPLES_ID_COLUMN)
    input_controller.set_target_columns(MULTIPLE_TARGET_COLUMN)
    input_controller.add_experimental_design(CLASSES_DESIGN_FOR_MULTICLASS)

    _set_splits(input_controller)

    input_controller.set_selected_models(SELECTED_MODELS_NAME)
    input_controller.set_cv_folds(2)
    input_controller.learn()


def test_givenTwoTargetColumnAndTwoDesign_whenLearning_thenNoThrow(input_controller):
    input_controller.set_id_column(SAMPLES_ID_COLUMN)
    input_controller.set_target_columns(MULTIPLE_TARGET_COLUMN)
    input_controller.add_experimental_design(CLASSES_DESIGN_FOR_MULTICLASS)
    input_controller.add_experimental_design(ALTERNATIVE_CLASSES_DESIGN_FOR_MULTICLASS)

    _set_splits(input_controller)

    input_controller.set_selected_models(SELECTED_MODELS_NAME)
    input_controller.set_cv_folds(2)
    input_controller.learn()
