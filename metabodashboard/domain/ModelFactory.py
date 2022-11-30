import importlib
import os
from typing import List, Union

import sklearn

from .MetaboModel import MetaboModel
from ..conf.SupportedModels import LEARN_CONFIG
from ..service import Utils


# TODO: deals with methods names' that are used in Results (for example), how to retrieve features/importance/etc
class ModelFactory:
    def __init__(self):
        self._SEED = 42

    def create_supported_models(self) -> dict:
        supported_models = {}
        for model_name, model_configuration in LEARN_CONFIG.items():
            supported_models[model_name] = MetaboModel(
                model_configuration["function"], model_configuration["ParamGrid"], self._SEED,
                model_configuration["importance_attribute"]

            )
        return supported_models

    def create_custom_model(
            self,
            model_name: str,
            needed_imports: str,
            params_grid: dict,
            importance_attribute: str = Utils.DEFAULT_IMPORTANCE_ATTRIBUTE
    ) -> MetaboModel:
        imports_list = needed_imports.split(".")
        model = Utils.get_model_from_import(imports_list, model_name)
        return MetaboModel(model, params_grid, self._SEED, importance_attribute)
