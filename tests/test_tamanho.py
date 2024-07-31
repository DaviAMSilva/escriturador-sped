import os

import pytest

from editor_sped import EscrituracaoPISCOFINS, abrir_escrituracao


@pytest.mark.parametrize("arquivo,tamanho_total,tamanho_blocos", [
    ("efd_pis_cofins_1.txt", 45, {"0": 5, "A": 2, "C": 2, "D": 2, "F": 2, "M": 4, "1": 2, "9": 26}),
    ("efd_pis_cofins_2.txt", 47, {"0": 6, "A": 2, "C": 2, "D": 2, "F": 2, "M": 4, "1": 2, "9": 27}),
    ("efd_pis_cofins_3.txt", 45, {"0": 5, "A": 2, "C": 2, "D": 2, "F": 2, "M": 4, "1": 2, "9": 26}),
    ("efd_pis_cofins_4.txt", 308, {"0": 112, "A": 11, "C": 31, "D": 13, "F": 10, "M": 66, "1": 2, "9": 63})
])
def test_tamanho_blocos(arquivo, tamanho_total, tamanho_blocos):
    escrituracao_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    escrituracao = EscrituracaoPISCOFINS(escrituracao_texto)

    assert escrituracao.tamanho == tamanho_total

    for nome_bloco, bloco in escrituracao.blocos.items():
        assert bloco.tamanho == tamanho_blocos[nome_bloco]
