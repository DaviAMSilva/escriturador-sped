# pylint: disable=import-outside-toplevel,unused-argument,import-error

import json
import os

from invoke.context import Context
from invoke.tasks import task




@task
def venv(c: Context, python: str = "python"):
    if not os.path.exists("venv"):
        c.run(f"{python} -m venv venv")

    activate(c)


@task
def activate(c: Context):
    if os.name == "nt":
        c.run("venv\\Scripts\\activate")
    else:
        c.run("source venv/bin/activate")


@task
def install(c: Context):
    c.run("pip install -e .[DEV]")


@task
def se_install(c: Context):
    if not os.path.exists("sped_extractor"):
        c.run("git clone https://github.com/akretion/sped-extractor.git sped_extractor")

    c.run("pip install requests") # Requerimento não declarado no sped-extractor
    c.run("pip install -e sped_extractor")


@task
def se_download(c: Context):
    from sped_extractor.spedextractor.constants import MODULES
    from sped_extractor.spedextractor.download import main

    with open("modules.json", "r", encoding="utf-8") as f:
        modules_data = json.load(f, object_hook=lambda d: {k: tuple(v) for k, v in d.items()})

    MODULES.clear()
    MODULES.update(modules_data)

    main([])


@task
def se_extract_tables(c: Context):
    from sped_extractor.spedextractor.constants import MODULES
    from sped_extractor.spedextractor.extract_tables import main

    with open("modules.json", "r", encoding="utf-8") as f:
        modules_data = json.load(f, object_hook=lambda d: {k: tuple(v) for k, v in d.items()})

    MODULES.clear()
    MODULES.update(modules_data)

    main([], None, None)
