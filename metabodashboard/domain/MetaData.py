import os.path
import pickle

import pandas as pd

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "metadata"))
DUMP_METADATA_PATH = os.path.join(DUMP_PATH, "metadata.p")
DUMP_TARGETS_PATH = os.path.join(DUMP_PATH, "targets.p")
DUMP_SAMPLES_ID_PATH = os.path.join(DUMP_PATH, "samples_id.p")


class MetaData:
    def __init__(self, df_meta_data: pd.DataFrame):
        with open(DUMP_METADATA_PATH, "w+b") as metadata_file:
            pickle.dump(df_meta_data, metadata_file)

        self.metadata_columns = list(df_meta_data.columns)
        self.id_column = None
        self.target_column = None

    def loadMetadata(self) -> pd.DataFrame:
        with open(DUMP_METADATA_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def getFormattedColumns(self) -> list:
        columns_with_none = ["None"] + self.metadata_columns
        return [{'label': column, 'value': column} for column in columns_with_none]

    def getFormattedTargets(self) -> list:
        if self.target_column is None:
            raise RuntimeError("Try to access the target column before setting one")
        df_metadata = self.loadMetadata()
        possible_targets = list(set(list(df_metadata[self.target_column])))
        return [{'label': target, 'value': target} for target in possible_targets]

    def setIdColumn(self, id_column: str):
        df_metadata = self.loadMetadata()
        with open(DUMP_SAMPLES_ID_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[id_column], metadata_file)

        self.id_column = id_column

    def setTargetColumn(self, target_column: str):
        df_metadata = self.loadMetadata()
        with open(DUMP_TARGETS_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[target_column], metadata_file)

        self.target_column = target_column

    def loadSamplesId(self) -> list:
        if self.id_column is None:
            raise RuntimeError("Try to access the samples id column before setting one")
        with open(DUMP_SAMPLES_ID_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def loadTargets(self) -> list:
        if self.target_column is None:
            raise RuntimeError("Try to access the target column before setting one")
        with open(DUMP_TARGETS_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)
