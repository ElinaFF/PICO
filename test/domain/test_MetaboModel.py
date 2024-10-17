import pytest
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier

from ..TestsUtility import FOLDS, DATA, CLASSES, PARAMETER_GRID, NUMBER_OF_PROCESSES, IMPORTANCE_ATTRIBUTE, SEED
from ...medic.domain.MetaboModel import MetaboModel


@pytest.fixture
def input_metabomodel() -> MetaboModel:
    return MetaboModel(DecisionTreeClassifier, PARAMETER_GRID, IMPORTANCE_ATTRIBUTE)


def test_givenModel_whenTuningWithGridSearch_thenReturnBestModel(input_metabomodel):
    best_model = input_metabomodel.train(
        FOLDS, DATA, CLASSES, GridSearchCV, [], NUMBER_OF_PROCESSES, 42
    )
    real_model = GridSearchCV(
        DecisionTreeClassifier(random_state=42), PARAMETER_GRID, cv=FOLDS
    )
    real_model.fit(DATA, CLASSES)
    assert best_model.get_params() == real_model.best_estimator_.get_params()


def test_givenModel_whenTuningWithRandomizedSearch_thenReturnBestModel(
    input_metabomodel,
):
    real_model = RandomizedSearchCV(
        DecisionTreeClassifier(random_state=42),
        PARAMETER_GRID,
        cv=FOLDS,
        random_state=42,
    )
    real_model.fit(DATA, CLASSES)
    for i in range(10):
        print(f"Run {i}")
        best_model = input_metabomodel.train(
            FOLDS, DATA, CLASSES, RandomizedSearchCV, [{"value": 10}], NUMBER_OF_PROCESSES, 42
        )
        assert best_model.get_params() == real_model.best_estimator_.get_params()
