import pytest

from pico.domain import Controller
from pico.service import Utils
from ..TestsUtility import (
    ENCODED_DATAMATRIX_DATAFRAME,
    SAMPLES_ID_COLUMN,
    TARGETS_COLUMN,
    CLASSES_DESIGN,
    ENCODED_METADATA_DATAFRAME,
    SELECTED_MODELS_NAME,
)


@pytest.fixture
def input_controller():
    return Controller()


# def test_givenDataset_whenLearning_thenNoThrow(input_controller):
#     input_controller.set_metadata("metadata.csv", data=ENCODED_METADATA_DATAFRAME)
#     input_controller.set_data_matrix_remove_rt(False)
#     input_controller.set_raw_use_for_data(False)
#     input_controller.set_data_matrix_from_path(
#         "data.csv", data=ENCODED_DATAMATRIX_DATAFRAME
#     )

#     input_controller.set_id_column(SAMPLES_ID_COLUMN)
#     input_controller.set_target_columns([TARGETS_COLUMN])
#     input_controller.add_classification_design(CLASSES_DESIGN)

#     input_controller.set_train_test_proportion(0.2)
#     input_controller.set_number_of_splits(2)
#     input_controller.create_splits()
#     input_controller.set_selected_models(SELECTED_MODELS_NAME)

#     input_controller.set_cv_folds(2)
#     input_controller.learn()


# def test_givenCustomModel_whenLearning_thenNoThrow(input_controller):
#     input_controller.set_metadata("metadata.csv", data=ENCODED_METADATA_DATAFRAME)
#     input_controller.set_data_matrix_remove_rt(False)
#     input_controller.set_raw_use_for_data(False)
#     input_controller.set_data_matrix_from_path(
#         "data.csv", data=ENCODED_DATAMATRIX_DATAFRAME
#     )

#     input_controller.set_id_column(SAMPLES_ID_COLUMN)
#     input_controller.set_target_columns([TARGETS_COLUMN])
#     input_controller.add_classification_design(CLASSES_DESIGN)

#     input_controller.set_train_test_proportion(0.2)
#     input_controller.set_number_of_splits(2)
#     input_controller.create_splits()
#     input_controller.add_custom_model("DecisionTreeClassifier", "tree", {"max_depth": [1, 5, 10]},
#                                       Utils.DEFAULT_IMPORTANCE_ATTRIBUTE)
#     input_controller.set_selected_models(["CustomDecisionTreeClassifier0"])

#     input_controller.set_cv_folds(2)
#     input_controller.learn()
