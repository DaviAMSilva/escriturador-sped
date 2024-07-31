import glob
import os

import pytest

from editor_sped import EscrituracaoICMSIPI, EscrituracaoPISCOFINS, abrir_escrituracao



@pytest.mark.parametrize("arquivo", glob.glob("efd_icms_ipi_*.txt", root_dir="exemplos/"))
def test_icms_ipi(arquivo):
    escrituracao_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    escrituracao = EscrituracaoICMSIPI(escrituracao_texto)

    resultado = escrituracao.converter_para_texto()

    assert escrituracao_texto == resultado



@pytest.mark.parametrize("arquivo", glob.glob("efd_pis_cofins_*.txt", root_dir="exemplos/"))
def test_pis_cofins(arquivo):
    escrituracao_texto = abrir_escrituracao(os.path.join("exemplos", arquivo))

    escrituracao = EscrituracaoPISCOFINS(escrituracao_texto)

    resultado = escrituracao.converter_para_texto()

    assert escrituracao_texto == resultado
