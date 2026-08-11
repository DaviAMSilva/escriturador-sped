import argparse
import csv
import json
import os
from glob import glob
from pathlib import Path

from editor_sped.constantes import EFD_MAIOR_NIVEL, EFD_ORDEM_BLOCOS
from editor_sped.efd_info import CampoTipo, EfdInfoRegistro, EfdInfoTipo, EfdTipo










# Constantes específicas do conversor de tabelas
EFD_INFO_PASTA_MODULOS = "src/editor_sped/modulos/"
EFD_INFO_ARQUIVO = "leiaute.{}"

EFD_JSON_INDENTACAO = 4

# Nomes das colunas esperadas para cada arquivo e cada módulo
COLUNAS = {
    "contribuicoes": {
        "campos": ["Register", "Page", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig"],
        "registros": ["block", "code", "required", "level", "card", "spec_required", "desc"]
    },
    "icms_ipi": {
        "campos": ["Register", "Page", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig", "Entr", "Saídas"],
        "registros": ["block", "code", "required", "in_required", "out_required", "level", "card", "spec_required", "spec_in", "spec_out", "desc"],
    }
}










def conversor(efd: EfdTipo, leiaute: str, versao: str) -> EfdInfoTipo:
    arquivo_registros = os.path.join(os.path.dirname(__file__), "..", "modulos", efd, leiaute, versao, "registros.csv")
    arquivo_campos = os.path.join(os.path.dirname(__file__), "..", "modulos", efd, leiaute, versao, "campos.csv")



    # Guarda as informações dos registros para cada arquivo
    objeto_registros: dict[str, EfdInfoRegistro] = {}



    converter_registros(efd, arquivo_registros, objeto_registros)
    converter_campos(efd, arquivo_campos, objeto_registros)



    efd_leiaute: EfdInfoTipo = {
        "blocos": [],
        "registros": {}
    }

    # Adicionando informações sobre blocos
    for i, nome_bloco in enumerate(EFD_ORDEM_BLOCOS[efd]):
        efd_leiaute["blocos"].append({
            "numero": i + 1,
            "nome": nome_bloco,
            "descricao": f"Bloco {nome_bloco}",
            "abertura": f"{nome_bloco}001",
            "fechamento": f"{nome_bloco}990"
        })

    efd_leiaute["registros"] = objeto_registros



    return efd_leiaute










def converter_registros(efd_tipo: EfdTipo, arquivo_registros: str, objeto_registros: dict[str, EfdInfoRegistro]) -> None:
    with open(arquivo_registros, encoding="utf-8", newline="") as ar:
        csv_registros = csv.DictReader(ar)

        if csv_registros.fieldnames != COLUNAS[efd_tipo]["registros"]:
            raise ValueError(f"Colunas inválidas no arquivo registers.csv do módulo {efd_tipo}")

        for linha_registros in csv_registros:
            assert len(linha_registros) == len(COLUNAS[efd_tipo]["registros"]), ("registros", efd_tipo, linha_registros)
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










def converter_campos(efd_tipo: EfdTipo, arquivo_campos: str, objeto_registros: dict[str, EfdInfoRegistro]):
    with open(arquivo_campos, encoding="utf-8", newline="") as ac:
        csv_campos = csv.DictReader(ac)

        if csv_campos.fieldnames != COLUNAS[efd_tipo]["campos"]:
            raise ValueError(f"Colunas inválidas no arquivo accurate_fields do módulo {efd_tipo}")

        for linha_campos in csv_campos:
            assert len(linha_campos) == len(COLUNAS[efd_tipo]["campos"]), ("campos", efd_tipo, linha_campos)
            assert all(campo is not None for campo in linha_campos.values())

            nome_registro = linha_campos["Register"]

            # NOTE: Os campos "Entr" e "Saídas" podem ser usados para identificar a obrigatoriedade geral de um campo apenas quando ambos forem "O"
            campo_obrigatorio = linha_campos["Obrig"] == "O" or (
                "Entr" in linha_campos and
                "Saídas" in linha_campos and
                linha_campos["Entr"] == "O" and
                linha_campos["Saídas"] == "O"
            )



            # Testa se o tipo de campo é um dos valores válidos
            assert linha_campos["Tipo"] in ("C", "N"), f"Tipo inesperado: {linha_campos['Tipo']}"
            tipo_campo: CampoTipo = linha_campos["Tipo"]
            tamanho_campo: int

            # Calculando o tamanho baseado nas regras
            if linha_campos["Tam"] in ("", "-"):
                if tipo_campo == "N":  # Numérico, sem limite no caso geral (assumindo 255 como limite prático)
                    tamanho_campo = 255
                elif tipo_campo == "C":  # Alfanumérico, limite de 255 no caso geral
                    tamanho_campo = 255
            else:
                tamanho_campo = int(linha_campos["Tam"].replace("*", "").replace("-", ""))



            objeto_registros[nome_registro]["campos"].append({
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
            objeto_registros[nome_registro]["campos"].sort(key=lambda x: x["numero"])








def main(formatado: bool = False):
    for caminho in glob("*/*/*/", root_dir="modulos"):
        efd: EfdTipo
        efd, leiaute, versao = Path(caminho).parts # type: ignore

        efd_info = conversor(efd, leiaute, versao)


        caminho_modulo = os.path.join(EFD_INFO_PASTA_MODULOS, efd, leiaute, versao)
        if not os.path.exists(caminho_modulo):
            os.makedirs(caminho_modulo)

        with open(os.path.join(caminho_modulo, EFD_INFO_ARQUIVO.format("json")), "w", encoding="utf-8") as arquivo_convertido:
            arquivo_convertido.write(json.dumps(efd_info, indent=EFD_JSON_INDENTACAO if formatado else None, ensure_ascii=False))










if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte as tabelas EFD para um formato mais prático")
    parser.add_argument("--formatado", action="store_true", help="Gera o arquivo com uma formatação ao invés de ser minimizado")
    args = parser.parse_args()

    main(args.formatado)
