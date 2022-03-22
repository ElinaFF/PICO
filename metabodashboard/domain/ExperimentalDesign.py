from typing import Generator

from . import SplitGroup, MetaData, Results


class ExperimentalDesign:
    def __init__(self, classes_design: dict, number_of_splits: int, train_test_proportion: float, metadata: MetaData):
        self._classes_design = classes_design
        self._name = ""
        self._compute_name()

        self._split_group = SplitGroup(metadata, train_test_proportion, number_of_splits, self._classes_design,
                                       self._name)

        self._selected_models_name = None
        self._results = None

    def get_name(self):
        return self._name

    def get_classes_design(self):
        return self._classes_design

    def set_selected_models_name(self, selected_models_name: list):
        self._selected_models_name = selected_models_name
        # self._results = Results(selected_models_name, self._split_group.get_number_of_splits())
        #TODO: add result

    def get_results(self) -> Results:
        if self._results is None:
            raise RuntimeError("The name of the selected models has to be set before accessing results.")
        return self._results

    def _compute_name(self) -> None:
        class_list = self._classes_design.keys()
        for class_name in class_list:
            self._name += class_name + "_vs_"
        self._name = self._name[:-4]

    def get_number_of_splits(self) -> int:
        return self._split_group.get_number_of_splits()

    def all_splits(self) -> Generator[list, None, None]:
        for split_index in range(self._split_group.get_number_of_splits()):
            yield split_index, self._split_group.load_split_with_index(split_index)


