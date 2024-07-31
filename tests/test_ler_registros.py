import pytest

from editor_sped import ler_registros, abrir_escrituracao
from editor_sped.classes import Registro


# TODO: parametrize
def test_ler_registros():
    registros_texto = abrir_escrituracao("exemplos/efd_pis_cofins_1.txt")

    registros = ler_registros(registros_texto, "efd_pis_cofins")

    assert type(registros) == list
    assert len(registros) > 0
    assert type(registros[0]) == Registro
    assert\
        (    registros[0].contem_filhos and registros[0].tamanho >  1 and len(registros[0].filhos) >  0)\
        or\
        (not registros[0].contem_filhos and registros[0].tamanho == 1 and len(registros[0].filhos) == 0)
