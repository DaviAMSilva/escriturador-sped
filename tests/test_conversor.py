import re

from data.conversor import EFD_MAIOR_NIVEL, conversor

from .constantes import BLOCOS_EFD_ICMS_IPI, BLOCOS_EFD_PIS_COFINS, REGISTROS_EFD_ICMS_IPI, REGISTROS_EFD_PIS_COFINS


def test_conversor():
    efd_info = conversor()



    # Convertido para dicionário
    assert isinstance(efd_info, dict)



    # Os SPEDs existem
    assert "efd_icms_ipi" in efd_info
    assert "efd_pis_cofins" in efd_info


    # As listas de registros tem os tamanhos corretos
    assert len(efd_info["efd_icms_ipi"]["registros"]) == len(REGISTROS_EFD_ICMS_IPI)
    assert len(efd_info["efd_pis_cofins"]["registros"]) == len(REGISTROS_EFD_PIS_COFINS)


    # Os registros corretos existem nas listas
    for registro_nome, registro_campos in REGISTROS_EFD_ICMS_IPI.items():
        verificar_registro(efd_info["efd_icms_ipi"]["registros"], registro_nome, efd_info["efd_icms_ipi"]["registros"][registro_nome], registro_campos)

    for registro_nome, registro_campos in REGISTROS_EFD_PIS_COFINS.items():
        verificar_registro(efd_info["efd_pis_cofins"]["registros"], registro_nome, efd_info["efd_pis_cofins"]["registros"][registro_nome], registro_campos)


    # Verificando que todos os registros são válidos
    for registro_nome in efd_info["efd_icms_ipi"]["registros"]:
        assert registro_nome in REGISTROS_EFD_ICMS_IPI

    for registro_nome in efd_info["efd_pis_cofins"]["registros"]:
        assert registro_nome in REGISTROS_EFD_PIS_COFINS


    # As listas de blocos tem os tamanhos corretos
    assert len(efd_info["efd_icms_ipi"]["blocos"]) == len(BLOCOS_EFD_ICMS_IPI)
    assert len(efd_info["efd_pis_cofins"]["blocos"]) == len(BLOCOS_EFD_PIS_COFINS)


    # Os blocos corretos existem nas listas
    for bloco in efd_info["efd_icms_ipi"]["blocos"]:
        assert bloco["nome"] in BLOCOS_EFD_ICMS_IPI

    for bloco in efd_info["efd_pis_cofins"]["blocos"]:
        assert bloco["nome"] in BLOCOS_EFD_PIS_COFINS


def verificar_registro(efd_registros, nome, registro, campos):
    # Nome e descrição
    assert nome in efd_registros
    assert len(nome) == 4
    assert re.fullmatch(r"[0ABCDEFGHIKMP19][0-9]{3}", nome)
    assert len(registro["descricao"]) > 0

    # Nível
    assert registro["nivel"] >= 0
    assert registro["nivel"] <= EFD_MAIOR_NIVEL

    # Booleanos
    assert isinstance(registro["obrigatorio"], bool)
    assert isinstance(registro["unico"], bool)

    # Campos
    assert isinstance(registro["campos"], list)
    assert len(registro["campos"]) >= 2
    assert len(registro["campos"]) == campos

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
        assert campo["tipo"] in ("C", "N")
