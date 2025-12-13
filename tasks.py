# pylint: disable=import-outside-toplevel,unused-argument,import-error,no-value-for-parameter

import json
import os

import importlib.resources
import shutil

from invoke.context import Context
from invoke.tasks import task


def modules():
    with open(os.path.join("data", "modules.json"), "r", encoding="utf-8") as m:
        return json.load(m, object_hook=lambda d: {k: tuple(v) for k, v in d.items()})


@task
def venv(c: Context, python: str = "python"):
    if not os.path.exists("venv"):
        c.run(f"{python} -m venv venv")

    print("Ative o ambiente virtual com:")
    print(".\\venv\\Scripts\\activate" if os.name == "nt" else "source venv/bin/activate")


@task
def install(c: Context):
    c.run("pip install -e .[DEV]")


@task
def se_install(c: Context):
    if not os.path.exists("sped_extractor"):
        c.run("git clone https://github.com/akretion/sped-extractor.git sped_extractor")

    c.run("pip install requests")  # Requerimento não declarado no sped-extractor
    c.run("pip install -e sped_extractor")


@task
def se_download(c: Context):
    from sped_extractor.spedextractor.constants import MODULES
    from sped_extractor.spedextractor.download import main

    modules_data = modules()

    MODULES.clear()
    MODULES.update(modules_data)

    main([])  # type: ignore


@task
def se_extract(c: Context):
    from sped_extractor.spedextractor.constants import MODULES
    from sped_extractor.spedextractor.extract_tables import main

    modules_data = modules()

    MODULES.clear()
    MODULES.update(modules_data)

    main([])  # type: ignore


@task
def se_patch(c: Context):
    modules_data = modules()

    for tipo in ("efd_icms_ipi", "efd_pis_cofins"):
        resource = importlib.resources.files("sped_extractor") / "spedextractor" / "specs" / tipo / str(modules_data[tipo][0]) / "camelot_patch"
        with importlib.resources.as_file(resource) as pasta:
            os.makedirs(os.path.join(pasta), exist_ok=True)

            origem = os.path.join(os.path.dirname(__file__), "data", "patches", f"{tipo}.csv")
            destino = os.path.join(pasta, "camelot_patch.csv")
            shutil.copy(origem, destino)


@task
def se_build(c: Context):
    from sped_extractor.spedextractor.constants import MODULES
    from sped_extractor.spedextractor.build_csv import main

    modules_data = modules()

    MODULES.clear()
    MODULES.update(modules_data)

    main([])  # type: ignore


@task
def se_copy(c: Context):
    modules_data = modules()

    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

    for tipo in ("efd_icms_ipi", "efd_pis_cofins"):
        os.makedirs(os.path.join(os.path.dirname(__file__), "data", tipo), exist_ok=True)

        for arquivo_nome in "accurate_fields.csv", "registers.csv", f"{tipo}.pdf":
            resource = importlib.resources.files("sped_extractor") / "spedextractor" / "specs" / tipo / str(modules_data[tipo][0]) / arquivo_nome
            with importlib.resources.as_file(resource) as origem:
                destino = os.path.join(os.path.dirname(__file__), "data", tipo, arquivo_nome)
                shutil.copy(origem, destino)


@task
def conversor(c: Context, formatado=False):
    from data.conversor import main
    main(formatado)
    shutil.copy(os.path.join("data", "modules.json"), os.path.join("src", "editor_sped", "data", "modules.json"))


@task
def download(c: Context):
    se_download(c)


@task
def build(c: Context):
    # se_download(c) # Por algum motivo essa etapa interrompe todo o processo
    se_extract(c)
    se_patch(c)
    se_build(c)
    se_copy(c)
    conversor(c)


@task
def all(c: Context):  # pylint: disable=redefined-builtin
    venv(c)
    install(c)
    se_install(c)
    # download(c)
    build(c)
