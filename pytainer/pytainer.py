import httpx
import json
import os
from urllib.parse import urljoin

class Pytainer:
    _base_url: str
    _headers: dict
    _api_token: str

    def __init__(self, * , base_url: str | None) -> None:
        if not base_url:
            self._base_url = os.getenv('PORTAINER_URL')
        else:
            self._base_url = base_url
        
        self._headers = {}

        self.stack = Stack(self)
        self.auth = Auth(self)


class APIResource:
    _client: Pytainer

    def __init__(self, client: Pytainer) -> None:
        self.client = client

# IMPL
class Stack(APIResource):
    _base_path = '/stacks'

    def get(self) -> dict:
        test = httpx.get(urljoin(self.client._base_url, self._base_path))
        print(test.json())
        return test.json()


class Auth(APIResource):
    _base_path = '/auth'

    def __call__(self, login: str | None) -> dict:
        self.headers = {"X-Client-ID": "ABC123"}
        auth_req = httpx.get(urljoin(self.client._base_url, self._base_path))
        self.client._api_token = auth_req.json()['jwt']
        print(auth_req.json())
        return(auth_req.json())