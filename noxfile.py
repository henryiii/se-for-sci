import nox
from pathlib import Path

nox.needs_version = ">=2022.1.7"
DIR = Path(__file__).parent.resolve()


@nox.session(reuse_venv=True)
def pyodide(session: nox.Session) -> None:
    session.install("jupyterlite[lab]")
    session.run("jupyter", "lite", "init")
    session.run("jupyter", "lite", "build", "--contents=content")

    if "--serve" in session.posargs:
        session.run("jupyter", "lite", "serve")
