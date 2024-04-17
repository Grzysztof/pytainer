import pytest
import requests_mock
from user_repository import UserRepository

@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def user_repository(mock_api):
    base_url = "https://api.example.com"
    repo = UserRepository(base_url)
    return repo