from typing import Generator, Tuple, Dict, Union

from . import SplitGroup, MetaData
from .Results import *


class ExperimentalDesign:
    def __init__(self, classes_design: dict):
        self._classes_design: dict = classes_design
        self._name: str = ""
        self._compute_name()
        self._split_group: Union[SplitGroup, None] = None
        self._selected_models_name: Union[list, None] = None
        self.results: dict = {}
        self._is_done: bool = False
        self._balance_correction: int = 0

    def get_is_done(self) -> bool:
        """
        Return the attribute is_done which is trigered when the learning is done
        """
        return self._is_done

    def set_is_done(self, is_done: bool) -> None:
        self._is_done = is_done

    def get_balance_correction(self) -> int:
        return self._balance_correction

    def set_balance_correction(self, balance_correction: int) -> None:
        if balance_correction < 0:
            raise ValueError("Balance correction cannot be negative")
        self._balance_correction = balance_correction

    def set_split_parameter_and_compute_splits(self, train_test_proportion: float, number_of_splits: int,
                                               metadata: MetaData, pairing_column: str,
                                               test_split_seed: int|None=None) -> None:
        """
        Retrieve the classes repartition which is needed to create an instance of SplitGroup
        Create an instance of SplitGroup in the attribute _split_group
        (The init of SplitGroup triggers the _compute_splits function).
        If test_split_seed is provided, then only this test split seed is computed.
        """
        classes_repartition = metadata.get_classes_repartition_based_on_design(self._classes_design)
        self._split_group = SplitGroup(metadata, self.get_selected_targets_name(), train_test_proportion,
                                       number_of_splits, self._classes_design, pairing_column, self._balance_correction,
                                       classes_repartition, test_split_seed)

    def get_name(self) -> str:
        return self._name

    def get_full_name(self) -> str:
        name = []
        for key, item_list in self._classes_design.items():
            name.append(f"{key} ({', '.join(item_list)})")
        return " versus ".join(name)

    def get_classes_design(self) -> dict:
        return self._classes_design

    def set_selected_models_name(self, selected_models_name: list) -> None:
        """
        Set the attribute self._selected_models_name
        and create the attribute self.results with initialized instances of the class Results for each algorithm
        selected_models_name: list of names of models to run on data
        """
        if self._split_group is None:
            raise ValueError("Trying to set models before setting splits parameters")
        self._selected_models_name = selected_models_name
        # TODO : un genre d'emballage de classe results pour pouvoir appeler juste un nom de classe
        for n in self._selected_models_name:
            self.results[n] = Results(self._split_group.get_number_of_splits())

    def get_results(self) -> Dict[str, Results]:
        """
        Return the results dict (attribute) corresponding to this instance of Experimental Design
        """
        if self.results == {}:
            raise RuntimeError("The name of the selected models has to be set before accessing results.")
        return self.results

    def _compute_name(self) -> None:
        self._name = "_vs_".join(self._classes_design)

    def get_number_of_splits(self) -> int:
        """
        Retrieve the number of splits from SplitGroup instance
        """
        return self._split_group.get_number_of_splits()

    def all_splits(self) -> Generator[Tuple[int, list], None, None]:
        if self._split_group is None:
            raise RuntimeError(
                "Trying to access Splits before setting splits parameters"
            )
        for split_index in range(self._split_group.get_number_of_splits()):
            yield split_index, self._split_group.load_split_with_index(split_index)

    def get_selected_targets_name(self) -> list:
        """
        get the _classes_design dict in input and reverse it to have the targets as key and their corresponding labels
        as value. It is then easier to retrieve a label for a specific target
        """
        return list(Utils.reverse_dict(self._classes_design).keys())
