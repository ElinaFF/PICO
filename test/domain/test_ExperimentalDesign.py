from unittest.mock import patch, Mock

import pandas as pd
import pytest as pytest

from metabodashboard.domain import ExperimentalDesign, MetaData, SplitGroup

from TestsUtility import MOCKED_METADATA, CLASSES_DESIGN, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS


@pytest.fixture
def input_experimental_design():
    experimental_design = ExperimentalDesign(CLASSES_DESIGN)
    return experimental_design


def testGetNumberOfSplit(input_experimental_design):
    input_experimental_design.set_split_parameter(TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, MOCKED_METADATA)
    assert input_experimental_design.get_number_of_splits() == NUMBER_OF_SPLITS


def testAllSplits(input_experimental_design):
    input_experimental_design.set_split_parameter(TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, MOCKED_METADATA)
    for split_index, (real_split_index, actual_split) in enumerate(input_experimental_design.all_splits()):
        assert split_index == real_split_index


