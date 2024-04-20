import httpx
import os
from urllib.parse import urljoin
from pydantic import BaseModel
from enum import Enum


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class AuthAuthenticatePayload(BaseModel):
    username: str
    password: str


class AuthAuthenticateResponse(BaseModel):
    jwt: str


class SystemInfoResponse(BaseModel):
    agents: int
    edgeAgents: int
    platform: str

class SystemBuildInfo(BaseModel):
    buildNumber: str
    goVersion: str
    imageTag: str
    nodejsVersion: str
    webpackVarsion: str
    yarnVersion: str

class SystemVersionResponse(BaseModel):
    latestVersion: str
    UpdateAvailable: bool
    build: SystemBuildInfo
    databaseVersion: str
    serverVersion: str

class AutoUpdateSettings(BaseModel):
    forcePullImage: bool
    forceUpdate: bool
    interval: int
    jobID: str
    webhook: str

class StackOption(BaseModel):
    prune: bool

class TeamResourceAccess(BaseModel):
    AccessLevel: int
    TeamId: int

class UserResourceAccess(BaseModel):
    AccessLevel: int
    UserId: int

class ResourceControl(BaseModel):
    AccessKevel: int
    AdministratorsOnly: bool
    Id: int
    OwnerId: int
    Public: bool
    ResourceId: str
    SubResourceIds: list[str]
    System: bool
    TeamAccesses: list[TeamResourceAccess]
    Type: int
    UserAccesses: list[UserResourceAccess]

class GitAuthentication(BaseModel):
    gitCredentialID: int
    password: str
    username: str

class Pair(BaseModel):
    name: str
    value: str

class RepoConfig(BaseModel): # Thats gittypes.RepoConfig
    authentication: GitAuthentication
    configFilePath: str
    configHash: str
    referenceName: str
    tlsskipVerify: bool
    url: str

class Stack(BaseModel):
    AdditionalFiles: list[str]
    AutoUpdate: AutoUpdateSettings
    EndpointID: int
    EntryPoint: list[str]
    Env: list[Pair]
    Id: int
    Name: str
    Option: StackOption
    ResourceControl: ResourceControl
    Status: int
    SwarmId: str
    Type: int
    createdBy: str
    creationDate: int
    fromAppTemplate: bool
    gitConfig: RepoConfig
    isComposeFormat: bool
    namespace: str
    projectPath: str
    updateDate: int
    updatedBy: str

class Pytainer:
    _base_url: str
    _headers: dict
    _api_token: str
    _requester: httpx.Client

    def __init__(
        self,
        base_url: str | None,
        api_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        if not base_url:
            self.base_url = os.getenv("PORTAINER_URL")
        else:
            self.base_url = base_url
        if not api_token:
            self.api_token = os.getenv("PORTAINER_API_TOKEN")
        else:
            self.api_token = api_token

        self._headers = {}
        self._requester = httpx.Client()

        self.stacks = Stacks(self)
        self.auth = Auth(self)
        self.system = System(self)

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

    @base_url.setter
    def base_url(self, url: str) -> None:
        self._base_url = url

    @property
    def requester(self) -> httpx.Client:
        return self._requester

    def make_request(
        self, method: HttpMethod, url: str, data: BaseModel | None = None
    ) -> httpx.Response:
        self.headers["X-API-Key"] = f"{self.api_token}"
        if data:
            data = data.model_dump()
        return self._requester.request(method, url, data=data, headers=self.headers)


class APIResource:
    _client: Pytainer

    def __init__(self, client: Pytainer) -> None:
        self.client = client


class Auth(APIResource):
    _client: Pytainer
    _resource_path: str = "/api/auth"

    def auth(
        self,
        username: str | None,
        password: str | None,
    ) -> AuthAuthenticateResponse:
        if not username:
            username = os.getenv("PORTAINER_USERNAME")
        if not password:
            password = os.getenv("PORTAINER_PASSWORD")
        data = AuthAuthenticatePayload(username=username, password=password)

        auth_req = self.client.make_request(
            HttpMethod.POST,
            urljoin(self.client.base_url, self._resource_path),
            data=data,
        )
        auth_resp = AuthAuthenticateResponse.model_validate(auth_req.json())
        self.client.api_token = auth_resp.jwt
        return auth_resp


class Backup(APIResource):
    pass


class Custom_templates(APIResource):
    pass


class Docker(APIResource):
    pass


class Edge(APIResource):
    pass


class Edge_groups(APIResource):
    pass


class Edge_jobs(APIResource):
    pass


class Edge_stacks(APIResource):
    pass


class Edge_templates(APIResource):
    pass


class Endpoint_groups(APIResource):
    pass


class Endpoints(APIResource):
    pass


class Helm(APIResource):
    pass


class Intel(APIResource):
    pass


class Kubernetes(APIResource):
    pass


class Ldap(APIResource):
    pass


class Motd(APIResource):
    pass


class Registries(APIResource):
    pass


class Resource_controls(APIResource):
    pass


class Roles(APIResource):
    pass


class Settings(APIResource):
    pass


class Ssl(APIResource):
    pass


class Stacks(APIResource):
    _base_path = "/api/stacks"
    _client: Pytainer

    def get(self) -> dict:
        """List stacks"""
        test = self.client.make_request(
            "GET", urljoin(self.client._base_url, self._base_path)
        )
        return test.json()

    pass


class Status(APIResource):
    pass


class System(APIResource):
    def info(self) -> SystemInfoResponse:
        resource_path = "api/system/info"
        request_url = urljoin(self.client.base_url, resource_path)
        info_req = self.client.make_request(HttpMethod.GET, request_url)
        info_resp = SystemInfoResponse.model_validate(info_req.json())
        return info_resp

    def version(self) -> SystemVersionResponse:
        resource_path = "api/system/version"
        request_url = urljoin(self.client.base_url, resource_path)
        version_req = self.client.make_request(HttpMethod.GET, request_url)
        version_resp = SystemInfoResponse.model_validate(version_req.json())
        return version_resp
    
class Tags(APIResource):
    pass


class Team_memberships(APIResource):
    pass


class Teams(APIResource):
    pass


class Templates(APIResource):
    pass


class Upload(APIResource):
    pass


class Users(APIResource):
    pass


class Webhooks(APIResource):
    pass


class Websocket(APIResource):
    pass


class Rbac_enabled(APIResource):
    pass
