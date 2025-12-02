import glob
from decimal import Decimal, InvalidOperation

import pytest

from editor_sped.classes.escrituracao import Escrituracao
from editor_sped.tabelas import EFD_INFO
from editor_sped.types import EfdTipo


def comparar_escrituracoes(texto1: str, texto2: str, efd_tipo: EfdTipo):
    lines1 = texto1.splitlines()
    lines2 = texto2.splitlines()

    assert len(lines1) == len(lines2)

    # Compara escriturações não apenas pelo texto, mas sim pelos valores
    for line1, line2 in zip(lines1, lines2):
        campos1 = line1.split("|")[1:-2]
        campos2 = line2.split("|")[1:-2]

        registro1 = campos1[0]
        registro2 = campos2[0]

        assert registro1 == registro2
        assert len(campos1) == len(campos2)

        for i, (campo1, campo2) in enumerate(zip(campos1, campos2)):
            tipo1 = EFD_INFO[efd_tipo]["registros"][registro1]["campos"][i]["tipo"]
            tipo2 = EFD_INFO[efd_tipo]["registros"][registro2]["campos"][i]["tipo"]

            assert tipo1 == tipo2

            if tipo1 == "N":
                # Campos vazios estão OK
                if campo1 == "" and campo2 == "":
                    continue

                try:
                    valor1 = Decimal(campo1.replace(",", "."))
                    valor2 = Decimal(campo2.replace(",", "."))

                    # Valor numérico
                    assert valor1 == valor2
                except InvalidOperation as e:
                    raise ValueError("Não foi possível converter para decimal") from e
            elif tipo1 == "C":
                # Valor alfanumérico
                assert campo1 == campo2
            else:
                raise ValueError(f"Tipo de campo desconhecido: {tipo1}")


@pytest.mark.parametrize("arquivo", glob.glob("efd_*.txt", root_dir="exemplos/"))
def test_importar_exportar(textos_todos: dict[str, str], escrituracoes_todas: dict[str, Escrituracao], arquivo: str):
    escrituracao_texto = textos_todos[arquivo]
    escrituracao = escrituracoes_todas[arquivo]

    escrituracao.recalcular_9900()
    resultado = escrituracao.texto()

    if "efd_icms_ipi" in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, "efd_icms_ipi")
    elif "efd_pis_cofins" in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, "efd_pis_cofins")
    else:
        raise FileExistsError(f"Arquivo inválido: {arquivo}")
