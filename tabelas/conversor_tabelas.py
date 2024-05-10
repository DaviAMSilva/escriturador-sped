import csv
import json
import os
from typing import *



# FIXME: Determinar uma maneira de importar as constantes do módulo sem executar a leitura do arquivo efd_info.json
# Porque esse arquivo conversor não é suposto a ser um arquivo do módulo, mas sim um arquivo que ajuda a gerar o módulo
EFD_NOMES = "efd_icms_ipi", "efd_pis_cofins"
EFD_MAIOR_NIVEL = 6

# Constantes específicas do conversor de tabelas
EFD_JSON_INDENTACAO = None
EFD_ORDEM_BLOCOS = {
    "efd_icms_ipi": {
        "0": 0, "A": 1,
        "B": 2, "C": 3,
        "D": 4, "E": 5,
        "G": 6, "H": 7,
        "I": 8, "K": 9,
        "M": 10, "P": 11,
        "1": 12, "9": 13,
    },
    "efd_pis_cofins": {
        "0": 0, "A": 1,
        "C": 2, "D": 3,
        "F": 4, "I": 5,
        "M": 6, "P": 7,
        "1": 8, "9": 9,
    },
    "geral": {
        "0": 0, "A": 1,
        "B": 2, "C": 3,
        "D": 4, "E": 5,
        "G": 6, "H": 7,
        "I": 8, "K": 9,
        "M": 10, "P": 11,
        "1": 12, "9": 13,
    }
}



def main(diretorio=""):
    efd_info = {}



    for efd_nome in EFD_NOMES:
        arquivo_registros = os.path.join(diretorio, f"{efd_nome}_registers.csv")
        arquivo_campos = os.path.join(diretorio, f"{efd_nome}_accurate_fields.csv")



        # Guarda as informações dos registros para cada arquivo
        objeto_registros: dict[str, dict] = {}



        with open(arquivo_registros, encoding="utf-8", newline="") as ar:
            for linha_registros in csv.DictReader(ar):
                registro_obrigatorio = linha_registros["spec_required"] == "O"
                # NOTE: os campos "spec_in" e "spec_out" não devem ser usados para identificar a obrigatoriedade geral de um registro devido a vários falsos positivos
                # or (
                #     "spec_in" in linha_registros and
                #     "spec_out" in linha_registros and
                #     linha_registros["spec_in"] == "O" and
                #     linha_registros["spec_out"] == "O"
                # )



                objeto_registros[linha_registros["code"]] = {
                    "descricao": linha_registros["desc"],
                    "nivel": int(linha_registros["level"]),
                    "obrigatorio": registro_obrigatorio,

                    # Não é preciso armazenar informação adicional sobre ocorrências pois todo registro com nível > 2 é automaticamente um registro "filho"
                    "unico": linha_registros["card"].split(":")[-1] == "1",
                    "campos": [],
                }



        # Ordena os registros conforme a ordem definida pelos manuais, independentemente da ordem de inserção original
        objeto_registros = dict(sorted(objeto_registros.items(), key=lambda a: EFD_ORDEM_BLOCOS[efd_nome][a[0][0]] * 1000 + int(a[0][1:4])))



        ultimos_registros: List[dict] = [None for _ in range(EFD_MAIOR_NIVEL + 1)]
        ultimos_registros[0] = "0000"
        nivel_anterior = -1

        # Isso pode ser feito pois em Python 3.7+ a ordenação das chaves de dicionários é garantida de ser idêntica à ordem de inserção
        for nome, registro in objeto_registros.items():
            registro["filhos"] = []
            registro["pai"] = None

            nivel_atual = registro["nivel"]

            if nivel_atual > nivel_anterior + 1:
                raise ValueError(f"Registros foram da ordem válida. De {nivel_anterior} ({ultimos_registros[nivel_anterior]}) para {nivel_atual} ({ultimos_registros[nivel_atual]})")
            elif nivel_atual == nivel_anterior + 1 or nivel_atual <= nivel_anterior:
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
                    "nome": linha_campos["Campo"],
                    "descricao": linha_campos["Descrição"],
                    "obrigatorio": campo_obrigatorio,
                    "tamanho": tamanho,
                    "tamanho_exato": len(linha_campos["Tam"]) > 0 and linha_campos["Tam"][-1] == "*",
                    "decimal": None if linha_campos["Dec"] in ("", "-") else int(linha_campos["Dec"]),
                    "tipo": linha_campos["Tipo"],
                })



                # Ordenando os campos para ter certeza da ordem correta
                objeto_registros[registro_nome]["campos"].sort(key=lambda x: x["numero"])



        efd_info[efd_nome] = objeto_registros



    return efd_info






if __name__ == "__main__":
    efd_info = main()

    # TODO: Adicionar condição para minimizar o arquivo json somente quando for gerado para produção usando variáveis de ambiente
    with open(f"efd_info.json", "w", encoding="utf-8") as arquivo_convertido:
        arquivo_convertido.write(json.dumps(efd_info, indent=EFD_JSON_INDENTACAO, ensure_ascii=False))
