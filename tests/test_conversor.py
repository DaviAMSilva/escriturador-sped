import re
from collections import Counter
from glob import glob
from pathlib import Path

import pytest

from editor_sped import MAIOR_NIVEL, ORDEM_BLOCOS, Campo, LeiauteT, ModuloT
from scripts.conversor import conversor

from .constantes import MODULOS_REGISTROS


@pytest.mark.parametrize("caminho", glob("*/*/*/", root_dir="modulos"))
def test_conversor(caminho: str):
    modulo: ModuloT
    modulo, leiaute, versao = Path(caminho).parts # type: ignore
    leiaute_atual: LeiauteT = conversor(modulo, leiaute, versao)


    # Convertido para dicionário
    assert isinstance(leiaute_atual, dict)


    # As listas de registros tem os tamanhos corretos
    assert len(leiaute_atual["registros"]) == len(MODULOS_REGISTROS[modulo])


    # Os registros corretos existem nas listas
    for nome_registros, campos_registro in MODULOS_REGISTROS[modulo].items():
        verificar_registro(leiaute_atual["registros"], nome_registros, leiaute_atual["registros"][nome_registros], campos_registro)


    # Verificando que todos os registros são válidos
    for nome_registros in leiaute_atual["registros"]:
        assert nome_registros in MODULOS_REGISTROS[modulo]


    # As listas de blocos tem os tamanhos corretos
    assert len(leiaute_atual["blocos"]) == len(ORDEM_BLOCOS[modulo])


    # Os blocos corretos existem nas listas
    for bloco in leiaute_atual["blocos"]:
        assert bloco["nome"] in ORDEM_BLOCOS[modulo]


def verificar_registro(efd_registros, nome, registro, campos):
    # Nome e descrição
    assert nome in efd_registros
    assert len(nome) == 4
    assert re.fullmatch(r"[0ABCDEFGHIKMP19][0-9]{3}", nome)
    assert len(registro["descricao"]) > 0

    # Nível
    assert registro["nivel"] >= 0
    assert registro["nivel"] <= MAIOR_NIVEL

    # Booleanos
    assert isinstance(registro["obrigatorio"], bool)
    assert isinstance(registro["unico"], bool)

    # Campos
    assert isinstance(registro["campos"], list)
    assert len(registro["campos"]) >= 2
    assert len(registro["campos"]) == campos

    # Campos duplicados
    contagem = Counter(campo["nome"] for campo in registro["campos"]).most_common()
    assert contagem[0][1] == 1, f"Campo duplicado: {contagem[0][0]} presente {contagem[0][1]} vezes no registro {nome}"

    # Pai e filhos
    assert isinstance(registro["filhos"], list)
    assert (registro["pai"] is None and nome in ("0000", "9999")) or (isinstance(registro["pai"], str) and registro["pai"] in efd_registros)


    # Campos
    for campo in registro["campos"]:
        # Nome e descrição
        assert len(campo["nome"]) >= 2
        assert re.fullmatch(r"[A-ZÀ-ÿe0-9_-]+", campo["nome"]), campo["nome"]
        assert not re.fullmatch(r".*([e_-])\1.*", campo["nome"]), campo["nome"]
        assert len(campo["descricao"]) >= 8

        # Tamanho e número
        assert campo["numero"] >= 1
        assert campo["tamanho"] > 0

        # Booleanos
        assert isinstance(campo["obrigatorio"], bool)
        assert isinstance(campo["tamanho_exato"], bool)

        # Decimal
        assert campo["decimal"] is None or (isinstance(campo["decimal"], int) and int(campo["decimal"]) > 0)

        # Tipo
        assert campo["tipo"] in (Campo.ALFANUMERICO, Campo.NUMERICO)
