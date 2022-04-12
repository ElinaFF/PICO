from unittest.mock import patch
import pytest as pytest

from metabodashboard.domain import MetaboExperiment

from TestsUtility import TRAIN_TEST_PROPORTION, NUMBER_OF_SPLITS, CLASSES_DESIGN, EXPERIMENT_NAME


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment


@patch('metabodashboard.domain.ExperimentalDesign.set_split_parameter', return_value=None)
@patch('metabodashboard.domain.ExperimentalDesign.get_name', side_effect=[EXPERIMENT_NAME, EXPERIMENT_NAME + str(1)])
@patch('metabodashboard.domain.ExperimentalDesign.__init__', return_value=None)
def test_givenMetaboExperiment_whenSetSplitsParameters_thenTheExperimentalDesignsAreCorrect(splits, get_name, init,
                                                                                            input_metabo_experiment):
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    input_metabo_experiment.set_splits_parameters(NUMBER_OF_SPLITS, TRAIN_TEST_PROPORTION)
    assert input_metabo_experiment.get_train_test_proportion() == TRAIN_TEST_PROPORTION
    assert input_metabo_experiment.get_number_of_splits() == NUMBER_OF_SPLITS
    assert list(input_metabo_experiment.get_experimental_designs().keys()) == [EXPERIMENT_NAME,
                                                                               EXPERIMENT_NAME + str(1)]


@patch('metabodashboard.domain.ExperimentalDesign.get_name', return_value=EXPERIMENT_NAME)
@patch('metabodashboard.domain.ExperimentalDesign.__init__', return_value=None)
def test_givenMetaboExperiment_whenAddExperimentalDesign_thenTheExperimentalDesignsAreCorrect(get_name, init,
                                                                                              input_metabo_experiment):
    input_metabo_experiment.add_experimental_design(CLASSES_DESIGN)
    assert list(input_metabo_experiment.get_experimental_designs().keys()) == [EXPERIMENT_NAME]
