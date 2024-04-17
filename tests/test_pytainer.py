import pytest
from pytainer.pytainer import Pytainer

@pytest.fixture
def mock_api():
    with httpx_mock.Mocker() as m:
        yield m

@pytest.fixture
def user_repository(mock_api):
    base_url = "https://api.example.com"
    repo = UserRepository(base_url)
    return repo
@pytest.fixture
def api_client():
    # Initialize your API client with appropriate configuration
    client = Pytainer(url='https://portaienr.free.beeceptor.com')
    return client

# Test case to check if the API client can retrieve data
def test_api_get_data(api_client):
    data = api_client.stack.get()
    assert data is not None
    assert data == {"resp": "api"}

def test_api_auth(api_client):
    data = api_client.auth(login='test')
    assert data == {"resp": "test"}