import os.path
import pickle
from typing import List

import pandas as pd

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "metadata"))
DUMP_METADATA_PATH = os.path.join(DUMP_PATH, "metadata.p")
DUMP_METADATA_COLUMNS_PATH = os.path.join(DUMP_PATH, "metadata_columns.p")
DUMP_SAMPLES_ID_PATH = os.path.join(DUMP_PATH, "samples_id.p")
DUMP_TARGETS_PATH = os.path.join(DUMP_PATH, "targets.p")


class MetaData:
    def __init__(self, metadata_dataframe: pd.DataFrame = None):

        if metadata_dataframe is not None:
            self.save_metadata(metadata_dataframe)

        self._id_column = None
        self._target_column = None

    def read_format_and_store_metadata(self):

        file_ext = self.filename.split(".")[-1]
        # TODO : beware of the sep (, or ;)
        if "csv" in file_ext:  # Abundance matrices of Progenesis are always in csv format, so its checked first
            if self.in_format == "base64":  # this condition is to make readable the input data from dcc.Upload
                self.data = io.StringIO(self.data.decode('utf-8'))
            else:  # this else is to enable the pd dataframe to be read from full file path
                self.data = self.filename
            header = pd.read_csv(self.data, header=None, sep=",", nrows=3, index_col=0).fillna('').to_numpy()
            print("---> DataFormat.py -> _convert_from_file : header")
            print(header)
            if "Normalised abundance" in header[0] or "Raw abundance" in header[0]:
                datatable = pd.read_csv(self.data, header=[0, 1, 2], sep=","
                                        , index_col=0)
                return self._read_Progenesis_data_table(datatable, header)
            else:
                datatable = pd.read_csv(self.data, sep=",", index_col=0)
                return self._read_general_data_table(datatable)

        elif "xls" in file_ext or "od" in file_ext:  # TODO : restrict the "od" condition, might be too large
            if self.in_format == "base64":  # same as above
                self.data = io.StringIO(io.BytesIO(self.data))
            else:
                self.data = self.filename
            datatable = pd.read_excel(self.data, index_col=0)
            return self._read_general_data_table(datatable)

        else:
            raise TypeError("The input file is not of the right type, must be excel, odt or csv.")

        self.save_metadata(df)
        return df

    def save_metadata(self, df_meta_data: pd.DataFrame):
        with open(DUMP_METADATA_PATH, "w+b") as metadata_file:
            pickle.dump(df_meta_data, metadata_file)

        with open(DUMP_METADATA_COLUMNS_PATH, "w+b") as metadata_file:
            pickle.dump(list(df_meta_data.columns), metadata_file)

    def load_metadata(self) -> pd.DataFrame:
        with open(DUMP_METADATA_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def load_columns(self) -> List[str]:
        with open(DUMP_METADATA_COLUMNS_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def get_formatted_columns(self) -> List[dict]:
        columns_with_none = self.load_columns()
        return [{'label': column, 'value': column} for column in columns_with_none]

    def get_formatted_unique_targets(self) -> List[dict]:
        targets = self.load_metadata()[self._target_column]
        print("MetaData -> get_formatted_unique_targets : print self._target_column = {}".format(self._target_column))
        possible_targets = list(set(targets))
        return [{'label': target, 'value': target} for target in possible_targets]

    def set_id_column(self, id_column: str) -> None:
        df_metadata = self.load_metadata()
        with open(DUMP_SAMPLES_ID_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[id_column].tolist(), metadata_file)

        self._id_column = id_column

    def set_target_column(self, target_column: str) -> None:
        self._target_column = target_column
        df_metadata = self.load_metadata()
        with open(DUMP_TARGETS_PATH, "w+b") as target_file:
            pickle.dump(df_metadata[target_column].tolist(), target_file)

    def load_targets(self) -> List[str]:
        if self._target_column is None:
            raise RuntimeError("Try to access the targets before setting the column.")
        with open(DUMP_TARGETS_PATH, "rb") as target_file:
            return pickle.load(target_file)

    def load_samples_id(self) -> List[str]:
        if self._id_column is None:
            raise RuntimeError("Try to access the samples id column before setting one")
        with open(DUMP_SAMPLES_ID_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

# TODO: join sampleId and target in same pickle file
