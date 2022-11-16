from typing import List, Tuple

from sklearn.model_selection import train_test_split
import numpy as np

from . import MetaData
from ..service import Utils


class SplitGroup:
    def __init__(self, metadata: MetaData, selected_targets: List[str], train_test_proportion: float, number_of_splits: int,
                 classes_design: dict, pairing_column: str):
        self._metadata = metadata
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._splits = []
        self._compute_splits(train_test_proportion, number_of_splits, pairing_column, selected_targets)

    def _compute_splits(self, train_test_proportion: float, number_of_splits: int, pairing_column: str, selected_targets: List[str]):
        """
        selected_targets : the selection of classes done with the interface or the automate.py (the names of the
        selected classes/targets)
        We consider selected_targets that has targets coming from multiple column, that they are separated
        by "__" i.e. "ali__A", "med__B", etc.
        """
        # TODO : this function would be a great place to implement class balancing / balance the dataset
        print("SplitGroup.py -> _compute_splits")
        print("argument pairing_column : ", pairing_column)
        print("argument selected_targets : ", selected_targets)


        # 1 - filter out the samples with a target not included in the classification design
        # retrieve metadata dataframe
        df_filter = self._metadata.get_metadata()
        # TODO : self._metadata.get_target_column() already compute unified targets... to change here
        # extract a dataframe with only the target(s) column(s)
        df_targets = self._metadata.get_metadata().loc[:, self._metadata.get_target_column()]
        if self._metadata.get_target_column() is list: # len(self._metadata.get_target_column()) > 1: ... TODO : line for multiple targets
            # new column of unified targets name, when targets are based on several columns
            df_filter["unified_targets"] = df_targets.apply(lambda row: "__".join(row), axis=1)
        else:
            # column of target if only one
            df_filter["unified_targets"] = df_targets
        # keep only the lines for which their value in the unified_targets column is in selected_targets
        df_filter = df_filter[df_filter["unified_targets"].isin(selected_targets)]
        print("_compute_split step #1 done")

        # 2 - select only one sample per entity
        if pairing_column != "":
            # sort the dataframe by the pairing_column values
            df_entity = df_filter.sort_values(pairing_column)
            # group samples by the pairing column and keep only the first row of each group (.nth(0) is more stable
            # than .first())
            # Carefull : the groupby function change the index of the dataframe to the column it groups by
            df_entity = df_entity.groupby(pairing_column).nth(0)
        else:
            df_entity = df_filter
        print("_compute_split step #2 done")

        # 2.5 - extract ids and targets, transform targets to labels
        ids = df_entity[self._metadata.get_id_column()]
        targets = df_entity["unified_targets"]
        labels = Utils.load_classes_from_targets(self._classes_design, targets)
        print("_compute_split step #2.5 done")

        # 3- procede with the train-test division on the selected samples
        print("start _compute_split step #3")
        for split_index in range(number_of_splits):

            if pairing_column == "":
                X_train, X_test, y_train, y_test = train_test_split(ids, labels, test_size=train_test_proportion, random_state=split_index)

                # 4- retrieve the paired samples corresponding to the one in train or test set
            else:
                # define the ids column as the index of the dataframe, so it can be extracted with groupby().groups
                print("df_filter")
                print(df_filter)
                df = df_filter.set_index(self._metadata.get_id_column())
                # groups is a dictionary with 'keys' as the pairing value and 'values' as the index of the lines corresponding to the pairing
                groups = df.groupby(pairing_column).groups
                # apply the train-test division on the pairing values / the entity
                X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(df_entity.index, labels, test_size=train_test_proportion, random_state=split_index)
                # retrieve the ids corresponding the to entities in train
                X_train = np.concatenate([list(groups[i]) for i in X_train_temp])
                # retrieve targets corresponding to ids and then convert to labels
                targets = df.loc[X_train]["unified_targets"]
                y_train = Utils.load_classes_from_targets(self._classes_design, targets)

                # retrieve the ids corresponding the to entities in train
                X_test = np.concatenate([list(groups[i]) for i in X_test_temp])
                # retrieve targets corresponding to ids and then convert to labels
                targets = df.loc[X_test]["unified_targets"]
                y_test = Utils.load_classes_from_targets(self._classes_design, targets)


            print("_compute_split step #4 done")
            self._splits.append([X_train, X_test, y_train, y_test])

    def load_split_with_index(self, split_index: int) -> list:
        return self._splits[split_index]

    def get_number_of_splits(self):
        return self._number_of_split

    def filter_sample_with_pairing_group(self, pairing_column: str) -> Tuple[List[str], List[str]]:
        """
        Function only needs the name of the column used to pair samples together.
        It retrieves other informations from the attributes (object MetaData).
        Then it iterates over all the metadata dataframe to store only one sample of each entity (entity stands for a
        biological source, like an individual). Multiple samples can originate from one entity.
        """
        metadata_dataframe = self._metadata.get_metadata()
        id_column = self._metadata.get_id_column()
        target_column = self._metadata.get_target_column()
        filtered_id = []
        filtered_target = []
        already_selected_value = set()
        # TODO : might want to change the process to sorting all lines and then picking the first one
        for index, row in metadata_dataframe.iterrows():
            if row[pairing_column] not in already_selected_value:
                already_selected_value.add(row[pairing_column])
                filtered_id.append(row[id_column])
                filtered_target.append(row[target_column])
        return filtered_id, filtered_target

#TODO : function to delete
    def restore_filtered_samples_from_pairing_group(self, X_train: List[str], X_test: List[str], pairing_column: str,
                                                    classes_design: dict) -> List[List[str]]:
        """
        Function retrieve metadata informations.
        Then restore the samples for the X_train, y_train combo and then the X_test, y_test combo
        """
        metadata_dataframe = self._metadata.get_metadata()
        id_column = self._metadata.get_id_column()
        target_column = self._metadata.get_target_column()

        (restored_X_train, restored_y_train) = Utils.restore_ids_and_targets_from_pairing_groups(X_train, metadata_dataframe, id_column,
                                                                                                 pairing_column, target_column, classes_design)
        (restored_X_test, restored_y_test) = Utils.restore_ids_and_targets_from_pairing_groups(X_test, metadata_dataframe, id_column,
                                                                                               pairing_column, target_column, classes_design)
        return [restored_X_train, restored_X_test, restored_y_train, restored_y_test]

    def get_selected_targets_and_ids(self, selected_targets: List[str], samples_id: List[str],
                                     targets: List[str]) -> Tuple[Tuple[str], Tuple[str]]:
        """
        Function just filters out the target/id that are not in the selected_targets list
        """
        return tuple(zip(*[(target, id) for target, id in zip(targets, samples_id) if target in selected_targets]))
