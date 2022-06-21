from unittest.mock import patch, mock_open

import pytest
from sklearn.model_selection import train_test_split

from ...metabodashboard.domain import SplitGroup

from .TestsUtility import MOCKED_METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME, \
    SPLITS, PAIRING_DICT, FILTERED_ID, COMPUTED_PATTERNS


@pytest.fixture
def input_splits():
    with patch('builtins.open', new_callable=mock_open()):
        return SplitGroup(MOCKED_METADATA, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, PAIRING_DICT)


@patch('pickle.load', side_effect=SPLITS)
@patch('builtins.open', new_callable=mock_open())
def test_givenASplitGroup_whenLoadSplitWithIndex_thenTheSplitsAreReproducible(pickle_mock, open_mock, input_splits):
    for split_index in range(NUMBER_OF_SPLITS):
        assert input_splits.load_split_with_index(split_index) == SPLITS[split_index]


def test_givenASplitGroup_whenGetNumberOfSplit_thenNumberOfSplitsIsCorrect(input_splits):
    assert input_splits.get_number_of_splits() == NUMBER_OF_SPLITS


def test_givenASplitGroup_whenFilterSample_thenSamplesAreFiltered(input_splits):
    assert input_splits.filter_sample_with_pairing_group(PAIRING_DICT) == FILTERED_ID


def test_givenASplitGroup_whenComputePattern_thenPatternsAreComputed(input_splits):
    actual_patterns = input_splits.compute_pattern(PAIRING_DICT)
    for pattern in actual_patterns:
        assert pattern in COMPUTED_PATTERNS

    for pattern in COMPUTED_PATTERNS:
        assert pattern in actual_patterns
