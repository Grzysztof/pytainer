import httpx
import json
import os
from urllib.parse import urljoin

class Pytainer:
    _requester: httpx.Client
    _base_url: str
    _headers: dict
    _api_token: str

    def __init__(self, * , portainer_adsr: str | None) -> None:
        if not portainer_adsr:
            self._base_url = os.getenv('PORTAINER_URL')
        else:
            self._base_url = portainer_adsr
        

        self._requester = httpx.Client(base_url=self._base_url)
        self._headers = {}

        self.stack = Stack(self)
        self.auth = Auth(self)


class APIResource:
    _client: Pytainer

# IMPL
class Stack(APIResource):
    def get(self) -> dict:
        test = self.client.get('/todos')
        print(test.json())
        return test.json()


class Auth(APIResource):
    def __call__(self, login: str | None) -> dict:
        self.headers = {"X-Client-ID": "ABC123"}
        auth_req = self.client.get('/auth')
        print(auth_req.json())
        return(auth_req.json())

if __name__=="__main__":
    client = Pytainer(url='https://mocki.io/')
    print(dir(client))
    print(vars(client))