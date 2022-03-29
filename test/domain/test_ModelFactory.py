import pytest
from metabodashboard.domain import ModelFactory


@pytest.fixture
def input_model_factory():
    model_factory = ModelFactory()
    return model_factory


def testSupportedModelCreation(input_model_factory):
    models = input_model_factory.create_supported_models()
    for name, metabomodel in models.items():
        print(name)
        print(metabomodel.model)
        print(metabomodel.grid_search_param)