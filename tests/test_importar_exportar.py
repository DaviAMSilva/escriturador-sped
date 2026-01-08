import glob
from decimal import Decimal, InvalidOperation

import pytest

from editor_sped import EFD_ICMS_IPI, EFD_INFO, EFD_PIS_COFINS, Campo, EfdTipo

from .cache import cache


def comparar_escrituracoes(texto1: str, texto2: str, efd_tipo: EfdTipo):
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

        comparar_campos(efd_tipo, campos1, campos2, nome1, nome2)


def comparar_campos(efd_tipo: EfdTipo, campos1: list[str], campos2: list[str], nome1: str, nome2: str):
    for i, (campo1, campo2) in enumerate(zip(campos1, campos2)):
        tipo1 = EFD_INFO[efd_tipo]["registros"][nome1]["campos"][i]["tipo"]
        tipo2 = EFD_INFO[efd_tipo]["registros"][nome2]["campos"][i]["tipo"]

        assert tipo1 == tipo2

        if tipo1 == Campo.NUMERICO:
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
        elif tipo1 == Campo.ALFANUMERICO:
            # Valor alfanumérico
            assert campo1 == campo2
        else:
            raise ValueError(f"Tipo de campo desconhecido: {tipo1}")


@pytest.mark.parametrize("arquivo", glob.glob("efd_*.txt", root_dir="exemplos/"))
def test_importar_exportar(arquivo: str):
    escrituracao_texto = cache.texto(arquivo)
    escrituracao = cache.escrituracao(arquivo)

    escrituracao.totalizar()
    resultado = escrituracao.texto()

    if EFD_ICMS_IPI in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, EFD_ICMS_IPI)
    elif EFD_PIS_COFINS in arquivo:
        comparar_escrituracoes(escrituracao_texto, resultado, EFD_PIS_COFINS)
    else:
        raise ValueError(f"Arquivo inválido: {arquivo}")
