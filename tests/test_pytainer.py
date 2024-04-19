import httpx
from pytest_httpx import HTTPXMock

from pytainer.pytainer import (
    Pytainer,
    AuthAuthenticatePayload,
    AuthAuthenticateResponse,
)


def test_portainer_init():
    portainer = Pytainer(base_url="https://portainer.test/", api_token="ASDASDASDASDASD")
    assert portainer.base_url == "https://portainer.test/"
    assert portainer.headers == {}
    assert portainer.api_token == "ASDASDASDASDASD"
    assert isinstance(portainer.requester, httpx.Client)


def test_portainer_auth(httpx_mock: HTTPXMock):
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsImV4cCI6MTQ5OTM3NjE1NH0.NJ6vE8FY1WG6jsRQzfMqeatJ4vh2TWAeeYfDhP71YEE"
    httpx_mock.add_response(
        method="POST",
        url="https://portainer.test/api/auth",
        json=AuthAuthenticateResponse(jwt=jwt).model_dump(),
    )
    portainer = Pytainer(base_url="https://portainer.test", api_token="asd")

    with httpx.Client() as client:
        resp = portainer.auth.auth(username="test-login", password="test-password")
        assert portainer.api_token == jwt
        assert isinstance(resp, AuthAuthenticateResponse)
        assert resp.jwt == jwt
