# pylint: disable=import-outside-toplevel,unused-argument,import-error

import os

from invoke.context import Context
from invoke.tasks import task


# Mude para usar uma versão diferente
PYTHON = "python"


@task
def venv(c: Context, python: str = PYTHON, pasta: str = "venv"):
    if not os.path.exists(f"{pasta}"):
        c.run(f"{python} -m venv {pasta}")

    print("Ative o ambiente virtual com:")
    if os.name == "nt":
        if "PSModulePath" in os.environ and os.environ.get("PROMPT", "") != "$P$G":
            print(f"& .\\{pasta}\\Scripts\\Activate.ps1")  # Windows PowerShell
        else:
            print(f".\\{pasta}\\Scripts\\activate.bat")  # Windows Command Prompt
    else:
        print(f"source {pasta}/bin/activate")  # Linux / MacOS


@task
def install(c: Context, dev: bool = True):
    c.run(f"{PYTHON} -m pip install -e {'.[DEV]' if dev else '.'}")


@task
def conversor(c: Context, formatado: bool = False):
    from scripts.conversor import main
    main(formatado)


@task
def tipagem(c: Context):
    from scripts.tipagem import main
    main()


@task
def build(c: Context):
    conversor(c)
    tipagem(c)


@task
def all(c: Context):  # pylint: disable=redefined-builtin
    install(c)
    build(c)


@task
def lint(c: Context):
    c.run(f"{PYTHON} -m pylint --fail-under=9.8 src tests scripts tasks.py")


@task
def test(c: Context, coverage: bool = False, profile: bool = False, profile_svg: bool = False):
    cmd = [f"{PYTHON} -m pytest", "tests", "--pstats-dir", ".prof"]

    if coverage:
        cmd += ["--cov=src", "--cov-report=term-missing"]

    if profile:
        cmd += ["--profile"]

    if profile_svg:
        cmd += ["--profile-svg"]

    c.run(" ".join(cmd))


@task
def snakeviz(c: Context, arquivo: str = ".prof/combined.prof"):
    c.run(f"snakeviz {arquivo}")
