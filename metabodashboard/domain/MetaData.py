import os.path
import pickle

import pandas as pd

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "metadata"))
DUMP_METADATA_PATH = os.path.join(DUMP_PATH, "metadata.p")
DUMP_METADATA_COLUMNS_PATH = os.path.join(DUMP_PATH, "metadata_columns.p")
DUMP_TARGETS_PATH = os.path.join(DUMP_PATH, "targets.p")
DUMP_SAMPLES_ID_PATH = os.path.join(DUMP_PATH, "samples_id.p")


class MetaData:
    def __init__(self, df_meta_data: pd.DataFrame):
        with open(DUMP_METADATA_PATH, "w+b") as metadata_file:
            pickle.dump(df_meta_data, metadata_file)

        with open(DUMP_METADATA_COLUMNS_PATH, "w+b") as metadata_file:
            pickle.dump(list(df_meta_data.columns), metadata_file)

        self._id_column = None
        self._target_column = None

    def loadMetadata(self) -> pd.DataFrame:
        with open(DUMP_METADATA_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def loadColumns(self):
        with open(DUMP_METADATA_COLUMNS_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def getFormattedColumns(self) -> list:
        columns_with_none = ["None"] + self.loadColumns()
        return [{'label': column, 'value': column} for column in columns_with_none]

    def getFormattedUniqueTargets(self) -> list:
        targets = self.loadTargets()
        possible_targets = list(set(targets))
        return [{'label': target, 'value': target} for target in possible_targets]

    def setIdColumn(self, id_column: str):
        df_metadata = self.loadMetadata()
        with open(DUMP_SAMPLES_ID_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[id_column].tolist(), metadata_file)

        self._id_column = id_column

    def setTargetColumn(self, target_column: str):
        df_metadata = self.loadMetadata()
        with open(DUMP_TARGETS_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[target_column].tolist(), metadata_file)

        self._target_column = target_column

    def loadSamplesId(self) -> list:
        if self._id_column is None:
            raise RuntimeError("Try to access the samples id column before setting one")
        with open(DUMP_SAMPLES_ID_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def loadTargets(self) -> list:
        if self._target_column is None:
            raise RuntimeError("Try to access the target column before setting one")
        with open(DUMP_TARGETS_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

# TODO: getGroupByDesignTarget(self, classes_design: dict):
