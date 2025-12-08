from decimal import Decimal

import pytest

from editor_sped.classes.campo import Campo
from editor_sped.classes.registro import Registro


def test_campo_atribuicao():
    # fmt: off
    casos_de_teste = [
        # Registro,         Campo, Valor,              Interno_c,    Interno_n,             Externo_c,    Externo_n
        ("|9999||",         1,     None,               "",           None,                  "",           None),
        ("|9999||",         1,     "ABCD",             "ABCD",       None,                  "ABCD",       None),
        ("|9999||",         1,     "ABCDE",            "ABCD",       None,                  "ABCD",       None),
        ("|9999||",         1,     "ABC",              "ABC",        None,                  "ABC",        None),
        ("|9999||",         1,     777,                "777",        None,                  "777",        None),
        ("|9999||",         2,     None,               "",           None,                  "",           None),
        ("|9999||",         2,     123,                "123",        Decimal("123"),        "123",        123),
        ("|9999||",         2,     123.49,             "123",        Decimal("123"),        "123",        123),
        ("|9999||",         2,     123.50,             "124",        Decimal("124"),        "124",        124),
        ("|9999||",         2,     "123.49",           "123",        Decimal("123"),        "123",        123),
        ("|9999||",         2,     "123.50",           "124",        Decimal("124"),        "124",        124),
        ("|G110||||||||||", 2,     "30112025",         "30112025",   Decimal("30112025"),   "30112025",   30112025),
        ("|G110||||||||||", 2,     "01112025",         "01112025",   Decimal("01112025"),   "01112025",   1_112025),
        ("|G110||||||||||", 2,     30112025,           "30112025",   Decimal("30112025"),   "30112025",   30112025),
        ("|G110||||||||||", 2,     1_112025,           "01112025",   Decimal("01112025"),   "01112025",   1_112025),
        ("|G110||||||||||", 8,     22/7,               "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
        ("|G110||||||||||", 8,     "3,14285714285714", "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
        ("|G110||||||||||", 8,     "3.14285714285714", "3,14285714", Decimal("3.14285714"), "3,14285714", 3.14285714),
    ]
    # fmt: on

    for registro, campo, valor, interno_c, interno_n, externo_c, externo_n in casos_de_teste:
        r = Registro(registro, "efd_icms_ipi")

        c = Campo(None, campo, r, "efd_icms_ipi")

        c.valor = valor

        # pylint: disable=protected-access
        assert c._valor_alfanumerico == interno_c
        assert c._valor_numerico == interno_n
        assert c.valor_c == externo_c
        assert c.valor_n == externo_n

    r = Registro("|9999||", "efd_icms_ipi")
    c1 = Campo(None, 2, r, "efd_icms_ipi")
    c2 = Campo(None, 2, r, "efd_icms_ipi")

    with pytest.raises(ValueError):
        c1.valor = True  # type: ignore

    with pytest.raises(TypeError):
        c1.valor = [0]  # type: ignore

    with pytest.raises(ValueError):
        c2.valor = True  # type: ignore

    with pytest.raises(TypeError):
        c2.valor = [0]  # type: ignore


def test_campo_erro():
    r = Registro("|9999||", "efd_icms_ipi")
    c = Campo(None, 2, r, "efd_icms_ipi")


    with pytest.raises(TypeError, match="não é uma função"):
        c.configurar_valor(10)  # type: ignore

    with pytest.raises(TypeError, match="não deve conter argumentos"):
        def f1(a: int):
            return a
        c.configurar_valor(f1)  # type: ignore

    with pytest.raises(TypeError, match="deve retornar str, int, float ou None"):
        def f2() -> list:
            return [10]
        c.configurar_valor(f2)  # type: ignore


    def f3() -> int:
        return 10

    c.configurar_valor(f3)

    assert c.valor_n == 10
