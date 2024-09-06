import pytest
import requests
from load_data import get_crypto_info


@pytest.fixture
def mock_requests_get(mocker):
    """Fixture to mock requests.get."""
    return mocker.patch('requests.get')
