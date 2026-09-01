import pytest

from escriturador_sped import Registro

from .cache import cache


@pytest.mark.parametrize("arquivo,tamanho_total,tamanho_blocos", [
    ("efd_contribuicoes_1.txt", 53, {"0": 5, "A": 2, "C": 2, "D": 2, "F": 2, "I": 2, "M": 4, "P": 2, "1": 2, "9": 30}),
    ("efd_contribuicoes_2.txt", 55, {"0": 6, "A": 2, "C": 2, "D": 2, "F": 2, "I": 2, "M": 4, "P": 2, "1": 2, "9": 31}),
    ("efd_contribuicoes_3.txt", 53, {"0": 5, "A": 2, "C": 2, "D": 2, "F": 2, "I": 2, "M": 4, "P": 2, "1": 2, "9": 30}),
    ("efd_contribuicoes_4.txt", 316, {"0": 112, "A": 11, "C": 31, "D": 13, "F": 10, "I": 2, "M": 66, "P": 2, "1": 2, "9": 67})
])
def test_blocos(arquivo: str, tamanho_total: int, tamanho_blocos: dict[str, int]):
    escrituracao = cache.escrituracao(arquivo)

    assert isinstance(escrituracao.abertura, Registro)
    assert isinstance(escrituracao.fechamento, Registro)

    assert isinstance(escrituracao.abertura.campos, tuple)
    assert isinstance(escrituracao.fechamento.campos, tuple)

    assert escrituracao.abertura.pai is None
    assert escrituracao.fechamento.pai is None

    assert escrituracao.abertura.nome == "0000"
    assert escrituracao.fechamento.nome == "9999"

    assert escrituracao.tamanho == tamanho_total

    assert len(escrituracao.filhos) == 2
    assert len(escrituracao.blocos) == 10

    assert isinstance(escrituracao.texto(), str)

    for nome_bloco, bloco in escrituracao.blocos.items():
        assert isinstance(bloco.abertura, Registro)
        assert isinstance(bloco.fechamento, Registro)

        assert isinstance(bloco.abertura.campos, tuple)
        assert isinstance(bloco.fechamento.campos, tuple)

        assert bloco.abertura.pai is escrituracao.abertura
        assert bloco.fechamento.pai is escrituracao.abertura

        assert bloco.abertura.nome == f"{bloco.nome}001"
        assert bloco.fechamento.nome == f"{bloco.nome}990"

        assert len(bloco.filhos) == 2

        assert bloco.tamanho == tamanho_blocos[nome_bloco]
