import os
import pickle

import pandas as pd

from metabodashboard.service import DataFormat

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, "dumps")
DUMP_DATA_MATRIX_PATH = os.path.join(DUMP_PATH, "datamatrix.p")


class DataMatrix:
    def __init__(self):
        # TODO : implémenter test format de matrice (progenesis -> ML ready)
        self.data = None

    def read_format_and_store_data(self, path: str, use_raw: bool):
        data_df = self._load_and_format_from_progenesis(path, use_raw)

        with open(DUMP_DATA_MATRIX_PATH, "w+b") as data_matrix_file:
            pickle.dump(data_df, data_matrix_file)

    def _load_and_format_from_progenesis(self, path, is_raw) -> pd.DataFrame:
        """
        load the progenesis table from a path and process it to make it more easy to manipulate
        """
        formater = DataFormat(path, is_raw)
        datatable_compoundsInfo, datatable, labels, sample_names = formater.convert()
        return datatable

    def load_data(self):  #loadDataMatrix
        with open(DUMP_DATA_MATRIX_PATH, "rb") as data_matrix_file:
            self.data = pickle.load(data_matrix_file)

    def load_samples_corresponding_to_IDs_in_splits(self, id_list: list) -> pd.DataFrame:
        """
        self.data is supposed to have samples as columns, so with select only the samples(columns) we need
        with their IDS(columns names)
        Also, the way of selecting the samples column assures the samples are in the same order as the list, which is
        it self in the same order as the target list
        :return: the reduced dataframe, transposed so the samples are lines and the matrix is ML ready
        """
        if self.data is None:
            raise RuntimeError("Need to load data from file before extracting specific samples")
        df = self.data.loc[id_list, :]
        return df

