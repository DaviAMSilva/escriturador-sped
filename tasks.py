# pylint: disable=import-outside-toplevel,unused-argument,import-error

import importlib.resources
import json
import os
import shutil

from invoke.context import Context
from invoke.tasks import task


# Redefinindo MODULES do sped-extractor com os dados presentes em data/modules.json
from sped_extractor.spedextractor.constants import MODULES

with open(os.path.join("data", "modules.json"), "r", encoding="utf-8") as modules_json:
    modules_data = json.load(modules_json, object_hook=lambda d: {k: tuple(v) for k, v in d.items()})

    MODULES.clear()
    MODULES.update(modules_data)


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
def install(c: Context, dev: bool = True, jupyter: bool = False):
    cmd = [PYTHON, "-m", "pip", "install", "-e", "."]
    extras = []

    if dev:
        extras.append("DEV")

    if jupyter:
        extras.append("JUPYTER")

    if extras:
        cmd[-1] = f".[{','.join(extras)}]"

    c.run(" ".join(cmd))



@task
def se_install(c: Context):
    if not os.path.exists("sped_extractor"):
        c.run("git clone https://github.com/akretion/sped-extractor.git sped_extractor")

    c.run(f"{PYTHON} -m pip install requests")  # Requerimento não declarado no sped-extractor
    c.run(f"{PYTHON} -m pip install -e sped_extractor")


@task
def se_download(c: Context):
    from sped_extractor.spedextractor.download import main

    if main.callback:
        main.callback("")


@task
def se_extract(c: Context):
    from sped_extractor.spedextractor.extract_tables import main

    if main.callback:
        main.callback("", 0, 10)


@task
def se_patch(c: Context):
    for tipo in ("efd_icms_ipi", "efd_pis_cofins"):
        resource = importlib.resources.files("sped_extractor") / "spedextractor" / "specs" / tipo / str(modules_data[tipo][0]) / "camelot_patch"
        with importlib.resources.as_file(resource) as pasta:
            os.makedirs(os.path.join(pasta), exist_ok=True)

            origem = os.path.join(os.path.dirname(__file__), "data", "patches", f"{tipo}.csv")
            destino = os.path.join(pasta, "camelot_patch.csv")
            shutil.copy(origem, destino)


@task
def se_build(c: Context, patch: bool = True):
    from sped_extractor.spedextractor.build_csv import main

    if main.callback:
        main.callback(patch)


@task
def se_copy(c: Context):
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

    for tipo in ("efd_icms_ipi", "efd_pis_cofins"):
        os.makedirs(os.path.join(os.path.dirname(__file__), "data", tipo), exist_ok=True)

        for arquivo_nome in "accurate_fields.csv", "registers.csv", f"{tipo}.pdf":
            resource = importlib.resources.files("sped_extractor") / "spedextractor" / "specs" / tipo / str(modules_data[tipo][0]) / arquivo_nome
            with importlib.resources.as_file(resource) as origem:
                destino = os.path.join(os.path.dirname(__file__), "data", tipo, arquivo_nome)
                shutil.copy(origem, destino)


@task
def conversor(c: Context, formatado: bool = False):
    from data.conversor import main
    main(formatado)
    shutil.copy(os.path.join("data", "modules.json"), os.path.join("src", "editor_sped", "data", "modules.json"))


@task
def build(c: Context):
    se_download(c)
    se_extract(c)
    se_patch(c)
    se_build(c)
    se_copy(c)
    conversor(c)


@task
def all(c: Context):  # pylint: disable=redefined-builtin
    install(c)
    se_install(c)
    build(c)


@task
def lint(c: Context):
    c.run(f"{PYTHON} -m pylint src tests tasks.py data/conversor.py")


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
