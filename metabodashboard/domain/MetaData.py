import os.path
import pickle

import pandas as pd

ROOT_PATH = os.path.dirname(__file__)
DUMP_PATH = os.path.join(ROOT_PATH, os.path.join("dumps", "metadata"))
DUMP_METADATA_PATH = os.path.join(DUMP_PATH, "metadata.p")
DUMP_METADATA_COLUMNS_PATH = os.path.join(DUMP_PATH, "metadata_columns.p")
DUMP_SAMPLES_ID_PATH = os.path.join(DUMP_PATH, "samples_id.p")
DUMP_CLASSES_PATH = os.path.join(DUMP_PATH, "classes.p")


class MetaData:
    def __init__(self, df_meta_data: pd.DataFrame):
        with open(DUMP_METADATA_PATH, "w+b") as metadata_file:
            pickle.dump(df_meta_data, metadata_file)

        with open(DUMP_METADATA_COLUMNS_PATH, "w+b") as metadata_file:
            pickle.dump(list(df_meta_data.columns), metadata_file)

        self._id_column = None
        self._target_column = None
        self._classes_design = None

    def load_metadata(self) -> pd.DataFrame:
        with open(DUMP_METADATA_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def load_columns(self):
        with open(DUMP_METADATA_COLUMNS_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def get_formatted_columns(self) -> list:
        columns_with_none = ["None"] + self.load_columns()
        return [{'label': column, 'value': column} for column in columns_with_none]

    def get_formatted_unique_targets(self) -> list:
        targets = self.load_classes()
        possible_targets = list(set(targets))
        return [{'label': target, 'value': target} for target in possible_targets]

    def set_id_column(self, id_column: str):
        df_metadata = self.load_metadata()
        with open(DUMP_SAMPLES_ID_PATH, "w+b") as metadata_file:
            pickle.dump(df_metadata[id_column].tolist(), metadata_file)

        self._id_column = id_column

    def set_target_column(self, target_column: str):
        self._target_column = target_column

    def set_classes_design(self):
        targets = self.load_classes()
        reverse_classes_design = {target: class_ for class_, target in self._classes_design.items()}
        classes = []
        for target in targets:
            classes.append(reverse_classes_design[target])
        with open(DUMP_CLASSES_PATH, "w+b") as classes_file:
            pickle.dump(classes, classes_file)

    def load_samples_id(self) -> list:
        if self._id_column is None:
            raise RuntimeError("Try to access the samples id column before setting one")
        with open(DUMP_SAMPLES_ID_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

    def load_classes(self) -> list:
        if self._classes_design is None:
            raise RuntimeError("Try to access the classes before setting the column.")
        with open(DUMP_CLASSES_PATH, "rb") as metadata_file:
            return pickle.load(metadata_file)

# TODO: join sampleId and target in same pickle file
