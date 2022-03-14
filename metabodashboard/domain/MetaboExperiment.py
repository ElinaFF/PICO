import pandas as pd

from metabodashboard.domain import SplitGroup
from metabodashboard.domain import MetaData
from metabodashboard.domain import DataMatrix
from metabodashboard.domain import ExperimentalDesign


class MetaboExperiment:
    def __init__(self):
        self.data_matrix = None
        self.metadata = None
        self.number_of_splits = None
        self.train_test_proportion = None
        self.experimental_designs = []

    def setMetadata(self, metadata: MetaData):
        self.metadata = metadata

    def setDataMatrix(self, data_matrix: DataMatrix):
        self.data_matrix = data_matrix

    def setNumberOfSplits(self, number_of_splits: int):
        self.number_of_splits = number_of_splits

    def setTrainTestProportion(self, train_test_proportion: float):
        self.train_test_proportion = train_test_proportion

    def addExperimentalDesign(self, classes_design: dict):
        if self.number_of_splits is None:
            raise RuntimeError("Number of splits must be set before adding a experimental design")
        if self.number_of_splits is None:
            raise RuntimeError("Trying to access to not-yet-set number of splits")
        self.experimental_designs.append(ExperimentalDesign(classes_design, self.number_of_splits,
                                                            self.train_test_proportion, self.metadata))
