import re

from data.conversor import EFD_MAIOR_NIVEL, conversor

REGISTROS_EFD_ICMS_IPI = ['0000', '0001', '0002', '0005', '0015', '0100', '0150', '0175', '0190', '0200', '0205', '0206', '0210', '0220', '0221', '0300', '0305', '0400', '0450', '0460', '0500', '0600', '0990', 'B001', 'B020', 'B025', 'B030', 'B350', 'B420', 'B440', 'B460', 'B470', 'B500', 'B510', 'B990', 'C001', 'C100', 'C101', 'C105', 'C110', 'C111', 'C112', 'C113', 'C114', 'C115', 'C116', 'C120', 'C130', 'C140', 'C141', 'C160', 'C165', 'C170', 'C171', 'C172', 'C173', 'C174', 'C175', 'C176', 'C177', 'C178', 'C179', 'C180', 'C181', 'C185', 'C186', 'C190', 'C191', 'C195', 'C197', 'C300', 'C310', 'C320', 'C321', 'C330', 'C350', 'C370', 'C380', 'C390', 'C400', 'C405', 'C410', 'C420', 'C425', 'C430', 'C460', 'C465', 'C470', 'C480', 'C490', 'C495', 'C500', 'C510', 'C590', 'C591', 'C595', 'C597', 'C600', 'C601', 'C610', 'C690', 'C700', 'C790', 'C791', 'C800', 'C810', 'C815', 'C850', 'C855', 'C857', 'C860', 'C870', 'C880', 'C890', 'C895', 'C897', 'C990', 'D001', 'D100', 'D101', 'D110', 'D120', 'D130', 'D140', 'D150', 'D160', 'D161', 'D162', 'D170', 'D180', 'D190', 'D195', 'D197', 'D300', 'D301', 'D310', 'D350', 'D355', 'D360', 'D365', 'D370', 'D390', 'D400', 'D410', 'D411', 'D420', 'D500', 'D510', 'D530', 'D590', 'D600', 'D610', 'D690', 'D695', 'D696', 'D697', 'D700', 'D730', 'D731', 'D735', 'D737', 'D750', 'D760', 'D761', 'D990', 'E001', 'E100', 'E110', 'E111', 'E112', 'E113', 'E115', 'E116', 'E200', 'E210', 'E220', 'E230', 'E240', 'E250', 'E300', 'E310', 'E311', 'E312', 'E313', 'E316', 'E500', 'E510', 'E520', 'E530', 'E531', 'E990', 'G001', 'G110', 'G125', 'G126', 'G130', 'G140', 'G990', 'H001', 'H005', 'H010', 'H020', 'H030', 'H990', 'K001', 'K010', 'K100', 'K200', 'K210', 'K215', 'K220', 'K230', 'K235', 'K250', 'K255', 'K260', 'K265', 'K270', 'K275', 'K280', 'K290', 'K291', 'K292', 'K300', 'K301', 'K302', 'K990', '1001', '1010', '1100', '1105', '1110', '1200', '1210', '1250', '1255', '1300', '1310', '1320', '1350', '1360', '1370', '1390', '1391', '1400', '1500', '1510', '1600', '1601', '1700', '1710', '1800', '1900', '1910', '1920', '1921', '1922', '1923', '1925', '1926', '1960', '1970', '1975', '1980', '1990', '9001', '9900', '9990', '9999']  # nopep8 pylint: disable=line-too-long
REGISTROS_EFD_PIS_COFINS = ['0000', '0001', '0035', '0100', '0110', '0111', '0120', '0140', '0145', '0150', '0190', '0200', '0205', '0206', '0208', '0400', '0450', '0500', '0600', '0900', '0990', 'A001', 'A010', 'A100', 'A110', 'A111', 'A120', 'A170', 'A990', 'C001', 'C010', 'C100', 'C110', 'C111', 'C120', 'C170', 'C175', 'C180', 'C181', 'C185', 'C188', 'C190', 'C191', 'C195', 'C198', 'C199', 'C380', 'C381', 'C385', 'C395', 'C396', 'C400', 'C405', 'C481', 'C485', 'C489', 'C490', 'C491', 'C495', 'C499', 'C500', 'C501', 'C505', 'C509', 'C600', 'C601', 'C605', 'C609', 'C800', 'C810', 'C820', 'C830', 'C860', 'C870', 'C880', 'C890', 'C990', 'D001', 'D010', 'D100', 'D101', 'D105', 'D111', 'D200', 'D201', 'D205', 'D209', 'D300', 'D309', 'D350', 'D359', 'D500', 'D501', 'D505', 'D509', 'D600', 'D601', 'D605', 'D609', 'D990', 'F001', 'F010', 'F100', 'F111', 'F120', 'F129', 'F130', 'F139', 'F150', 'F200', 'F205', 'F210', 'F211', 'F500', 'F509', 'F510', 'F519', 'F525', 'F550', 'F559', 'F560', 'F569', 'F600', 'F700', 'F800', 'F990', 'I001', 'I010', 'I100', 'I199', 'I200', 'I299', 'I300', 'I399', 'I990', 'M001', 'M100', 'M105', 'M110', 'M115', 'M200', 'M205', 'M210', 'M211', 'M215', 'M220', 'M225', 'M230', 'M300', 'M350', 'M400', 'M410', 'M500', 'M505', 'M510', 'M515', 'M600', 'M605', 'M610', 'M611', 'M615', 'M620', 'M625', 'M630', 'M700', 'M800', 'M810', 'M990', 'P001', 'P010', 'P100', 'P110', 'P199', 'P200', 'P210', 'P990', '1001', '1010', '1011', '1020', '1050', '1100', '1101', '1102', '1200', '1210', '1220', '1300', '1500', '1501', '1502', '1600', '1610', '1620', '1700', '1800', '1809', '1900', '1990', '9001', '9900', '9990', '9999']  # nopep8 pylint: disable=line-too-long

