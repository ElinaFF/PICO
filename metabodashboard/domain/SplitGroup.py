from typing import List, Dict, Tuple

from sklearn.model_selection import train_test_split

from . import MetaData
from ..service import Utils


class SplitGroup:
    def __init__(self, metadata: MetaData, train_test_proportion: float, number_of_splits: int, classes_design: dict,
                 pairing_columns: Dict[str, List[str]]):
        self._metadata = metadata
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._splits = []
        self._compute_splits(train_test_proportion, number_of_splits, pairing_columns)

        self._removed_samples = {}

    def _compute_splits(self, train_test_proportion: float, number_of_splits: int,
                        pairing_columns: Dict[str, List[str]]):
        classes = Utils.load_classes_from_targets(self._classes_design, self._metadata.get_targets())
        for split_index in range(number_of_splits):
            X_train, X_test, y_train, y_test = train_test_split(self._metadata.get_samples_id(),
                                                                classes,
                                                                test_size=train_test_proportion,
                                                                random_state=split_index)

            self._splits.append([X_train, X_test, y_train, y_test])

    def load_split_with_index(self, split_index: int) -> list:
        return self._splits[split_index]

    def get_number_of_splits(self):
        return self._number_of_split

    # def _process_pattern_combination(self, pairing_list: List[List[str]]) -> list:
    #     result = []
    #     for pattern in pairing_list[0]:
    #         for sub_pattern in pairing_list[1]:
    #             result.append(f"{pattern}*{sub_pattern}")
    #     return result

    def _filter_sample_with_pairing_group(self, pairing_columns: Dict[str, List[str]]) -> List[str]:
        pairing_group = pairing_columns["group"]
        metadata_dataframe = self._metadata.get_metadata()
        id_column = self._metadata.get_id_column()
        filtered_samples = []
        for pairing_group_item in pairing_group:
            already_selected_value = set()
            for index, row in metadata_dataframe.iterrows():
                if row[pairing_group_item] not in already_selected_value:
                    already_selected_value.add(row[pairing_group_item])
                    filtered_samples.append(row[id_column])
                else:
                    self._removed_samples[str(row[pairing_group_item])] = row[id_column]
        return filtered_samples

