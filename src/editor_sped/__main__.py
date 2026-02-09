import json
from importlib.resources import files

from . import __version__


with files("editor_sped.data").joinpath("modules.json").open("r", encoding="utf-8") as modules_arquivo:
    efd_info = json.loads(modules_arquivo.read())

    print(f"Módulos carregados no Editor de SPED ({__version__}):\n")

    for tipo in efd_info.keys():
        print(f"Módulo:  {tipo}")
        print(f"Versão:  {efd_info[tipo][3]}")
        print(f"Leiaute: {efd_info[tipo][0]}")
        print(f"Data:    {efd_info[tipo][1]}")
        print(f"Link:    {efd_info[tipo][2]}\n")
