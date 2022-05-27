from unittest.mock import patch, mock_open
import pytest
from sklearn.preprocessing import StandardScaler

from ...metabodashboard.domain import DataMatrix

from .TestsUtility import DATAMATRIX, SAMPLES_ID, SCALED_DATA


@pytest.fixture
def input_data_matrix():
    data_matrix = DataMatrix()
    return data_matrix


@patch('pickle.load', return_value=DATAMATRIX)
@patch('__main__.open', return_value=mock_open())
def test_givenData_whenLoadData_thenDataIsLoaded(open_mock, pickle_mock, input_data_matrix):
    input_data_matrix.load_data()
    assert input_data_matrix.data.equals(DATAMATRIX)


def test_givenData_whenLoadSampleWithEmptyList_thenNoDataIsLoaded(input_data_matrix):
    input_data_matrix.data = DATAMATRIX
    assert input_data_matrix.load_samples_corresponding_to_IDs_in_splits([]).equals(DATAMATRIX.loc[[], :])


def test_givenData_whenLoadSampleWithIdList_thenTheDataIsLoaded(input_data_matrix):
    input_data_matrix.data = DATAMATRIX
    selected_samples = list(SAMPLES_ID[:5])
    assert input_data_matrix.load_samples_corresponding_to_IDs_in_splits(selected_samples).equals(DATAMATRIX.loc[selected_samples, :])


@patch('sklearn.preprocessing.StandardScaler.transform', return_value=SCALED_DATA)
def test_givenData_whenGettingScaleData_thenTheScaleDataIsLoaded(scaler_mock, input_data_matrix):
    input_data_matrix.data = DATAMATRIX
    assert input_data_matrix.get_scale_data().equals(SCALED_DATA)


def test_givenNoData_whenLoadSampleWithIdList_thenThrowException(input_data_matrix):
    with pytest.raises(RuntimeError):
        input_data_matrix.load_samples_corresponding_to_IDs_in_splits(SAMPLES_ID)


def test_givenNoData_whenGettingScaledData_thenThrowException(input_data_matrix):
    with pytest.raises(RuntimeError):
        input_data_matrix.get_scale_data()
