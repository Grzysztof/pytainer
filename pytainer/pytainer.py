import httpx
import os
from urllib.parse import urljoin

class Pytainer:
    _base_url: str
    _headers: dict
    _api_token: str
    _requester: httpx.Client

    def __init__(self, * , base_url: str | None, api_token: str | None) -> None:
        if not base_url:
            self._base_url = os.getenv('PORTAINER_URL')
        else:
            self._base_url = base_url
        if not api_token:
            self._api_token = os.getenv('PORTAINER_API_TOKEN')
        else:
            self._api_token = api_token

        self._headers = {}
        self._requester = httpx.Client()

        self.stack = Stack(self)
        self.auth = Auth(self)
    
    @property
    def headers(self) -> dict:
        return self._headers
    
    @headers.setter
    def headers(self, headers: dict) -> None:
        self._headers.update(headers)

    @property
    def api_token(self) -> str:
        return self._api_token

    @api_token.setter
    def api_token(self, token: str) -> None:
        self._api_token = token
    
    @property
    def base_url(self) -> str:
        return self._base_url
    
    @property
    def requester(self) -> httpx.Client:
        return self._requester

    def make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        print(f'make_request: {self._headers}')
        return self._requester.request(method, url, **kwargs)    


class APIResource: 
    _client: Pytainer

    def __init__(self, client: Pytainer) -> None:
        self.client = client

class Stack(APIResource):
    _base_path = '/stacks'
    _client: Pytainer
    _test: int = 0

    def get(self) -> dict:
        self._test += 1
        self.client._headers['Test'] = f'{self._test}'
        test = self.client.make_request('GET', urljoin(self.client._base_url, self._base_path))
        print(self.client._headers)
        return test.json()


class Auth(APIResource):
    _base_path = '/auth'
    _client: Pytainer

    def __call__(self, login: str | None) -> dict:
        self.headers = {"X-Client-ID": "ABC123"}
        auth_req = httpx.get(urljoin(self.client._base_url, self._base_path))
        self.client._api_token = auth_req.json()['jwt']
        self._client._headers['Authorization'] = f"Bearer {self.client._api_token}"
        print(auth_req.json())
        return(auth_req.json())