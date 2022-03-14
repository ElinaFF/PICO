import os
import pickle

import pandas as pd

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, "dump")
DUMP_DATA_MATRIX_PATH = os.path.join(DUMP_PATH, "datamatrix.p")


class DataMatrix:
    def __init__(self, df_data_matrix: pd.DataFrame):
        with open(DUMP_DATA_MATRIX_PATH, "w+b") as data_matrix_file:
            pickle.dump(df_data_matrix, data_matrix_file)

    def loadDataMatrix(self) -> pd.DataFrame:
        with open(DUMP_DATA_MATRIX_PATH, "rb") as data_matrix_file:
            return pickle.load(data_matrix_file)

