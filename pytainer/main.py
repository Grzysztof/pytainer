import typer
import os
from pytainer import Pytainer

app = typer.Typer()
system_app = typer.Typer()

app.add_typer(system_app, name="system")

@system_app.command()
def info():
    portainer = Pytainer(base_url=os.getenv("PORTAINER_URL"), api_token=os.getenv("PORTAINER_API_TOKEN"))
    print(portainer.system.info())

if __name__ == "__main__":
    app()