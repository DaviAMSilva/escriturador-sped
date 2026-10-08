# pylint: disable=missing-module-docstring,missing-function-docstring,import-outside-toplevel,unused-argument,import-error

import os

from invoke.context import Context
from invoke.tasks import task


# Mude para usar uma versão diferente (-u = unbuffered)
PYTHON = "python -u"


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
def tipagem(c: Context, lint: bool = True):  # pylint: disable=redefined-outer-name
    from scripts.tipagem import main
    main()

    if lint:
        c.run(f"{PYTHON} -m pylint src/escriturador_sped/modulos/**/*.py")


@task
def mkdocs_serve(c: Context):
    os.environ["IMAGING"] = "false" if os.name == "nt" else "true"
    c.run(f"{PYTHON} -m mkdocs serve")


@task
def build_docs(c: Context, formatado: bool = False):
    from scripts.docs import main
    main(formatado)


@task
def build(c: Context, sdist: bool = False, wheel: bool = False):
    c.run(f"{PYTHON} -m build{' --sdist' if sdist else ''}{' --wheel' if wheel else ''}")


@task
def lint(c: Context):
    c.run(f"{PYTHON} -m pylint --fail-under=9.8 src tests scripts tasks.py")


@task
def markdownlint(c: Context):
    c.run("markdownlint-cli2 **/*.md #venv $@")


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
    c.run(f"{PYTHON} -m snakeviz {arquivo}")
