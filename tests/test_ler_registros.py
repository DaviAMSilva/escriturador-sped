import glob

import pytest

from editor_sped import EFD_TIPOS, Registro
from editor_sped.constantes import EFD_ICMS_IPI, EFD_PIS_COFINS

from .cache import cache


@pytest.mark.parametrize("arquivo", glob.glob("efd_*.txt", root_dir="exemplos/"))
def test_ler_registros(arquivo: str):
    registros_texto = cache.texto(arquivo)

    if EFD_ICMS_IPI in arquivo:
        registros = Registro.ler(registros_texto, EFD_ICMS_IPI)
    elif EFD_PIS_COFINS in arquivo:
        registros = Registro.ler(registros_texto, EFD_PIS_COFINS)
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
    assert primeiro_registro.efd_tipo in EFD_TIPOS

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
        ("C100",       SyntaxError),
        ("C100|0|",    SyntaxError),
        ("|C100",      SyntaxError),
        ("C100|0",     SyntaxError),
        ("|ERRO|1|",   KeyError),
        ("|C100|0|",   SyntaxError),
        ("|0990|ABC|", ValueError),
    ]
    # fmt: on

    for tipo in EFD_TIPOS:
        for registros_texto, erro_esperado in casos_de_teste:
            with pytest.raises(erro_esperado):
                Registro.ler(registros_texto, tipo)
