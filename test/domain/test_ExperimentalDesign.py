import pandas as pd
import pytest as pytest

from metabodashboard.domain import ExperimentalDesign, MetaData, SplitGroup

CLASSES_DESIGN = {"sick": ["sick", "ill"], "healthy_experimental_design_test": ["healthy"]}
NUMBER_OF_SPLITS = 3
TRAIN_TEST_PROPORTION = 0.666
METADATA_DATAFRAME = pd.DataFrame(data={"meta1": ["11", "12", "13"], "meta2": ["21", "22", "23"],
                                        "meta3": ["sick", "healthy", "ill"]})
TARGET_COLUMN = "meta3"
ID_COLUMN = "meta1"
METADATA = MetaData(METADATA_DATAFRAME)
METADATA.setTargetColumn(TARGET_COLUMN)
METADATA.setIdColumn(ID_COLUMN)
EXPERIMENT_NAME = "sick_vs_healthy_expected_experimental_test"
SPLIT_GROUP = SplitGroup(METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME)

@pytest.fixture
def input_experimental_design():
    experimental_design = ExperimentalDesign(CLASSES_DESIGN, NUMBER_OF_SPLITS, TRAIN_TEST_PROPORTION, METADATA)
    return experimental_design


def testAllSplits(input_experimental_design):
    for split_index, actual_split in enumerate(input_experimental_design.allSplits()):
        assert SPLIT_GROUP.loadSplitWithIndex(split_index) == actual_split


