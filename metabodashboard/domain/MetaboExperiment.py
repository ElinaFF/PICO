from . import MetaData, MetaboModel
from . import DataMatrix
from . import ExperimentalDesign
from .ModelFactory import ModelFactory

from metabodashboard.domain import SplitGroup
from metabodashboard.domain import MetaData
from metabodashboard.domain import DataMatrix
from metabodashboard.domain import ExperimentalDesign


class MetaboExperiment:
    def __init__(self):
        self._model_factory = ModelFactory()

        self._data_matrix = None
        self._metadata = None

        self._number_of_splits = None
        self._train_test_proportion = None

        self._experimental_designs = []

    def setMetadata(self, metadata: MetaData):
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
