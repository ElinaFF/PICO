from . import MetaData, MetaboModel
from . import DataMatrix
from . import ExperimentalDesign
from .ModelFactory import ModelFactory

X_TRAIN_INDEX = 0
X_TEST_INDEX = 1
y_TRAIN_INDEX = 2
y_TEST_INDEX = 3


class MetaboExperiment:
    def __init__(self):
        self._model_factory = ModelFactory()

        self._data_matrix = None
        self._metadata = None

        self._number_of_splits = None
        self._train_test_proportion = None

        self._experimental_designs = []

        self._supported_model = self._model_factory.create_supported_models()
        self._custom_models = {}
        self._selected_models = []

    def set_metadata(self, metadata: MetaData):
        self._metadata = metadata

    def set_data_matrix(self, data_matrix: DataMatrix):
        self._data_matrix = data_matrix

    def set_number_of_splits(self, number_of_splits: int):
        self._number_of_splits = number_of_splits

    def set_train_test_proportion(self, train_test_proportion: float):
        self._train_test_proportion = train_test_proportion

    def get_experimental_designs(self) -> list:
        return self._experimental_designs

    def add_experimental_design(self, classes_design: dict):
        if self._number_of_splits is None:
            raise RuntimeError("Train test proportion, number of splits and metadata need to be set before adding an "
                               "experiment: missing number of splits")
        if self._train_test_proportion is None:
            raise RuntimeError("Train test proportion, number of splits and metadata need to be set before adding an "
                               "experiment: missing train test proportion")
        if self._metadata is None:
            raise RuntimeError("Train test proportion, number of splits and metadata need to be set before adding an "
                               "experiment: missing metadata")
        self._experimental_designs.append(ExperimentalDesign(classes_design, self._number_of_splits,
                                                             self._train_test_proportion, self._metadata))

    def add_custom_model(self, model_name: str, needed_import: str, grid_search_param: dict):
        self._custom_models[model_name] = self._model_factory.create_custom_model(model_name, needed_import, grid_search_param)

    def set_selected_model(self, selected_model: list):
        self._selected_models = selected_model

    def get_model_from_name(self, model_name: str) -> MetaboModel:
        if model_name in self._supported_model.keys():
            return self._supported_model[model_name]
        elif model_name in self._custom_models.keys():
            return self._custom_models[model_name]
        else:
            raise RuntimeError("The model '"+model_name+"' has not been found neither in supported and custom lists.")

    def learn(self):
        for experimental_design in self._experimental_designs:
            number_of_splits = experimental_design.get_number_of_splits()
            result = experimental_design.get_results()
            for split_index, split in experimental_design.all_splits:
                split_index = str(split_index)
                for model_name in self._selected_models:
                    metabo_model = self.get_model_from_name(model_name)
                    best_model = metabo_model.train(number_of_splits, split[X_TRAIN_INDEX], split[y_TRAIN_INDEX])
                    y_train_pred = best_model.predict(split[X_TRAIN_INDEX])
                    y_test_pred = best_model.predict(split[X_TEST_INDEX])
                    result.add_results_from_one_algo_on_one_split(best_model, split[y_TRAIN_INDEX], y_train_pred, split[y_TEST_INDEX], y_test_pred, model_name, split_index)

