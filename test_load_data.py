import pytest
import requests
from load_data import get_crypto_info, fetch_crypto_ids


@pytest.fixture
def mock_requests_get(mocker):
    """Fixture to mock requests.get."""
    return mocker.patch('requests.get')


def test_get_crypto_info_success(mock_requests_get):
    """Test case for a successful API call."""
    mock_response = [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin",
                      "image": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = get_crypto_info("bitcoin")

    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)


def test_get_crypto_info_failure(mock_requests_get):
    """Test case for a failed API call."""
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Network Error")

    result = get_crypto_info("bitcoin")
    assert result is None


def test_fetch_crypto_ids_success(mock_requests_get):
    """Test case for a successful API call."""
    mock_response = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum"}
    ]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = fetch_crypto_ids()

    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert "bitcoin" in result
    assert "ethereum" in result


def test_fetch_crypto_ids_failure(mock_requests_get):
    """Test case for a failed API call."""
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Network Error")

    result = fetch_crypto_ids()
    assert result == []
