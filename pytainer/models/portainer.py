from pydantic import BaseModel
from pytainer.models import gittypes

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

class Pair(BaseModel):
    name: str
    value: str

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
    gitConfig: gittypes.RepoConfig
    isComposeFormat: bool
    namespace: str
    projectPath: str
    updateDate: int
    updatedBy: str