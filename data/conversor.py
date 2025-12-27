import argparse
import csv
import json
import os
from typing import Literal

from editor_sped.constantes import EFD_MAIOR_NIVEL, EFD_ORDEM_BLOCOS, EFD_TIPOS
from editor_sped.types import EfdInfo, EfdInfoRegistro










# Constantes específicas do conversor de tabelas
EFD_INFO_PASTA_DATA = "src/editor_sped/data/"
EFD_INFO_PASTA_VISUALIZADOR = "src/editor_sped/visualizador/"
EFD_INFO_ARQUIVO = "efd_info.{}"

EFD_JSON_INDENTACAO = 4

# Nomes das colunas esperadas para cada arquivo e cada módulo
COLUNAS = {
    "registros": {
        "efd_icms_ipi": ["block", "code", "required", "in_required", "out_required", "level", "card", "spec_required", "spec_in", "spec_out", "desc"],
        "efd_pis_cofins": ["block", "code", "required", "level", "card", "spec_required", "desc"]
    },
    "campos": {
        "efd_icms_ipi": ["Register", "Page", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig", "Entr", "Saídas"],
        "efd_pis_cofins": ["Register", "Page", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig"]
    }
}










def conversor():
    efd_info: EfdInfo = {}


    for efd_tipo in EFD_TIPOS:
        arquivo_registros = os.path.join(os.path.dirname(__file__), f"{efd_tipo}", "registers.csv")
        arquivo_campos = os.path.join(os.path.dirname(__file__), f"{efd_tipo}", "accurate_fields.csv")



        # Guarda as informações dos registros para cada arquivo
        objeto_registros: dict[str, "EfdInfoRegistro"] = {}



        converter_registros(efd_tipo, arquivo_registros, objeto_registros)
        converter_campos(efd_tipo, arquivo_campos, objeto_registros)



        efd_info[efd_tipo] = {
            "blocos": [],
            "registros": {}
        }

        # Adicionando informações sobre blocos
        for i, bloco_nome in enumerate(EFD_ORDEM_BLOCOS[efd_tipo]):
            efd_info[efd_tipo]["blocos"].append({
                "numero": i + 1,
                "nome": bloco_nome,
                "descricao": f"Bloco {bloco_nome}",
                "abertura": f"{bloco_nome}001",
                "fechamento": f"{bloco_nome}990"
            })

        efd_info[efd_tipo]["registros"] = objeto_registros



    return efd_info










def converter_registros(efd_tipo, arquivo_registros, objeto_registros):
    with open(arquivo_registros, encoding="utf-8", newline="") as ar:
        csv_registros = csv.DictReader(ar)

        if csv_registros.fieldnames != COLUNAS["registros"][efd_tipo]:
            raise ValueError(f"Colunas inválidas no arquivo registers.csv do módulo {efd_tipo}")

        for linha_registros in csv_registros:
            assert len(linha_registros) == len(COLUNAS["registros"][efd_tipo]), ("registros", efd_tipo, linha_registros)
            assert all(registro is not None for registro in linha_registros.values())

            registro_obrigatorio: bool = linha_registros["spec_required"] in ("O", "S")
            # NOTE: os campos "spec_in" e "spec_out" não devem ser usados para identificar
            # a obrigatoriedade geral de um registro devido a vários falsos positivos
            # or (
            #     "spec_in" in linha_registros and
            #     "spec_out" in linha_registros and
            #     linha_registros["spec_in"] == "O" and
            #     linha_registros["spec_out"] == "O"
            # )



            objeto_registros[linha_registros["code"]] = {
                "descricao": linha_registros["desc"].strip(),
                "nivel": int(linha_registros["level"]),
                "obrigatorio": registro_obrigatorio,
                # Não é preciso armazenar informação adicional sobre ocorrências pois todo registro com nível > 2 é automaticamente um registro "filho"
                "unico": linha_registros["card"].split(":")[-1] == "1",
                "campos": [],
                "filhos": [],
                "pai": None
            }



    # Ordena os registros conforme a ordem definida pelos manuais, independentemente da ordem de inserção original
    itens_ordenados = sorted(
        objeto_registros.items(),
        key=lambda registro, efd_tipo=efd_tipo:
        EFD_ORDEM_BLOCOS[efd_tipo].index(registro[0][0]) * 1000 + int(registro[0][1:4])
    )

    objeto_registros.clear()
    objeto_registros.update(itens_ordenados)



    ultimos_registros: list[str | None] = [None for _ in range(EFD_MAIOR_NIVEL + 1)]
    ultimos_registros[0] = "0000"
    nivel_anterior = -1

    # Isso pode ser feito pois em Python 3.7+ a ordenação das chaves de dicionários é garantida de ser idêntica à ordem de inserção
    for nome, registro in objeto_registros.items():
        nivel_atual = registro["nivel"]

        if nivel_atual > nivel_anterior + 1:
            raise ValueError(f"Registros fora da ordem válida. De {nivel_anterior} para {nivel_atual}")

        ultimos_registros[nivel_atual] = nome

        ultimos_registros_nivel_atual = ultimos_registros[nivel_atual]
        ultimos_registros_nivel_anterior = ultimos_registros[nivel_atual - 1]
        if ultimos_registros_nivel_atual and ultimos_registros_nivel_anterior:
            if nivel_atual > 0:
                objeto_registros[ultimos_registros_nivel_atual]["pai"] = ultimos_registros_nivel_anterior
                objeto_registros[ultimos_registros_nivel_anterior]["filhos"].append(ultimos_registros_nivel_atual)

        nivel_anterior = nivel_atual










def converter_campos(efd_tipo, arquivo_campos, objeto_registros):
    with open(arquivo_campos, encoding="utf-8", newline="") as ac:
        csv_campos = csv.DictReader(ac)

        if csv_campos.fieldnames != COLUNAS["campos"][efd_tipo]:
            raise ValueError(f"Colunas inválidas no arquivo accurate_fields do módulo {efd_tipo}")

        for linha_campos in csv_campos:
            assert len(linha_campos) == len(COLUNAS["campos"][efd_tipo]), ("campos", efd_tipo, linha_campos)
            assert all(campo is not None for campo in linha_campos.values())

            registro_nome = linha_campos["Register"]

            # NOTE: Os campos "Entr" e "Saídas" podem ser usados para identificar a obrigatoriedade geral de um campo apenas quando ambos forem "O"
            campo_obrigatorio = linha_campos["Obrig"] == "O" or (
                "Entr" in linha_campos and
                "Saídas" in linha_campos and
                linha_campos["Entr"] == "O" and
                linha_campos["Saídas"] == "O"
            )



            # Testa se o tipo de campo é um dos valores válidos
            assert linha_campos["Tipo"] in ("C", "N"), f"Tipo inesperado: {linha_campos['Tipo']}"
            tipo_campo: Literal["C", "N"] = linha_campos["Tipo"]
            tamanho_campo: int

            # Calculando o tamanho baseado nas regras
            if linha_campos["Tam"] in ("", "-"):
                if tipo_campo == "N":  # Numérico, sem limite no caso geral (assumindo 255 como limite prático)
                    tamanho_campo = 255
                elif tipo_campo == "C":  # Alfanumérico, limite de 255 no caso geral
                    tamanho_campo = 255
            else:
                tamanho_campo = int(linha_campos["Tam"].replace("*", "").replace("-", ""))



            objeto_registros[registro_nome]["campos"].append({
                "numero": int(linha_campos["Nº"]),
                "nome": linha_campos["Campo"].replace(" ", "").replace("*", ""),
                "descricao": linha_campos["Descrição"].strip(),
                "obrigatorio": campo_obrigatorio,
                "tamanho": tamanho_campo,
                "tamanho_exato": len(linha_campos["Tam"]) > 0 and linha_campos["Tam"][-1] == "*",
                "decimal": None if linha_campos["Dec"] in ("", "-") else int(linha_campos["Dec"]),
                "tipo": tipo_campo,
            })



            # Ordenando os campos para ter certeza da ordem correta
            objeto_registros[registro_nome]["campos"].sort(key=lambda x: x["numero"])








def main(formatado=False):
    efd_info_main = conversor()

    if not os.path.exists(EFD_INFO_PASTA_DATA):
        os.mkdir(EFD_INFO_PASTA_DATA)

    if not os.path.exists(EFD_INFO_PASTA_VISUALIZADOR):
        os.mkdir(EFD_INFO_PASTA_VISUALIZADOR)

    with open(os.path.join(EFD_INFO_PASTA_DATA, EFD_INFO_ARQUIVO.format("json")), "w", encoding="utf-8") as arquivo_convertido:
        arquivo_convertido.write(json.dumps(efd_info_main, indent=EFD_JSON_INDENTACAO if formatado else None, ensure_ascii=False))

    # Salvando como arquivo js para ser carregado no navegador
    with open(os.path.join(EFD_INFO_PASTA_VISUALIZADOR, EFD_INFO_ARQUIVO.format("js")), "w", encoding="utf-8") as arquivo_convertido:
        arquivo_convertido.write("window.EFD_INFO=" + json.dumps(efd_info_main, ensure_ascii=False))










if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte as tabelas EFD para um formato mais prático")
    parser.add_argument("--formatado", action="store_true", help="Gera o arquivo com uma formatação ao invés de ser minimizado")
    args = parser.parse_args()

    main(args.formatado)
