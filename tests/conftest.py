# pylint: disable=W0621

import os
from glob import glob

import pytest

from editor_sped.classes.escrituracao import Escrituracao, EscrituracaoICMSIPI, EscrituracaoPISCOFINS
from editor_sped.utilidades import abrir_escrituracao



@pytest.fixture(scope="session")
def textos_todos(textos_icms_ipi: dict[str, str], textos_pis_cofins: dict[str, str]):
    return {**textos_icms_ipi, **textos_pis_cofins}


@pytest.fixture(scope="session")
def textos_icms_ipi():
    textos: dict[str, str] = {}
    arquivos = glob("efd_icms_ipi_*.txt", root_dir="exemplos/")

    for arquivo in arquivos:
        textos[arquivo] = abrir_escrituracao(os.path.join("exemplos", arquivo))

    return textos


@pytest.fixture(scope="session")
def textos_pis_cofins():
    textos: dict[str, str] = {}
    arquivos = glob("efd_pis_cofins_*.txt", root_dir="exemplos/")

    for arquivo in arquivos:
        textos[arquivo] = abrir_escrituracao(os.path.join("exemplos", arquivo))

    return textos







@pytest.fixture(scope="session")
def escrituracoes_todas(escrituracoes_icms_ipi: dict[str, tuple[str, Escrituracao]], escrituracoes_pis_cofins: dict[str, tuple[str, Escrituracao]]):
    return {**escrituracoes_icms_ipi, **escrituracoes_pis_cofins}


@pytest.fixture(scope="session")
def escrituracoes_icms_ipi(textos_icms_ipi: dict[str, str]):
    escrituracoes: dict[str, Escrituracao] = {}

    for arquivo, escrituracao_texto in textos_icms_ipi.items():
        escrituracoes[arquivo] = EscrituracaoICMSIPI(escrituracao_texto)

    return escrituracoes


@pytest.fixture(scope="session")
def escrituracoes_pis_cofins(textos_pis_cofins: dict[str, str]):
    escrituracoes: dict[str, Escrituracao] = {}

    for arquivo, escrituracao_texto in textos_pis_cofins.items():
        escrituracoes[arquivo] = EscrituracaoPISCOFINS(escrituracao_texto)

    return escrituracoes
