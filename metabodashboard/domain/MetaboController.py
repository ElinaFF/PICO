from typing import Generator, Tuple

import pandas as pd

from metabodashboard.domain import MetaboExperiment
from ..service import Plots
from .Results import *


class MetaboController:
    def __init__(self):
        self._metabo_experiment = MetaboExperiment()
        self._plots = Plots("blues")

    def set_metadata(self) -> bool:

        return self._metabo_experiment.set_metadata()

    def set_metadata_dataframe_from_path(self, path: str):
        if path.split(".")[-1] == "csv":
            self._metabo_experiment.set_metadata_with_dataframe(pd.read_csv(path, sep=";"))
            return True
        if "xls" in path.split(".")[-1] or "od" in path.split(".")[-1]:
            self._metabo_experiment.set_metadata_with_dataframe(pd.read_excel(path))
            return True
        return False

    def set_data_matrix_from_path(self, path_data_matrix, use_raw):
        return self._metabo_experiment.set_data_matrix(path_data_matrix, use_raw)

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

    def show_exp_info_all(self, df: pd.DataFrame):
        return self._plots.show_exp_info_all(df)

    def produce_exp_info(self, design_name: str, algo: str):
        return self._metabo_experiment.experimental_designs[design_name].results[algo].results["info_expe"]

    def show_accuracy_all(self, df: pd.DataFrame):
        return self._plots.show_accuracy_all(df)

    def produce_accuracy_plot_all(self, design_name: str, algo: str):
        # TODO: méthode get_accuracy_plot_all(design_name: str, algo:str)
        return self._metabo_experiment.experimental_designs[design_name].results[algo].produce_accuracy_plot_all()

    def show_features_selection(self, df: pd.DataFrame):
        return self._plots.show_features_selection(df)

    def produce_features_importance_table(self, design_name: str, algo: str):
        return self._metabo_experiment.experimental_designs[design_name].results[
            algo].produce_features_importance_table()

    def show_umap(self, df: pd.DataFrame):
        return self._plots.show_umap_2D(df)

    def produce_umap(self, design_name: str, algo: str):
        return self._metabo_experiment.experimental_designs[design_name].results[
            algo].produce_features_importance_table()
