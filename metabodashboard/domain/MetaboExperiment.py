from typing import Generator, Tuple

import pandas as pd

from . import MetaData, MetaboModel
from .DataMatrix import DataMatrix
from . import ExperimentalDesign
from .ModelFactory import ModelFactory

X_TRAIN_INDEX = 0
X_TEST_INDEX = 1
y_TRAIN_INDEX = 2
y_TEST_INDEX = 3


class MetaboExperiment:
    def __init__(self):
        self._model_factory = ModelFactory()

        self._data_matrix = DataMatrix()
        self._metadata = None

        self._number_of_splits = None
        self._train_test_proportion = None

        self.experimental_designs = {}

        self._supported_model = self._model_factory.create_supported_models()
        self._custom_models = {}
        self._selected_models = []

    def set_metadata(self):
        self._metadata = MetaData()

    def set_metadata_with_dataframe(self, metadata_dataframe: pd.DataFrame):
        self._metadata = MetaData(metadata_dataframe)

    def set_data_matrix(self, path_data_matrix: str, use_raw: bool):
        self._data_matrix.read_format_and_store_data(path_data_matrix, use_raw)

    def _update_experimental_design(self):
        for _, experimental_design in self.experimental_designs.items():
            experimental_design.set_split_parameter(self._train_test_proportion, self._number_of_splits, self._metadata)

    def set_splits_parameters(self, number_of_splits: int, train_test_proportion: float):
        # TODO : ATTENTION : ajouter update experimental design dans add experimental design
        self._number_of_splits = number_of_splits
        self._train_test_proportion = train_test_proportion
        self._update_experimental_design()

    def get_experimental_designs(self) -> dict:
        return self.experimental_designs

    def add_experimental_design(self, classes_design: dict):
        experimental_design = ExperimentalDesign(classes_design)
        self.experimental_designs[experimental_design.get_name()] = experimental_design

    def remove_experimental_design(self, name: str):
        self.experimental_designs.pop(name)

    def add_custom_model(self, model_name: str, needed_import: str, grid_search_param: dict):
        self._custom_models[model_name] = self._model_factory.create_custom_model(model_name, needed_import, grid_search_param)

    def set_selected_models(self, selected_models: list):
        self._selected_models = selected_models
        for _, experimental_design in self.experimental_designs.items():
            experimental_design.set_selected_models_name(selected_models)

    def get_formatted_columns(self) -> list:
        if self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        return self._metadata.get_formatted_columns()

    def set_target_column(self, target_column: str):
        if self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        self._metadata.set_target_column(target_column)

    def set_id_column(self, id_column: str):
        if self._metadata is None:
            raise RuntimeError("Metadata is not set.")
        self._metadata.set_id_column(id_column)

    def get_formatted_unique_targets(self) -> list:
        return self._metadata.get_formatted_unique_targets()

    def get_model_from_name(self, model_name: str) -> MetaboModel:
        if model_name in self._supported_model.keys():
            return self._supported_model[model_name]
        elif model_name in self._custom_models.keys():
            return self._custom_models[model_name]
        else:
            raise RuntimeError("The model '"+model_name+"' has not been found neither in supported and custom lists.")

    def _check_experimental_design(self):
        error_message = "Train test proportion, number of splits and metadata need to be set before start learning: "
        if self._number_of_splits is None:
            raise RuntimeError(error_message + "missing number of splits")
        if self._train_test_proportion is None:
            raise RuntimeError(error_message + "missing train test proportion")
        if self._metadata is None:
            raise RuntimeError(error_message + "missing metadata")

    def all_experimental_designs_names(self) -> Generator[Tuple[str, str], None, None]:
        for name, experimental_design in self.experimental_designs.items():
            yield name, experimental_design.get_full_name()

    def learn(self, folds: int):
        self._check_experimental_design()
        self._data_matrix.load_data()
        for _, experimental_design in self.experimental_designs.items():
            results = experimental_design.get_results()
            for split_index, split in experimental_design.all_splits():
                x_train = self._data_matrix.load_samples_corresponding_to_IDs_in_splits(split[X_TRAIN_INDEX])
                x_test = self._data_matrix.load_samples_corresponding_to_IDs_in_splits(split[X_TEST_INDEX])
                for model_name in self._selected_models:
                    results[model_name].set_feature_names(x_train)
                    metabo_model = self.get_model_from_name(model_name)
                    best_model = metabo_model.train(folds, x_train, split[y_TRAIN_INDEX])
                    y_train_pred = best_model.predict(x_train)
                    y_test_pred = best_model.predict(x_test)
                    results[model_name].add_results_from_one_algo_on_one_split(best_model, x_train, split[y_TRAIN_INDEX], y_train_pred,
                                                                              split[y_TEST_INDEX], y_test_pred, model_name,
                                                                              str(split_index))
        self._data_matrix.data = None

    def get_results(self, classes_design: str, algo_name) -> dict:
        return self.experimental_designs[classes_design].get_results()[algo_name]

    def get_all_results(self) -> dict:
        results = {}
        for name in self.experimental_designs:
            results[name] = self.experimental_designs[name].get_results()
        return results


# TODO: print current algo when training
