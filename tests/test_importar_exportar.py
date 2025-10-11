from decimal import Decimal, InvalidOperation
import glob
import os

import pytest

from editor_sped import EscrituracaoICMSIPI, EscrituracaoPISCOFINS, abrir_escrituracao
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


@pytest.mark.parametrize("arquivo", glob.glob("efd_icms_ipi_*.txt", root_dir="exemplos/"))
def test_icms_ipi(arquivo):
    escrituracao_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    escrituracao = EscrituracaoICMSIPI(escrituracao_texto)

    resultado = escrituracao.texto()

    comparar_escrituracoes(escrituracao_texto, resultado, "efd_icms_ipi")



@pytest.mark.parametrize("arquivo", glob.glob("efd_pis_cofins_*.txt", root_dir="exemplos/"))
def test_pis_cofins(arquivo):
    escrituracao_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    escrituracao = EscrituracaoPISCOFINS(escrituracao_texto)

    resultado = escrituracao.texto()

    comparar_escrituracoes(escrituracao_texto, resultado, "efd_pis_cofins")
