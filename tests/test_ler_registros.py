import glob
import os

import pytest

from editor_sped import Registro, abrir_escrituracao, ler_registros


@pytest.mark.parametrize("arquivo", glob.glob("efd_pis_cofins_*.txt", root_dir="exemplos/"))
def test_ler_registros(arquivo):
    registros_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    registros = ler_registros(registros_texto, "efd_pis_cofins")

    assert isinstance(registros, list)
    assert len(registros) > 0
    assert isinstance(registros[0], Registro)
    assert\
        (    registros[0].contem_filhos and registros[0].tamanho >  1 and len(registros[0].filhos) >  0)\
        or\
        (not registros[0].contem_filhos and registros[0].tamanho == 1 and len(registros[0].filhos) == 0)



def test_ler_registros_vazio():
    registros_vazio1 = ler_registros("", "efd_icms_ipi")
    registros_vazio2 = ler_registros("", "efd_pis_cofins")

    assert isinstance(registros_vazio1, list)
    assert isinstance(registros_vazio1, list)
    assert len(registros_vazio2) == 0
    assert len(registros_vazio2) == 0
