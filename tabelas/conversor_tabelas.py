import argparse
import csv
import json
import os
from typing import Literal










EFD_TIPOS = "efd_icms_ipi", "efd_pis_cofins"
EFD_MAIOR_NIVEL = 6

# Constantes específicas do conversor de tabelas
EFD_INFO_PASTA = "src/editor_sped/data/"
EFD_INFO_ARQUIVO = "efd_info.json"

EFD_JSON_INDENTACAO = 4

EFD_ORDEM_BLOCOS:dict[Literal["efd_icms_ipi", "efd_pis_cofins"], str] = {
    "efd_icms_ipi": ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"],
    "efd_pis_cofins": ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"]
}



def main():
    efd_info = {}



    for efd_tipo in EFD_TIPOS:
        arquivo_registros = os.path.join(os.path.dirname(__file__), f"{efd_tipo}_registers.csv")
        arquivo_campos = os.path.join(os.path.dirname(__file__), f"{efd_tipo}_accurate_fields.csv")



        # Guarda as informações dos registros para cada arquivo
        objeto_registros: dict[str, dict] = {}



        with open(arquivo_registros, encoding="utf-8", newline="") as ar:
            for linha_registros in csv.DictReader(ar):
                registro_obrigatorio = linha_registros["spec_required"] == "O"
                # NOTE: os campos "spec_in" e "spec_out" não devem ser usados para identificar
                # a obrigatoriedade geral de um registro devido a vários falsos positivos
                # or (
                #     "spec_in" in linha_registros and
                #     "spec_out" in linha_registros and
                #     linha_registros["spec_in"] == "O" and
                #     linha_registros["spec_out"] == "O"
                # )



                objeto_registros[linha_registros["code"]] = {
                    # Substituindo “ (0x201C) e ” (0x201D) pelas aspas duplas padrão
                    "descricao": linha_registros["desc"].replace("“", "\"").replace("”", "\""),

                    "nivel": int(linha_registros["level"]),
                    "obrigatorio": registro_obrigatorio,

                    # Não é preciso armazenar informação adicional sobre ocorrências pois todo registro com nível > 2 é automaticamente um registro "filho"
                    "unico": linha_registros["card"].split(":")[-1] == "1",
                    "campos": [],
                }



        # Ordena os registros conforme a ordem definida pelos manuais, independentemente da ordem de inserção original
        objeto_registros = dict(sorted(objeto_registros.items(), key=lambda r: EFD_ORDEM_BLOCOS[efd_tipo].index(r[0][0]) * 1000 + int(r[0][1:4])))



        ultimos_registros: list[dict] = [None for _ in range(EFD_MAIOR_NIVEL + 1)]
        ultimos_registros[0] = "0000"
        nivel_anterior = -1

        # Isso pode ser feito pois em Python 3.7+ a ordenação das chaves de dicionários é garantida de ser idêntica à ordem de inserção
        for nome, registro in objeto_registros.items():
            registro["filhos"] = []
            registro["pai"] = None

            nivel_atual = registro["nivel"]

            if nivel_atual > nivel_anterior + 1:
                raise ValueError(f"Registros fora da ordem válida. De {nivel_anterior} para {nivel_atual}")

            ultimos_registros[nivel_atual] = nome

            if (nivel_atual > 0):
                objeto_registros[ultimos_registros[nivel_atual]]["pai"] = ultimos_registros[nivel_atual - 1]
                objeto_registros[ultimos_registros[nivel_atual - 1]]["filhos"].append(ultimos_registros[nivel_atual])

            nivel_anterior = nivel_atual





        with open(arquivo_campos, encoding="utf-8", newline="") as ac:
            for linha_campos in csv.DictReader(ac):
                registro_nome = linha_campos["Register"]

                # NOTE: Os campos "Entr" e "Saídas" podem ser usados para identificar a obrigatoriedade geral de um campo apenas quando ambos forem "O"
                campo_obrigatorio = linha_campos["Obrig"] == "O" or (
                    "Entr" in linha_campos and
                    "Saídas" in linha_campos and
                    linha_campos["Entr"] == "O" and
                    linha_campos["Saídas"] == "O"
                )



                # Calculando o tamanho baseado nas regras
                if linha_campos["Tam"] in ("", "-"):
                    if linha_campos["Tipo"] == "N":  # Numérico, limite de 255 no caso geral
                        tamanho = 255
                    elif linha_campos["Tipo"] == "C":  # Alfanumérico, sem limite no caso geral (assumindo 65535 como limite prático)
                        tamanho = 65535
                else:
                    tamanho = int(linha_campos["Tam"].replace("*", "").replace("-", ""))



                objeto_registros[registro_nome]["campos"].append({
                    "numero": int(linha_campos["Nº"]),

                    # Removendo espaços devido ao um erro do programa que lê os PDFs dos manuais
                    "nome": linha_campos["Campo"].replace(" ", ""),

                    # Substituindo “ (0x201C) e ” (0x201D) pelas aspas duplas padrão
                    "descricao": linha_campos["Descrição"].replace("“", "\"").replace("”", "\""),

                    "obrigatorio": campo_obrigatorio,
                    "tamanho": tamanho,
                    "tamanho_exato": len(linha_campos["Tam"]) > 0 and linha_campos["Tam"][-1] == "*",
                    "decimal": None if linha_campos["Dec"] in ("", "-") else int(linha_campos["Dec"]),
                    "tipo": linha_campos["Tipo"],
                })



                # Ordenando os campos para ter certeza da ordem correta
                objeto_registros[registro_nome]["campos"].sort(key=lambda x: x["numero"])



        efd_info[efd_tipo] = {}



        # Adicionando informações sobre blocos
        efd_info[efd_tipo]["blocos"] = []
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










if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte as tabelas EFD para um formato mais prático")
    parser.add_argument("--formatado", action="store_true", help="Gera o arquivo com uma formatação ao invés de ser minimizado")
    args = parser.parse_args()

    efd_info_main = main()

    if not os.path.exists(EFD_INFO_PASTA):
        os.mkdir(EFD_INFO_PASTA)

    with open(os.path.join(EFD_INFO_PASTA, EFD_INFO_ARQUIVO), "w", encoding="utf-8") as arquivo_convertido:
        arquivo_convertido.write(json.dumps(efd_info_main, indent=EFD_JSON_INDENTACAO if args.formatado else None, ensure_ascii=False))
