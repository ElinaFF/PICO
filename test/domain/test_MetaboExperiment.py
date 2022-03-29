import pandas as pd
import pytest as pytest

from metabodashboard.domain import MetaboExperiment, MetaData

from TestsUtility import METADATA_DATAFRAME, TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment

