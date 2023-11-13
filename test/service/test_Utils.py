import pytest
import os

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

from ...metabodashboard.service import Utils

from ..TestsUtility import (CLASSES_DESIGN, TARGETS, CLASSES,
                            PARTIAL_CLASSES_DESIGN, FILTERED_CLASSES, FILTERED_TARGETS)


def test_givenUtils_whenGetFilePath_thenReturnFilePath():
    assert Utils.DUMP_EXPE_PATH == os.path.join(
        os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2]),
        "metabodashboard",
        "domain",
        "dumps",
        "save.mtxp",
    )


def test_givenBinaryClass_whenGettingBinary_thenBinaryIsReturned():
    assert Utils.get_binary(["b", "c", "b", "c"], ["b", "c"]) == [0, 1, 0, 1]


def test_givenMultiClass_whenGettingBinary_thenBinaryIsReturned():
    assert Utils.get_binary(["b", "c", "b", "c", "a", "c"], ["a", "b", "c"]) == [
        1,
        2,
        1,
        2,
        0,
        2,
    ]


def test_given_str_to_convert_when_converting_to_list_of_lists_then_return_list_of_lists():
    assert Utils.convert_str_to_list_of_lists("[1,2],[3,4]") == [[1, 2], [3, 4]]


def test_given_str_to_convert_when_converting_to_list_then_return_list():
    assert Utils.convert_str_to_list_of_lists("[1,2]") == [[1, 2]]


def test_given_PCA_when_getting_model_parameters_then_return_attributes():
    assert Utils.get_model_parameters(PCA) == [('n_components', 'NoneType'),
                                               ('copy', 'bool'),
                                               ('whiten', 'bool'),
                                               ('svd_solver', 'str'),
                                               ('tol', 'float'),
                                               ('iterated_power', 'str'),
                                               ('n_oversamples', 'int'),
                                               ('power_iteration_normalizer', 'str')]


def test_given_DecisionTreeClassifier_when_getting_model_parameters_then_return_attributes():
    assert Utils.get_model_parameters(DecisionTreeClassifier) == [('criterion', 'str'),
                                                                  ('splitter', 'str'),
                                                                  ('max_depth', 'NoneType'),
                                                                  ('min_samples_split', 'int'),
                                                                  ('min_samples_leaf', 'int'),
                                                                  ('min_weight_fraction_leaf', 'float'),
                                                                  ('max_features', 'NoneType'),
                                                                  ('max_leaf_nodes', 'NoneType'),
                                                                  ('min_impurity_decrease', 'float'),
                                                                  ('class_weight', 'NoneType'),
                                                                  ('ccp_alpha', 'float')]


def test_givenDT_whenGetParametersAfterTraining_thenReturnParameters():
    assert Utils.get_model_parameters_after_training(DecisionTreeClassifier) == [('feature_importances_', 'ndarray')]


def test_givenRF_whenGetParametersAfterTraining_thenReturnParameters():
    assert Utils.get_model_parameters_after_training(RandomForestClassifier) == [('feature_importances_', 'ndarray')]

def test_givenSVCwithMutuallyExclusiveParamater_whenGetParametersAfterTraining_thenReturnParameters():
    assert Utils.get_model_parameters_after_training(LinearSVC) == [('coef_', 'ndarray')]


def test_givenListAsString_whenConvertStringToList_thenListIsReturned():
    assert Utils.convert_str_to_list_of_lists("[1, 2, 3], [a, b, c], [15.35, .35, 15]") == [
        [1, 2, 3],
        ["a", "b", "c"],
        [15.35, 0.35, 15],
    ]


def test_givenTargets_whenLoadCalssesFromTargets_thenClassesAreReturned():
    assert Utils.load_classes_from_targets(CLASSES_DESIGN, TARGETS) == CLASSES


def test_givenPartialTargets_whenLoadCalssesFromTargets_thenPartialClassesAreReturned():
    assert Utils.load_classes_from_targets(PARTIAL_CLASSES_DESIGN, FILTERED_TARGETS) == FILTERED_CLASSES


def test_givenTargetsAndPartialDesign_whenLoadCalssesFromTargets_thenThrowValueError():
    with pytest.raises(ValueError):
        Utils.load_classes_from_targets(PARTIAL_CLASSES_DESIGN, TARGETS)
