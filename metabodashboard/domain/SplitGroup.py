import os
import pickle

from sklearn.model_selection import train_test_split

from metabodashboard.domain import MetaData

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "splits"))


class SplitGroup:
    def __init__(self, metadata: MetaData, train_test_proportion: float, number_of_splits: int, classes_design: dict, experiment_name: str):
        self._metadata = metadata
        self._template_file_name = experiment_name + "_split_{}.p"
        self._number_of_split = number_of_splits
        self._computeSplits(train_test_proportion, number_of_splits, classes_design)

    def _computeSplits(self, train_test_proportion: float, number_of_splits: int, classes_design: dict):
        for split_index in range(number_of_splits):
            X_train, X_test, y_train, y_test = train_test_split(self._metadata.loadSamplesId(),
                                                                self._metadata.loadTargets(),
                                                                test_size=train_test_proportion,
                                                                random_state=split_index)

            with open(os.path.join(DUMP_PATH, self._template_file_name.format(split_index)), "w+b") as split_file:
                pickle.dump([X_train, X_test, y_train, y_test], split_file)

    def loadSplitWithIndex(self, split_index: int) -> list:
        with open(os.path.join(DUMP_PATH, self._template_file_name.format(split_index)), "rb") as split_file:
            return pickle.load(split_file)

    def getNumberOfSplits(self):
        return self._number_of_split
