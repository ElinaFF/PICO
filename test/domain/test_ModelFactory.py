import pytest
from sklearn.svm import SVC

from ...metabodashboard.domain import ModelFactory
from ..TestsUtility import SUPPORTED_MODEL


@pytest.fixture
def input_model_factory():
    model_factory = ModelFactory()
    return model_factory


def test_givenAModelFactory_whenCreateSupportedModel_thenTheSupportedModelsAreCorrect(
    input_model_factory,
):
    models = input_model_factory.create_supported_models()
    supported_model_names = list(SUPPORTED_MODEL.keys())
    for index, (name, metabomodel) in enumerate(models.items()):
        assert name == supported_model_names[index]
        assert metabomodel.model == SUPPORTED_MODEL[name]["function"]
        for key, value in SUPPORTED_MODEL[name]["ParamGrid"].items():
            assert key in metabomodel.grid_search_param
            for param in value:
                assert param in metabomodel.grid_search_param[key]


def test_givenAModelFactory_whenCreateCustomModel_thenTheCustomModelIsCorrect_2(
    input_model_factory,
):
    model_name = "SVC"
    needed_imports = "svm"
    model_param_grid = ["test_value_1", "test_value_2"]
    value_to_test = [
        ["test_value_11", "test_value_12"],
        ["test_value_21", "test_value_22", "test_value_23"],
    ]
    real_grid_search_param = {
        "test_value_1": ["test_value_11", "test_value_12"],
        "test_value_2": ["test_value_21", "test_value_22", "test_value_23"],
    }

    custom_model = input_model_factory.create_custom_model(
        model_name, needed_imports, real_grid_search_param, "feature_importances_"
    )

    assert custom_model.model == SVC
    assert custom_model.grid_search_param == real_grid_search_param
