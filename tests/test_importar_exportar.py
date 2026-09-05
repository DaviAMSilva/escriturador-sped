import glob
from typing import assert_never

import pytest

from escriturador_sped import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI, MODULOS, Campo, ModuloT

from .cache import cache


def comparar_escrituracoes(texto1: str, texto2: str, modulo: ModuloT):
    lines1 = texto1.splitlines()
    lines2 = texto2.splitlines()

    assert len(lines1) == len(lines2)

    # Compara escriturações não apenas pelo texto, mas sim pelos valores
    for line1, line2 in zip(lines1, lines2):
        campos1 = line1.split("|")[1:-1]
        campos2 = line2.split("|")[1:-1]

        nome1 = campos1[0]
        nome2 = campos2[0]

        assert nome1 == nome2
        assert len(campos1) == len(campos2)

        comparar_campos(modulo, campos1, campos2, nome1, nome2)


def comparar_campos(modulo: ModuloT, campos1: list[str], campos2: list[str], nome1: str, nome2: str):
    for i, (campo1, campo2) in enumerate(zip(campos1, campos2)):
        try:
            tipo1 = MODULOS[modulo]["registros"][nome1]["campos"][i]["tipo"]
            tipo2 = MODULOS[modulo]["registros"][nome2]["campos"][i]["tipo"]
        except IndexError:
            tipo1, tipo2 = "C", "C"

        assert tipo1 == tipo2

        if tipo1 == Campo.NUMERICO:
            # Campos vazios estão OK
            if campo1 == "" and campo2 == "":
                continue

            try:
                valor1 = float(campo1.replace(",", "."))
                valor2 = float(campo2.replace(",", "."))

                # Valor numérico
                assert valor1 == valor2

                # Valor numérico com tamanho exato
                if MODULOS[modulo]["registros"][nome1]["campos"][i]["tamanho_exato"]:
                    assert campo1 == campo2
            except ValueError as e:
                raise ValueError("Não foi possível converter para float") from e
        elif tipo1 == Campo.ALFANUMERICO:
            # Valor alfanumérico
            assert campo1 == campo2
        else:
            assert_never(tipo1)


@pytest.mark.parametrize("arquivo", glob.glob("*.txt", root_dir="exemplos/"))
def test_importar_exportar(arquivo: str):
    escrituracao_texto = cache.texto(arquivo)
    escrituracao = cache.escrituracao(arquivo)

    escrituracao.totalizar()
    resultado = escrituracao.texto()

    if ECD in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, ECD)
    elif ECF in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, ECF)
    elif EFD_ICMS_IPI in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, EFD_ICMS_IPI)
    elif EFD_CONTRIBUICOES in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, EFD_CONTRIBUICOES)
    else:
        raise ValueError(f"Arquivo inválido: {arquivo}")
