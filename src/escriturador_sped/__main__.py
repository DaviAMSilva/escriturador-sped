from collections import defaultdict
from importlib.resources import as_file, files
from importlib.metadata import version

from .modulos import MODULOS_PADROES, ModuloT


print(f"Módulos disponíveis no Escriturador SPED (v{version("escriturador_sped")}):")
print("* = Manual carregada por padrão")


modulos: dict[ModuloT, list[tuple[str, str]]] = defaultdict(list)
with as_file(files("escriturador_sped.modulos")) as modulos_raiz:
    for caminho in sorted(modulos_raiz.glob("*/*/*/")):
        modulo: ModuloT
        modulo, leiaute, manual = caminho.parts[-3:] # type: ignore
        modulos[modulo].append((leiaute[1:], manual[1:].replace("_", ".")))


for modulo, leiautes_versoes in modulos.items():
    print(f"\n[{modulo}]")
    for leiaute, manual in leiautes_versoes:
        try:
            print("* " if MODULOS_PADROES[modulo] == (leiaute, manual) else "  ", end="")
            print(f"Leiaute: {leiaute} - Manual: {manual}")
        except KeyError:
            continue


print()
