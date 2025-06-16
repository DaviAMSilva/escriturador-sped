import json
from importlib.resources import files

from .types import EfdInfo










with files("editor_sped.data").joinpath("efd_info.json").open("r", encoding="utf-8") as __efd_info_arquivo:
    EFD_INFO: EfdInfo = json.loads(__efd_info_arquivo.read())
