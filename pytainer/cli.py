import typer
import os
from typing import Annotated, List, Optional
from pytainer import Pytainer
from pytainer.models.portainer import UpdateSwarmStackPayload, Pair
from rich import print

app = typer.Typer()
system_app = typer.Typer(help="System commands")
stacks_app = typer.Typer(help="Stacks control commands")

app.add_typer(system_app, name="system")
app.add_typer(stacks_app, name="stacks")

client = Pytainer()


@system_app.command("info")
def info():
    print(client.system.info())


@system_app.command("version")
def version():
    print(client.system.version())


@stacks_app.command("list")
def list_stack():
    print(client.stacks.list())


@stacks_app.command("get")
def get_stack(
    stack_id: Annotated[int, typer.Argument(...)],
):
    print(client.stacks.get(stack_id=stack_id))


@stacks_app.command("update")
def update_stack(
    stack_id: Annotated[int, typer.Argument(...)],
    env: Annotated[Optional[List[str]], typer.Option("--env")] = None,
    prune: Annotated[bool, typer.Option("--prune")] = False,
    pull_image: Annotated[bool, typer.Option("--pull")] = False,
):
    parsed_env = []
    if env:
        for item in env:
            key, value = item.split("=")
            parsed_env.append(Pair(name=key, value=value))

    current_stack = client.stacks.get(stack_id=stack_id)
    current_stack_file = client.stacks.get_file(stack_id=stack_id)

    if current_stack:
        # compare current stack env with parsed env and update with changed values
        # TODO: Not sure about shallow copy in pydantic models
        updated_envs: List[Pair] = current_stack.Env.copy()
        for item in parsed_env:
            for i, env in enumerate(updated_envs):
                if env.name == item.name:
                    updated_envs[i].value = item.value
                else:
                    updated_envs.append(item)

        data = UpdateSwarmStackPayload(
            env=updated_envs,
            prune=prune,
            pullImage=pull_image,
            stackFileContent=current_stack_file.StackFileContent,
        )
        response = client.stacks.update(
            stack_id=stack_id, endpoint_id=current_stack.EndpointId, data=data
        )
        return response

@stacks_app.command("start")
def satrt_stack(
    stack_id: Annotated[int, typer.Argument(...)],
    endpoint_id: Annotated[int, typer.Option("--endpoint")] = None,
):  
    if not endpoint_id:
        endpoint_id = client.stacks.get(stack_id=stack_id).EndpointId
    response = client.stacks.start(stack_id=stack_id, endpoint_id=endpoint_id)    
    return response

@stacks_app.command("stop")
def satrt_stack(
    stack_id: Annotated[int, typer.Argument(...)],
    endpoint_id: Annotated[int, typer.Option("--endpoint")] = None,
):  
    if not endpoint_id:
        endpoint_id = client.stacks.get(stack_id=stack_id).EndpointId

    response = client.stacks.stop(stack_id=stack_id, endpoint_id=endpoint_id)    
    return response


def main():
    app()


if __name__ == "__main__":
    main()
