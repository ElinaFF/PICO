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

    def read_format_and_store_data(self, path: str, data=None, use_raw: bool=False, from_base64: bool=True):
        data_df = self._load_and_format(path, data=data, is_raw=use_raw, from_base64=from_base64)

        with open(DUMP_DATA_MATRIX_PATH, "w+b") as data_matrix_file:
            pickle.dump(data_df, data_matrix_file)

    def _load_and_format(self, path, data=None, is_raw=False, from_base64=True) -> pd.DataFrame:
        """
        load the table from a path and process it to make it more easy to manipulate
        """
        formater = DataFormat(path, data=data, use_raw=is_raw, from_base64_str=from_base64)
        datatable_compoundsInfo, datatable, labels, sample_names = formater.convert()
        return datatable

    def load_data(self):  #loadDataMatrix
        with open(DUMP_DATA_MATRIX_PATH, "rb") as data_matrix_file:
            self.data = pickle.load(data_matrix_file)

    def load_samples_corresponding_to_IDs_in_splits(self, id_list: list) -> pd.DataFrame:
        """
        self.data is supposed to have samples as lines, so we select only the samples we need
        with their IDS(lines indexes)
        Also, the way of selecting the samples assures the samples are in the same order as the list, which is
        it self in the same order as the target list
        :return: the reduced dataframe, the samples are lines and the matrix is ML ready
        """
        if self.data is None:
            raise RuntimeError("Need to load data from file before extracting specific samples")
        df = self.data.loc[id_list, :]
        return df

