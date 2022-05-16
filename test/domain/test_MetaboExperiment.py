from unittest.mock import patch

import pandas as pd
import pytest as pytest
from sklearn.model_selection import RandomizedSearchCV

from ...metabodashboard.domain import MetaboExperiment, MetaboModel, SplitGroup

from .TestsUtility import TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME, SPLITS, \
    MOCKED_METADATA, SAMPLES_ID


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment


def test_givenMetaboExperiment_whenAddExperimentalDesign_thenTheExperimentalDesignsAreCorrect(input_metabo_experiment):
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    assert list(input_metabo_experiment.get_experimental_designs().keys()) == [EXPERIMENT_NAME]


def test_givenMetaboExperiment_whenGetSelectedCvType_thenTheCvTypeIsCorrect(input_metabo_experiment):
    input_metabo_experiment.set_cv_type('RandomizedSearchCV')
    assert input_metabo_experiment.get_selected_cv_type() == "RandomizedSearchCV"


def test_givenMetaboExperiment_whenChangeCvType_thenTheCvTypeIsCorrect(input_metabo_experiment):
    input_metabo_experiment.set_cv_type('RandomizedSearchCV')
    assert input_metabo_experiment.get_cv_algorithm() == RandomizedSearchCV


def test_givenMetaboExperiment_whenChangeCvTypeToIncorrect_thenRaiseValueError(input_metabo_experiment):
    with pytest.raises(ValueError):
        input_metabo_experiment.set_cv_type('alibaba')

