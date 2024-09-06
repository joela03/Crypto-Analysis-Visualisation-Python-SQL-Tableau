import pytest
import requests
from load_data import get_crypto_info


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
