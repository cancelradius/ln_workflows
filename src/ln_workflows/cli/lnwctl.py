import typer
from ln_workflows.orch.control import ControlPlane

app = typer.Typer()

@app.callback()
def callback(): ...

@app.command()
def start():
    ctl = ControlPlane()

