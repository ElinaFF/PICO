import pytest
import uuid
import random
from sklearn.tree import DecisionTreeClassifier
import time
import math

from pico.domain import Results
from ..TestsUtility import NUMBER_OF_SPLITS, RESULTS, SAMPLES_ID, CLASSES, CLASSES_DESIGN, IMPORTANCE_ATTRIBUTE, \
    DATAMATRIX_DATAFRAME


@pytest.fixture
def input_results() -> Results:
    return Results(NUMBER_OF_SPLITS)


def test_givenFeatures_whenFormatNameAndAssociatedValues_thenValid(input_results):
    # There can be 14k features times 25 splits
    # The values are 0 and over
    # Let's simulate random features name
    n_features = 14_000
    n_splits = 25

    # Create deterministic names and values
    random.seed(42)
    names = [str(uuid.UUID(int=random.getrandbits(128), version=4)) for _ in range(n_features)] * n_splits
    values = [random.random() for _ in range(len(names))]
    values = [0 if v < 0.5 else v for v in values] # introduce some zeroes

    start_time = time.time()
    features_stats = input_results.format_name_and_associated_values(names, values)
    first_feature = features_stats[names[0]]
    assert names[0] == 'bdd640fb-0667-4ad1-9c80-317fa3b1799d'
    assert math.isclose(first_feature[0], 15.)
    assert math.isclose(first_feature[1], 0.7380823693490595)
    stop_time = time.time()
    print("Total time", stop_time - start_time)

    # Test when inputs are empty
    features = input_results.format_name_and_associated_values([], [])
    assert features == {}

    # Test when only zeros
    features = input_results.format_name_and_associated_values(["a", "a", "a", "a"], [0, 0, 0, 0])
    assert features["a"][0] == 0
    assert features["a"][1] == 0
    assert features["a"][2] == 0


def test_givenResults_whenProduceMetricsTable_thenReturnTable(input_results):
    input_results.results = RESULTS
    print(input_results.produce_metrics_table())


def test_givenModelResults_whenAddResults_thenReturnNoThrow(input_results):

    tree = DecisionTreeClassifier(random_state=42)
    tree.fit(DATAMATRIX_DATAFRAME[:10], CLASSES[:10])

    input_results.add_results_from_one_algo_on_one_split(
        tree,
        DATAMATRIX_DATAFRAME,
        IMPORTANCE_ATTRIBUTE,
        list(CLASSES_DESIGN.keys()),
        CLASSES[10:],
        CLASSES[10:],
        CLASSES[:10],
        CLASSES[:10],
        "0",
        SAMPLES_ID[10:],
        SAMPLES_ID[:10],
    )
