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
            modulo, leiaute, versao = caminho.parts[-3:]  # type: ignore
            leiaute, versao = leiaute[1:], versao[1:].replace("_", ".")

            with open(os.path.join(caminho, "leiaute.json"), "r", encoding="utf-8") as f:
                modulos[modulo][leiaute][versao] = json.load(f)

    with open("docs/modulos/modulos.js", "w", encoding="utf-8") as f:
        f.write("const MODULOS=")
        json.dump(modulos, f, ensure_ascii=False, sort_keys=False, indent=4 if formatado else None)


if __name__ == "__main__":
    main()
