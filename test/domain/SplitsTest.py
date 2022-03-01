import pytest
from sklearn.model_selection import train_test_split

from metabodashboard.domain import Splits

LABELS = ["sick", "healthy", "healthy", "healthy", "healthy", "healthy", "sick", "sick", "healthy", "healthy"]
SAMPLES_ID = ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9", "id10"]
TRAIN_TEST_PROPORTION = 0.20
NUMBER_OF_SPLIT = 3


@pytest.fixture
def input_splits():
    splits = Splits(LABELS, SAMPLES_ID, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLIT)
    return splits


def testGetSplitsWithIndex(input_splits):
    for split_index in range(NUMBER_OF_SPLIT):
        assert train_test_split(SAMPLES_ID, LABELS, test_size=TRAIN_TEST_PROPORTION, random_state=split_index) == \
               input_splits.getSplitsWithIndex(split_index)
