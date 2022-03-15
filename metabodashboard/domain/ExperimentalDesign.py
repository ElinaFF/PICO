from typing import Generator

from metabodashboard.domain import SplitGroup, MetaData


class ExperimentalDesign:
    def __init__(self, classes_design: dict, number_of_splits: int, train_test_proportion: float, metadata: MetaData):
        self._classes_design = classes_design
        self._name = ""
        self._computeName()

        self._split_group = SplitGroup(metadata, train_test_proportion, number_of_splits, self._classes_design,
                                       self._name)

    def _computeName(self) -> None:
        class_list = self._classes_design.keys()
        for class_name in class_list:
            self._name += class_name + "_vs_"
        self._name = self._name[:-4]

    def allSplits(self) -> Generator[list, None, None]:
        for split_index in range(self._split_group.getNumberOfSplits()):
            yield self._split_group.loadSplitWithIndex(split_index)
