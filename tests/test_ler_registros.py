import glob

import pytest

from editor_sped import EFD_TIPOS, Registro


@pytest.mark.parametrize("arquivo", glob.glob("efd_*.txt", root_dir="exemplos/"))
def test_ler_registros(textos_todos: dict[str, str], arquivo: str):
    registros_texto = textos_todos[arquivo]

    if "efd_icms_ipi" in arquivo:
        registros = Registro.ler(registros_texto, "efd_icms_ipi")
    elif "efd_pis_cofins" in arquivo:
        registros = Registro.ler(registros_texto, "efd_pis_cofins")
    else:
        raise FileExistsError(f"Arquivo inválido: {arquivo}")


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

    assert primeiro_registro.contem_filhos
    assert isinstance(primeiro_registro.filhos, list)
    assert isinstance(primeiro_registro.campos, tuple)

    if primeiro_registro.contem_filhos:
        assert primeiro_registro.tamanho > 1 and len(primeiro_registro.filhos) > 0
    else:
        assert primeiro_registro.tamanho == 1 and len(primeiro_registro.filhos) == 0



def test_ler_registros_vazio():
    registros_vazio1 = Registro.ler("", "efd_icms_ipi")
    registros_vazio2 = Registro.ler("", "efd_pis_cofins")

    assert isinstance(registros_vazio1, list)
    assert isinstance(registros_vazio2, list)
    assert len(registros_vazio1) == 0
    assert len(registros_vazio2) == 0



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
