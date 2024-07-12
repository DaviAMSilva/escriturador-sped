import json
from importlib.resources import files










with open(files("editor_sped.data").joinpath("efd_info.json"), newline="", encoding="utf-8") as __efd_info_arquivo:
    EFD_INFO = json.loads(__efd_info_arquivo.read())
