import pytest

from editor_sped import EFD_ICMS_IPI, Campo


def test_campo_atribuicao():
    # fmt: off
    casos_de_teste = [
        # Registro, Campo, Valor,              Valor_c,      Valor_n,
        ("9999",    1,     None,               "",           None),
        ("9999",    1,     "ABCD",             "ABCD",       None),
        ("9999",    1,     "ABCDE",            "ABCD",       None),
        ("9999",    1,     "ABC",              "ABC",        None),
        ("9999",    1,     777,                "777",        None),
        ("9999",    2,     None,               "",           None),
        ("9999",    2,     123,                "123",        123),
        ("G110",    2,     "30112025",         "30112025",   30112025),
        ("G110",    2,     "01112025",         "01112025",    1112025),
        ("G110",    2,     30112025,           "30112025",   30112025),
        ("G110",    2,      1112025,           "01112025",    1112025),
        ("G110",    8,     22/7,               "3,14285714", 3.14285714),
        ("G110",    8,     "3,14285714285714", "3,14285714", 3.14285714),
        ("G110",    8,     "3.14285714285714", "3,14285714", 3.14285714),
    ]
    # fmt: on

    for nome_registro, numero_campo, valor, valor_c, valor_n in casos_de_teste:
        c = Campo(EFD_ICMS_IPI, nome_registro, numero_campo, None)

        c.valor = valor

        assert c.valor == (valor_c if c.tipo == "C" else valor_n if c.tipo == "N" else float("inf"))

        assert c.valor_c == valor_c
        assert c.valor_n == valor_n



def test_campo_erro():
    c1 = Campo(EFD_ICMS_IPI, "9999", 1, None)
    c2 = Campo(EFD_ICMS_IPI, "9999", 2, None)


    c1.valor = True
    assert c1.valor_c == "True"
    assert c1.valor_n is None

    with pytest.raises(TypeError):
        c1.valor = ["0"]  # type: ignore


    c2.valor = 10
    assert c2.valor_n == 10
    assert c2.valor_c == "10"

    with pytest.raises(ValueError):
        c2.valor = "str"  # type: ignore

    with pytest.raises(TypeError):
        c2.valor = [0]  # type: ignore
