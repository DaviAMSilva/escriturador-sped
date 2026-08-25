import os
from glob import glob
from pathlib import Path

from editor_sped import EFD_ICMS_IPI, EFD_PIS_COFINS, MODULOS, ModuloT


MODULOS_CLASSES = {
    EFD_ICMS_IPI: "EfdIcmsIpi",
    EFD_PIS_COFINS: "EfdPisCofins"
}


def main():
    for caminho in glob("*/*/*/", root_dir="modulos"):
        modulo: ModuloT
        modulo, leiaute, versao = Path(caminho).parts  # type: ignore

        arquivo_conteudo = (
            "# pylint: disable=relative-beyond-top-level,duplicate-code,non-ascii-name,too-many-lines\n"
            "from .....classes.campo import CampoC, CampoN\n"
            f"from .....classes.registro import Registro{MODULOS_CLASSES[modulo]}\n"
        )

        for nome_registro, info_registro in MODULOS[modulo]["registros"].items():
            # Cabeçalho da classe
            arquivo_conteudo += (
                f"\n\nclass Registro{nome_registro}(Registro{MODULOS_CLASSES[modulo]}):\n"
                f"    nome = \"{nome_registro}\"\n"
            )

            for campo in info_registro["campos"]:
                # Hifens ('-') em nomes de campos serão substituídos por dois underlines ('__')
                arquivo_conteudo += f"    {campo['nome'].replace('-', '__')}: Campo{campo['tipo']}\n"

        pasta_destino = os.path.join("src", "editor_sped", "modulos", modulo, f"l{leiaute}", f"v{versao.replace('.', '_')}")

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        with open(os.path.join(pasta_destino, "registros.py"), "w", encoding="utf-8") as arquivo_tipagem:
            arquivo_tipagem.write(arquivo_conteudo)


if __name__ == "__main__":
    main()
