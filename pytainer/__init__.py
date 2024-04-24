import httpx
import os
from urllib.parse import urljoin
from pydantic import BaseModel
from typing import List
from enum import Enum
from pytainer.models import portainer


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class Pytainer:
    _base_url: str
    _headers: dict
    _api_token: str
    _requester: httpx.Client

    def __init__(
        self,
        base_url: str | None = None,
        api_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self._base_url = base_url or os.getenv("PORTAINER_URL")
        self._api_token = api_token or os.getenv("PORTAINER_API_TOKEN")
        
        if not self._api_token:
            raise Exception("API token is required")
        
        if not self._base_url:
            raise Exception("Base URL is required")

        self._headers = {}
        self._requester = httpx.Client()

        self.stacks = Stacks(self)
        self.auth = Auth(self)
        self.system = System(self)
    
    @property
    def base_url(self) -> str:
        return self._base_url

    def make_request(
        self,
        method: HttpMethod,
        url: str,
        params: dict | None = None,
        data: BaseModel | None = None,
    ) -> httpx.Response:
        
        self._headers["X-API-Key"] = f"{self._api_token}"

        if data:
            data = data.model_dump_json()
        req = self._requester.request(
            method, url, data=data, headers=self._headers, params=params
        ).raise_for_status()
        return req


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
    ) -> portainer.AuthAuthenticateResponse:
        if not username:
            username = os.getenv("PORTAINER_USERNAME")
        if not password:
            password = os.getenv("PORTAINER_PASSWORD")
        data = portainer.AuthAuthenticatePayload(username=username, password=password)

        auth_req = self.client.make_request(
            HttpMethod.POST,
            urljoin(self.client.base_url, self._resource_path),
            data=data,
        )
        auth_resp = portainer.AuthAuthenticateResponse.model_validate(auth_req.json())
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

    def list(self) -> List[portainer.Stack]:
        """List stacks https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackList"""
        req = self.client.make_request(
            "GET", urljoin(self.client.base_url, self._base_path)
        )
        return [portainer.Stack.model_validate(stack_item) for stack_item in req.json()]

    def update(
        self, stack_id: int, endpoint_id: int, data: portainer.UpdateSwarmStackPayload
    ) -> dict:
        """Update a stack https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackUpdate"""
        try:
            req = self.client.make_request(
                HttpMethod.PUT,
                urljoin(self.client.base_url, f"{self._base_path}/{stack_id}"),
                params={"endpointId": endpoint_id},
                data=data,
            ).raise_for_status()
            return portainer.Stack.model_validate(req.json())
        except httpx.RequestError as e:
            raise Exception(f"An error occurred while updating the stack: {e}")

    def get(self, stack_id: int) -> portainer.Stack:
        """Get a stack https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackInspect"""
        try:
            req = self.client.make_request(
                HttpMethod.GET,
                urljoin(self.client.base_url, f"{self._base_path}/{stack_id}"),
            ).raise_for_status()
            return portainer.Stack.model_validate(req.json())
        except httpx.RequestError as e:
            raise Exception(
                f"An error occurred while getting the stack: {e}, {req.json()}"
            )

    def get_file(self, stack_id: int) -> portainer.Stack:
        """Get stack file https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackFileInspect"""
        req = self.client.make_request(
            HttpMethod.GET,
            urljoin(self.client.base_url, f"{self._base_path}/{stack_id}/file"),
        )
        return portainer.StackFileResponse.model_validate(req.json())

    def start(self, stack_id: int, endpoint_id: int) -> portainer.Stack:
        """Start a stack https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackStart"""
        req = self.client.make_request(
            HttpMethod.POST,
            urljoin(self.client.base_url, f"{self._base_path}/{stack_id}/start"), params={"endpointId": endpoint_id}
        )
        return portainer.Stack.model_validate(req.json())
    
    def stop(self, stack_id: int, endpoint_id: int) -> portainer.Stack:
        """Stop a stack https://app.swaggerhub.com/apis/portainer/portainer-ce/2.19.4#/stacks/StackStop"""
        req = self.client.make_request(
            HttpMethod.POST,
            urljoin(self.client.base_url, f"{self._base_path}/{stack_id}/stop"), params={"endpointId": endpoint_id}
        )
        return portainer.Stack.model_validate(req.json())

class Status(APIResource):
    pass


class System(APIResource):
    def info(self) -> portainer.SystemInfoResponse:
        """Get system info"""
        info_req = self.client.make_request(HttpMethod.GET, urljoin(self.client.base_url, "api/system/info"))
        return portainer.SystemInfoResponse.model_validate(info_req.json())

    def version(self) -> portainer.SystemVersionResponse:
        """Get Portainer version"""
        info_req = self.client.make_request(HttpMethod.GET, urljoin(self.client.base_url, "api/system/version"))
        return portainer.SystemVersionResponse.model_validate(info_req.json())


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
