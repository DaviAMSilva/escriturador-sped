from collections import defaultdict
from importlib.resources import as_file, files

from editor_sped.efd_info import EfdTipo
from editor_sped.modulos import MODULOS_PADROES

from . import __version__


print(f"Módulos disponíveis no Editor de SPED ({__version__}):")
print("* = Versão carregada por padrão")


modulos: dict[EfdTipo, list[tuple[str, str]]] = defaultdict(list)
with as_file(files("editor_sped").joinpath("modulos")) as modulos_raiz:
    for caminho in sorted(modulos_raiz.glob("*/*/*/")):
        efd: EfdTipo
        efd, leiaute, versao = caminho.parts[-3:] # type: ignore
        modulos[efd].append((leiaute, versao))


for modulo, leiautes_versoes in modulos.items():
    print(f"\n[{modulo}]")
    for leiaute, versao in leiautes_versoes:
        print("* " if MODULOS_PADROES[modulo] == (leiaute, versao) else "  ", end="")
        print(f"Leiaute: {leiaute} - Versão: {versao}")


print()
