import pytest
from sklearn.tree import DecisionTreeClassifier

from ...metabodashboard.domain import Results
from ..TestsUtility import NUMBER_OF_SPLITS, RESULTS, SAMPLES_ID, CLASSES, CLASSES_DESIGN, IMPORTANCE_ATTRIBUTE, \
    DATAMATRIX_DATAFRAME


@pytest.fixture
def input_results() -> Results:
    return Results(NUMBER_OF_SPLITS)


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
