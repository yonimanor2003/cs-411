import pytest
from unittest.mock import patch
from meal_max.utils.random_utils import get_random


@pytest.fixture
def mock_response():
    """Fixture to provide a mock response for the random.org request."""
    return "0.75"  # Example random number as a string


@patch('meal_max.utils.random_utils.requests.get')
def test_get_random_success(mock_get, mock_response):
    """Test fetching a random number successfully."""
    mock_get.return_value.text = mock_response
    mock_get.return_value.status_code = 200

    random_number = get_random()
    assert random_number == 0.75
    mock_get.assert_called_once()  # Ensure the request was made


@patch('meal_max.utils.random_utils.requests.get')
def test_get_random_invalid_response(mock_get):
    """Test error handling when the response cannot be converted to a float."""
    mock_get.return_value.text = "invalid"
    mock_get.return_value.status_code = 200

    with pytest.raises(ValueError, match="Invalid response from random.org: invalid"):
        get_random()


@patch('meal_max.utils.random_utils.requests.get')
def test_get_random_timeout(mock_get):
    """Test error handling for a timeout exception."""
    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()


@patch('meal_max.utils.random_utils.requests.get')
def test_get_random_request_exception(mock_get):
    """Test error handling for a generic request exception."""
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()
