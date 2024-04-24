import httpx
from pytest_httpx import HTTPXMock

from pytainer import Pytainer
from pytainer.models.portainer import AuthAuthenticateResponse, SystemInfoResponse, SystemVersionResponse, SystemBuildInfo


def test_portainer_init():
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    assert portainer._base_url == "https://portainer.test/"
    assert portainer._headers == {}
    assert portainer._api_token == "debug-auth-token"
    assert isinstance(portainer._requester, httpx.Client)


def test_auth_auth(httpx_mock: HTTPXMock):
    jwt = "debug-auth-token"
    httpx_mock.add_response(
        method="POST",
        url="https://portainer.test/api/auth",
        json=AuthAuthenticateResponse(jwt=jwt).model_dump(),
    )
    portainer = Pytainer(
        base_url="https://portainer.test", api_token="debug-auth-token"
    )

    with httpx.Client() as client:
        resp = portainer.auth.auth(username="test-login", password="test-password")
        assert portainer.api_token == jwt
        assert isinstance(resp, AuthAuthenticateResponse)
        assert resp.jwt == jwt


def test_system_info(httpx_mock: HTTPXMock):
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    httpx_mock.add_response(
        method="GET",
        url="https://portainer.test/api/system/info",
        json=SystemInfoResponse(agents=0, edgeAgents=0, platform="str").model_dump(),
    )

    with httpx.Client() as client:
        resp = portainer.system.info()
        assert isinstance(resp, SystemInfoResponse)

def test_system_version(httpx_mock: HTTPXMock):
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    httpx_mock.add_response(
        method="GET",
        url="https://portainer.test/api/system/version",
        json=SystemVersionResponse(
            LatestVersion="0.0.0",
            UpdateAvailable=False,
            Build=SystemBuildInfo(
                BuildNumber="0.0.0",
                GoVersion="0.0.0",
                ImageTag="0.0.0",
                NodejsVersion="0.0.0",
                WebpackVersion="0.0.0",
                YarnVersion="0.0.0",
            ),
            DatabaseVersion="0.0.0",
            ServerVersion="0.0.0",
        ).model_dump(),
    )

    with httpx.Client() as client:
        resp = portainer.system.version()
        assert isinstance(resp, SystemVersionResponse)

def test_stacks_list(httpx_mock: HTTPXMock):
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    httpx_mock.add_response(
        method="GET",
        url="https://portainer.test/api/stacks",
        json=[],
    )

    with httpx.Client() as client:
        resp = portainer.stacks.list()
        assert isinstance(resp, list)
        assert len(resp) == 0
