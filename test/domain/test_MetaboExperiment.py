from unittest.mock import patch

import pandas as pd
import pytest as pytest

from ...metabodashboard.domain import MetaboExperiment, SplitGroup

from .TestsUtility import TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME, SPLITS, \
    MOCKED_METADATA, SAMPLES_ID


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment


def test_givenMetaboExperiment_whenAddExperimentalDesign_thenTheExperimentalDesignsAreCorrect(input_metabo_experiment):
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    assert list(input_metabo_experiment.get_experimental_designs().keys()) == [EXPERIMENT_NAME]
