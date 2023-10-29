from typing import List, Tuple, Union

import pandas as pd
from sklearn.model_selection import train_test_split

from . import MetaData
from ..service import Utils
import numpy as np


class SplitGroup:
    def __init__(self, metadata: MetaData, selected_targets: List[str], train_test_proportion: float,
                 number_of_splits: int, classes_design: dict, pairing_column: str, balance_correction: int = 0,
                 classes_repartition: Union[dict, None] = None):
        self._metadata = metadata
        self._number_of_split = number_of_splits
        self._classes_design = classes_design
        self._splits = []
        self._compute_splits(train_test_proportion, number_of_splits, pairing_column, selected_targets,
                             balance_correction, classes_repartition)

    def _compute_splits(self, train_test_proportion: float, number_of_splits: int, pairing_column: str,
                        selected_targets: List[str], balance_correction: int = 0,
                        classes_repartition: Union[dict, None] = None):
        """
        selected_targets : the selection of classes done with the interface or the automate.py (the names of the
        selected classes/targets)
        We consider selected_targets that has targets coming from multiple column, that they are separated
        by "__" i.e. "ali__A", "med__B", etc.
        """
        # TODO : this function would be a great place to implement class balancing / balance the dataset

        # 1 - filter out the samples with a target not included in the classification design
        # retrieve metadata dataframe
        df_filter = self._metadata.get_metadata()
        # keep only the lines for which the value in the final_targets column is in selected_targets
        df_filter = df_filter[df_filter[self._metadata.get_target_column()].isin(selected_targets)]
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
        targets = df_entity[self._metadata.get_target_column()]
        labels = Utils.load_classes_from_targets(self._classes_design, targets)
        print("_compute_split step #2.5 done")

        # 3- procede with the train-test division on the selected samples
        print("start _compute_split step #3")
        for split_index in range(number_of_splits):
            if pairing_column == "":
                X_train, X_test, y_train, y_test = train_test_split(ids, labels, test_size=train_test_proportion,
                                                                    random_state=split_index)

                # 4- retrieve the paired samples corresponding to the one in train or test set
            else:
                # random shuffle initialisation for second shuffle of samples
                rng = np.random.default_rng(seed=split_index)
                # define the ids column as the index of the dataframe, so it can be extracted with groupby().groups
                df = df_filter.set_index(self._metadata.get_id_column())
                # groups is a dictionary with 'keys' as the pairing value and 'values' as the index of the lines corresponding to the pairing
                groups = df.groupby(pairing_column).groups
                # apply the train-test division on the pairing values / the entity
                X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(df_entity.index, labels,
                                                                                        test_size=train_test_proportion,
                                                                                        random_state=split_index)
                # retrieve the ids corresponding the to entities in train
                X_train = []
                for representative in X_train_temp:
                    represented_pairing_value = df_filter.loc[representative][pairing_column]
                    X_train.extend(groups[represented_pairing_value])
                # retrieve targets corresponding to ids and then convert to labels
                X_train = pd.Series(X_train)
                targets = df.loc[X_train][self._metadata.get_target_column()]
                y_train = Utils.load_classes_from_targets(self._classes_design, targets)

                training_data = list(zip(X_train, y_train))
                rng.shuffle(training_data)
                X_train, y_train = zip(*training_data)

                # retrieve the ids corresponding the to entities in test
                X_test = []
                for representative in X_test_temp:
                    represented_pairing_value = df_filter.loc[representative][pairing_column]
                    X_test.extend(groups[represented_pairing_value])
                # retrieve targets corresponding to ids and then convert to labels
                X_test = pd.Series(X_test)
                targets = df.loc[X_test][self._metadata.get_target_column()]
                y_test = Utils.load_classes_from_targets(self._classes_design, targets)

                testing_data = list(zip(X_test, y_test))
                rng.shuffle(testing_data)
                X_test, y_test = zip(*testing_data)

            if balance_correction > 0:
                X_train, y_train = Utils.remove_random_samples_from_class(X_train,
                                                                          y_train,
                                                                          balance_correction,
                                                                          classes_repartition)

            print("_compute_split step #4 done")
            self._splits.append([X_train.tolist(), X_test.tolist(), y_train, y_test])

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

    def get_selected_targets_and_ids(self, selected_targets: List[str], samples_id: List[str],
                                     targets: List[str]) -> Tuple[Tuple[str], Tuple[str]]:
        """
        Function just filters out the target/id that are not in the selected_targets list
        """
        return tuple(zip(*[(target, id) for target, id in zip(targets, samples_id) if target in selected_targets]))
