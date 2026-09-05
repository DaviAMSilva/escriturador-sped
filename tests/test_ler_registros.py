import glob

import pytest

from escriturador_sped import MODULOS_NOMES, Registro
from escriturador_sped.constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI

from .cache import cache


@pytest.mark.parametrize("arquivo", glob.glob("*.txt", root_dir="exemplos/"))
def test_ler_registros(arquivo: str):
    registros_texto = cache.texto(arquivo)

    if ECD in arquivo:
        registros = Registro.ler(registros_texto, ECD)
    elif ECF in arquivo:
        registros = Registro.ler(registros_texto, ECF)
    elif EFD_CONTRIBUICOES in arquivo:
        registros = Registro.ler(registros_texto, EFD_CONTRIBUICOES)
    elif EFD_ICMS_IPI in arquivo:
        registros = Registro.ler(registros_texto, EFD_ICMS_IPI)
    else:
        raise ValueError(f"Arquivo inválido: {arquivo}")


    assert isinstance(registros, list)
    assert len(registros) > 0

    primeiro_registro = registros[0]

    assert isinstance(primeiro_registro, Registro)
    assert primeiro_registro.pai is None

    assert isinstance(primeiro_registro.linha, str)
    assert isinstance(primeiro_registro.texto(), str)

    assert isinstance(primeiro_registro.nome, str)
    assert isinstance(primeiro_registro.descricao, str)
    assert primeiro_registro.modulo in MODULOS_NOMES

    assert primeiro_registro.filhos
    assert isinstance(primeiro_registro.filhos, list)
    assert isinstance(primeiro_registro.campos, tuple)

    if primeiro_registro.filhos:
        assert primeiro_registro.tamanho > 1 and len(primeiro_registro.filhos) > 0
    else:
        assert primeiro_registro.tamanho == 1 and len(primeiro_registro.filhos) == 0



def test_ler_registros_vazio():
    valores_teste = ("", None, [""], [None])

    for valor_teste in valores_teste:
        with pytest.raises(TypeError):
            Registro.ler(valor_teste, EFD_ICMS_IPI)  # type: ignore



def test_ler_registros_erro():
    # fmt: off
    casos_de_teste = [
        ("|",          SyntaxError),
        ("||",         SyntaxError),
        ("|||",        KeyError),
        ("0000",       SyntaxError),
        ("0000|0|",    SyntaxError),
        ("|0000",      SyntaxError),
        ("0000|0",     SyntaxError),
        ("|ERRO|1|",   KeyError),
        ("|0000|0|",   SyntaxError),
        ("|0990|ABC|", ValueError),
    ]
    # fmt: on

    for tipo in MODULOS_NOMES:
        for registros_texto, erro_esperado in casos_de_teste:
            with pytest.raises(erro_esperado):
                Registro.ler(registros_texto, tipo)
