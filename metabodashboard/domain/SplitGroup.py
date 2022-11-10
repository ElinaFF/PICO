from typing import List, Tuple

from sklearn.model_selection import train_test_split

from . import MetaData
from ..service import Utils


class SplitGroup:
    def __init__(
        self,
        metadata: MetaData,
        selected_targets: List[str],
        train_test_proportion: float,
        number_of_splits: int,
        classes_design: dict,
        pairing_column: str,
    ):
        self._metadata = metadata
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._splits = []
        self._compute_splits(
            train_test_proportion, number_of_splits, pairing_column, selected_targets
        )

    def _compute_splits(
        self,
        train_test_proportion: float,
        number_of_splits: int,
        pairing_column: str,
        selected_targets: List[str],
    ):
        targets = self._metadata.get_targets()
        sample_ids = self._metadata.get_samples_id()
        targets, sample_ids = self.get_selected_targets_and_ids(
            selected_targets, sample_ids, targets
        )
        if pairing_column != "":
            sample_ids, targets = Utils.filter_sample_with_pairing_group(self._metadata.get_metadata(), sample_ids,
                                                                         targets, pairing_column)
        classes = Utils.load_classes_from_targets(self._classes_design, targets)
        for split_index in range(number_of_splits):
            X_train, X_test, y_train, y_test = train_test_split(
                sample_ids, classes, test_size=train_test_proportion, random_state=split_index
            )

            if pairing_column != "":
                (X_train, y_train) = self._restore_ids_and_classes_from_pairing_and_filtered_samples(
                    X_train, pairing_column, selected_targets
                )
                (X_test, y_test) = self._restore_ids_and_classes_from_pairing_and_filtered_samples(
                    X_test, pairing_column, selected_targets
                )
            self._splits.append([X_train, X_test, y_train, y_test])

    def load_split_with_index(self, split_index: int) -> list:
        return self._splits[split_index]

    def get_number_of_splits(self):
        return self._number_of_split

    def _restore_ids_and_classes_from_pairing_and_filtered_samples(self, filtered_samples: List[str],
                                                                   paired_column: str, selected_targets: List[str]) -> Tuple[List[str], List[str]]:

        metadata_dataframe = self._metadata.get_metadata()
        # Pairing column (ex: Subject) value for all kept sample after pairing and train-test split
        paired_values_for_filtered_samples = \
            metadata_dataframe.loc[metadata_dataframe[self._metadata.get_id_column()].isin(filtered_samples)][
                paired_column
            ].tolist()
        # Retrieve ids for all the samples corresponding to paired_values_for_filtered_samples
        all_ids_restored_with_pair_value = \
            metadata_dataframe[metadata_dataframe[paired_column].isin(paired_values_for_filtered_samples)][
                self._metadata.get_id_column()].tolist()

        # Remove ids where the target doesn't correspond to the classification design
        targets = self._metadata.get_targets_from_ids(all_ids_restored_with_pair_value)
        selected_restored_ids = []
        selected_restored_targets = []
        for i, target in enumerate(targets):
            if target in selected_targets:
                selected_restored_ids.append(all_ids_restored_with_pair_value[i])
                selected_restored_targets.append(target)

        selected_restored_classes = Utils.load_classes_from_targets(self._classes_design, selected_restored_targets)

        return selected_restored_ids, selected_restored_classes

    def get_selected_targets_and_ids(self, selected_targets: List[str], samples_id: List[str], targets: List[str]) -> \
            Tuple[List[str], List[str]]:
        return tuple(
            zip(
                *[(target, id) for target, id in zip(targets, samples_id) if target in selected_targets]
            )
        )
