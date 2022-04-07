import os
import pickle

from sklearn.model_selection import train_test_split

from metabodashboard.domain import MetaData
from metabodashboard.service import Utils

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "splits"))


class SplitGroup:
    def __init__(self, metadata: MetaData, train_test_proportion: float, number_of_splits: int, classes_design: dict, experiment_name: str):
        self._metadata = metadata
        self._template_file_name = experiment_name + "_split_{}.p"
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._target_to_class = {item: key for key, item_list in classes_design.items() for item in item_list}
        self._compute_splits(train_test_proportion, number_of_splits)

    def _load_classes(self):
        targets = self._metadata.load_targets()
        print("targets _load_classes : {}".format(targets))
        reverse_classes_design = Utils.reverse_dict(self._classes_design)
        classes = []
        for target in targets:
            classes.append(reverse_classes_design[target])
        return classes

    def _compute_splits(self, train_test_proportion: float, number_of_splits: int):
        for split_index in range(number_of_splits):
            X_train, X_test, y_train, y_test = train_test_split(self._metadata.load_samples_id(),
                                                                self._load_classes(),
                                                                test_size=train_test_proportion,
                                                                random_state=split_index)

            with open(os.path.join(DUMP_PATH, self._template_file_name.format(split_index)), "w+b") as split_file:
                pickle.dump([X_train, X_test, y_train, y_test], split_file)

    def load_split_with_index(self, split_index: int) -> list:
        with open(os.path.join(DUMP_PATH, self._template_file_name.format(split_index)), "rb") as split_file:
            return pickle.load(split_file)

    def get_number_of_splits(self):
        return self._number_of_split

# TODO: C'est pas les data sur lesquelles il devrait se train ?