from collections import defaultdict
from importlib.resources import as_file, files
from importlib.metadata import version

from .modulos import MODULOS_PADROES, ModuloT


print(f"Módulos disponíveis no Escriturador SPED ({version("escriturador_sped")}):")
print("* = Versão carregada por padrão")


modulos: dict[ModuloT, list[tuple[str, str]]] = defaultdict(list)
with as_file(files("escriturador_sped.modulos")) as modulos_raiz:
    for caminho in sorted(modulos_raiz.glob("*/*/*/")):
        modulo: ModuloT
        modulo, leiaute, versao = caminho.parts[-3:] # type: ignore
        modulos[modulo].append((leiaute, versao))


for modulo, leiautes_versoes in modulos.items():
    print(f"\n[{modulo}]")
    for leiaute, versao in leiautes_versoes:
        leiaute, versao = leiaute[1:], versao[1:].replace("_", ".")
        try:
            print("* " if MODULOS_PADROES[modulo] == (leiaute, versao) else "  ", end="")
            print(f"Leiaute: {leiaute} - Versão: {versao}")
        except KeyError:
            continue


print()
