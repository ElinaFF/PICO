import pandas as pd
import pytest as pytest

from metabodashboard.domain import MetaboExperiment, MetaData

CLASSES_DESIGN = {"sick": ["sick", "ill"], "healthy": ["healthy"]}
NUMBER_OF_SPLITS = 3
TRAIN_TEST_PROPORTION = 0.666
METADATA_DATAFRAME = pd.DataFrame(data={"meta1": ["11", "12", "13"], "meta2": ["21", "22", "23"],
                                        "meta3": ["sick", "healthy", "ill"]})
TARGET_COLUMN = "meta3"
ID_COLUMN = "meta1"
METADATA = MetaData(METADATA_DATAFRAME)
METADATA.setTargetColumn(TARGET_COLUMN)
METADATA.setIdColumn(ID_COLUMN)


@pytest.fixture
def input_metabo_experiment():
    metabo_experiment = MetaboExperiment()
    return metabo_experiment


def testThrowRuntimeErrorWhenAddingExperimentGivenNoNumberOfSplit(input_metabo_experiment):
    input_metabo_experiment.setMetadata(METADATA)
    input_metabo_experiment.setTrainTestProportion(TRAIN_TEST_PROPORTION)
    with pytest.raises(RuntimeError) as e_info:
        input_metabo_experiment.addExperimentalDesign(CLASSES_DESIGN)


def testThrowRuntimeErrorWhenAddingExperimentGivenNoTrainTestSplitProportion(input_metabo_experiment):
    input_metabo_experiment.setMetadata(METADATA)
    input_metabo_experiment.setNumberOfSplits(NUMBER_OF_SPLITS)
    with pytest.raises(RuntimeError) as e_info:
        input_metabo_experiment.addExperimentalDesign(CLASSES_DESIGN)


def testThrowRuntimeErrorWhenAddingExperimentGivenNoMetaData(input_metabo_experiment):
    input_metabo_experiment.setNumberOfSplits(NUMBER_OF_SPLITS)
    input_metabo_experiment.setTrainTestProportion(TRAIN_TEST_PROPORTION)
    with pytest.raises(RuntimeError) as e_info:
        input_metabo_experiment.addExperimentalDesign(CLASSES_DESIGN)
