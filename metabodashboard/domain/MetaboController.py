from typing import Generator, Tuple

import pandas as pd

from metabodashboard.domain import MetaboExperiment


class MetaboController:
    def __init__(self):
        self._metabo_experiment = MetaboExperiment()

    def set_metadata_from_path(self, path: str) -> bool:
        if path.split(".")[-1] == "csv":
            self._metabo_experiment.set_metadata(pd.read_csv(path))
            return True
        if "xls" in path.split(".")[-1] or "od" in path.split(".")[-1]:
            self._metabo_experiment.set_metadata(pd.read_excel(path))
            return True
        return False

    def get_formatted_columns(self) -> list:
        return self._metabo_experiment.get_formatted_columns()

    def set_target_column(self, target_column: str):
        self._metabo_experiment.set_target_column(target_column)

    def get_formatted_unique_targets(self) -> list:
        return self._metabo_experiment.get_formatted_unique_targets()

    def add_experimental_design(self, classes_design: dict):
        self._metabo_experiment.add_experimental_design(classes_design)

    def get_experimental_designs(self):
        return self._metabo_experiment.get_experimental_designs()

    def all_experimental_designs_names(self) -> Generator[Tuple[str, str], None, None]:
        return self._metabo_experiment.all_experimental_designs_names()

    def remove_experimental_design(self, name: str):
        self._metabo_experiment.remove_experimental_design(name)

    def set_splits_parameters(self, number_of_splits: int, train_test_split: float):
        self._metabo_experiment.set_splits_parameters(number_of_splits, train_test_split)

    def set_id_column(self, id_column: str):
        self._metabo_experiment.set_id_column(id_column)

    def set_selected_models(self, selected_models: list):
        self._metabo_experiment.set_selected_models(selected_models)

    def learn(self, folds: int):
        self._metabo_experiment.learn(folds)
