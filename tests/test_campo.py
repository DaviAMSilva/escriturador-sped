from decimal import Decimal

import pytest

from editor_sped import Campo
from editor_sped import EFD_ICMS_IPI


def test_campo_atribuicao():
    # fmt: off
    casos_de_teste = [
        # Registro, Campo, Valor,              Interno_c,    Interno_n,             Externo_c,    Externo_n
        ("9999",    1,     None,               "",           None,                  "",           None),
        ("9999",    1,     "ABCD",             "ABCD",       None,                  "ABCD",       None),
        ("9999",    1,     "ABCDE",            "ABCD",       None,                  "ABCD",       None),
        ("9999",    1,     "ABC",              "ABC",        None,                  "ABC",        None),
        ("9999",    1,     777,                "777",        None,                  "777",        None),
        ("9999",    2,     None,               "",           None,                  "",           None),
        ("9999",    2,     123,                "123",        Decimal("123"),        "123",        123),
        ("9999",    2,     123.49,             "123",        Decimal("123"),        "123",        123),
        ("9999",    2,     123.50,             "124",        Decimal("124"),        "124",        124),
        ("9999",    2,     "123.49",           "123",        Decimal("123"),        "123",        123),
        ("9999",    2,     "123.50",           "124",        Decimal("124"),        "124",        124),
        ("G110",    2,     "30112025",         "30112025",   Decimal("30112025"),   "30112025",   30112025),
        ("G110",    2,     "01112025",         "01112025",   Decimal("01112025"),   "01112025",   1_112025),
        ("G110",    2,     30112025,           "30112025",   Decimal("30112025"),   "30112025",   30112025),
        ("G110",    2,     1_112025,           "01112025",   Decimal("01112025"),   "01112025",   1_112025),
        ("G110",    8,     22/7,               "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
        ("G110",    8,     "3,14285714285714", "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
        ("G110",    8,     "3.14285714285714", "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
    ]
    # fmt: on

    for registro_nome, numero_campo, valor, interno_c, interno_n, externo_c, externo_n in casos_de_teste:
        c = Campo(None, registro_nome, numero_campo, EFD_ICMS_IPI)

        c.valor = valor

        # pylint: disable=protected-access
        assert c._valor_alfanumerico == interno_c
        assert c._valor_numerico == interno_n
        assert c.valor_c == externo_c
        assert c.valor_n == externo_n



def test_campo_erro():
    c1 = Campo(None, "9999", 1, EFD_ICMS_IPI)
    c2 = Campo(None, "9999", 2, EFD_ICMS_IPI)


    c1.valor = True
    assert c1.valor_c == "True"
    assert c1.valor_n is None

    with pytest.raises(TypeError):
        c1.valor = ["0"]  # type: ignore


    c2.valor = 10
    assert c2.valor_n == 10
    assert c2.valor_c == "10"

    with pytest.raises(ValueError):
        c2.valor = True  # type: ignore

    with pytest.raises(ValueError):
        c2.valor = "str"  # type: ignore

    with pytest.raises(TypeError):
        c2.valor = [0]  # type: ignore
