import argparse
import json
import os
from collections import defaultdict
from importlib.resources import as_file, files
from typing import DefaultDict

from escriturador_sped import LeiauteT, ModuloT


def main(formatado: bool = False):
    modulos: DefaultDict[ModuloT, DefaultDict[str, dict[str, LeiauteT]]] = defaultdict(lambda: defaultdict(dict))

    with as_file(files("escriturador_sped.modulos")) as modulos_raiz:
        modulo: ModuloT
        for caminho in sorted(modulos_raiz.glob("*/*/*/")):
            modulo, leiaute, manual = caminho.parts[-3:]  # type: ignore
            leiaute, manual = leiaute[1:], manual[1:].replace("_", ".")

            with open(os.path.join(caminho, "modulo.json"), "r", encoding="utf-8") as f:
                modulos[modulo][leiaute][manual] = json.load(f)

    with open("docs/modulos/modulos.js", "w", encoding="utf-8") as f:
        f.write("const MODULOS=")
        json.dump(modulos, f, ensure_ascii=False, sort_keys=False, indent=4 if formatado else None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte os módulos SPED para o formato usado pela documentação")
    parser.add_argument("--formatado", action="store_true", help="Gera o arquivo com uma formatação ao invés de ser minimizado")
    args = parser.parse_args()

    main(args.formatado)
