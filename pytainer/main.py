import typer

app = typer.Typer()


@app.command()
def login(username: str, password: str):
    typer.echo(f"Logging in as: {username}")
