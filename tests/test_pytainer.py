import pytest
import httpx
from pytest_httpx import HTTPXMock

from pytainer.pytainer import Pytainer


def test_get_stacks(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://portainer.test/stacks", json={"resp": "test"})
    portainer = Pytainer(base_url="https://portainer.test")

    with httpx.Client() as client:
        resp = portainer.stack.get()
        assert resp == {"resp": "test"}

def test_auth(httpx_mock: HTTPXMock):
    login = "test-login"
    httpx_mock.add_response(url="https://portainer.test/auth", json={"jwt": login})
    portainer = Pytainer(base_url="https://portainer.test")

    with httpx.Client() as client:
        resp = portainer.auth(login)
        assert portainer._api_token == login
        assert resp == {"jwt": login}