BLOCOS_EFD_ICMS_IPI = ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"]
BLOCOS_EFD_PIS_COFINS = ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"]



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
    for registro_nome in REGISTROS_EFD_ICMS_IPI:
        verificar_registro(efd_info["efd_icms_ipi"]["registros"], registro_nome, efd_info["efd_icms_ipi"]["registros"][registro_nome])

    for registro_nome in REGISTROS_EFD_PIS_COFINS:
        verificar_registro(efd_info["efd_pis_cofins"]["registros"], registro_nome, efd_info["efd_pis_cofins"]["registros"][registro_nome])


    # As listas de blocos tem os tamanhos corretos
    assert len(efd_info["efd_icms_ipi"]["blocos"]) == len(BLOCOS_EFD_ICMS_IPI)
    assert len(efd_info["efd_pis_cofins"]["blocos"]) == len(BLOCOS_EFD_PIS_COFINS)


    # Os blocos corretos existem nas listas
    for bloco in efd_info["efd_icms_ipi"]["blocos"]:
        assert bloco["nome"] in BLOCOS_EFD_ICMS_IPI

    for bloco in efd_info["efd_pis_cofins"]["blocos"]:
        assert bloco["nome"] in BLOCOS_EFD_PIS_COFINS



def verificar_registro(efd, nome, registro):
    # Nome e descrição
    assert nome in efd
    assert len(nome) == 4
    assert re.match(r"^[0ABCDEFGHIKMP19][0-9]{3}$", nome), nome
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

    # Pai e filhos
    assert isinstance(registro["filhos"], list)
    assert (registro["pai"] is None and nome in ("0000", "9999")) or (isinstance(registro["pai"], str) and len(registro["pai"]) == 4) and registro["pai"] in efd



    # Campos
    for campo in registro["campos"]:
        # Nome e descrição
        assert len(campo["nome"]) > 0
        assert campo["nome"].find(" ") == -1, campo["nome"]
        assert len(campo["descricao"]) > 0

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
