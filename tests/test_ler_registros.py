import glob
import os

import pytest

from editor_sped import EFD_TIPOS, Registro, abrir_escrituracao, ler_registros


@pytest.mark.parametrize("arquivo", glob.glob("efd_pis_cofins_*.txt", root_dir="exemplos/"))
def test_ler_registros(arquivo):
    registros_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    registros = ler_registros(registros_texto, "efd_pis_cofins")

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

    assert\
        (    primeiro_registro.contem_filhos and primeiro_registro.tamanho >  1 and len(primeiro_registro.filhos) >  0)\
        or\
        (not primeiro_registro.contem_filhos and primeiro_registro.tamanho == 1 and len(primeiro_registro.filhos) == 0)



def test_ler_registros_vazio():
    registros_vazio1 = ler_registros("", "efd_icms_ipi")
    registros_vazio2 = ler_registros("", "efd_pis_cofins")

    assert isinstance(registros_vazio1, list)
    assert isinstance(registros_vazio2, list)
    assert len(registros_vazio1) == 0
    assert len(registros_vazio2) == 0
