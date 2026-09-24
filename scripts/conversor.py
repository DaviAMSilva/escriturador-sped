import argparse
import csv
import json
import os
from glob import glob
from pathlib import Path
from typing import Literal

# Permite importar a biblioteca mesmo sem os módulos gerados
# pylint: disable=wrong-import-position
os.environ["__CONVERSAO__"] = "1"

from escriturador_sped.constantes import MAIOR_NIVEL, ORDEM_BLOCOS
from escriturador_sped.tipos import CampoTipoT, LeiauteT, ModuloT, RegistroT










# Decide a indentação do arquivo JSON se --formatado for usado
JSON_INDENTACAO = 4


# Nomes das colunas esperadas para cada arquivo e cada módulo
COLUNAS: dict[ModuloT, dict[Literal["campos", "registros"], list[str]]] = {
    "ecd": {
        "campos": ["Register", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Valores Válidos", "Obrig", "Regras de Validação do Campo"],
        "registros": ["block", "code", "required", "level", "card", "spec_required", "desc"]
    },
    "ecf": {
        "campos": ["Register", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Valores Válidos", "Obrig"],
        "registros": ["block", "code", "required", "level", "card", "spec_required", "desc"]
    },
    "efd_contribuicoes": {
        "campos": ["Register", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig"],
        "registros": ["block", "code", "required", "level", "card", "spec_required", "desc"]
    },
    "efd_icms_ipi": {
        "campos": ["Register", "Nº", "Campo", "Descrição", "Tipo", "Tam", "Dec", "Obrig", "Entr", "Saídas"],
        "registros": ["block", "code", "required", "in_required", "out_required", "level", "card", "spec_required", "spec_in", "spec_out", "desc"],
    }
}


# Registros com quantidades variáveis de campos (suporte experimental)
# list:  Múltiplos valores possíveis
# tuple: Faixa de valores possíveis (inclusive)
CAMPOS_VARIAVEIS: dict[ModuloT, dict[str, None | list[int] | tuple[int, int]]] = {
    "ecd": {
        # Leiaute parametrizável (I510)
        "I550": (1, 100),
        "I555": (1, 100),
        # Campos adicionais (I020)
        "I155": [9, 15],
        "I157": [5, 7],
        "I200": [6, 7],
        "I250": [9, 11],
        "I310": [5, 7],
        "I355": [5, 7],
    }
}










def conversor(modulo: ModuloT, leiaute: str, manual: str) -> LeiauteT:
    arquivo_registros = os.path.join(os.path.dirname(__file__), "..", "modulos", modulo, leiaute, manual, "registros.csv")
    arquivo_campos = os.path.join(os.path.dirname(__file__), "..", "modulos", modulo, leiaute, manual, "campos.csv")



    # Guarda as informações dos registros para cada arquivo
    objeto_registros: dict[str, RegistroT] = {}



    converter_registros(modulo, arquivo_registros, objeto_registros)
    converter_campos(modulo, arquivo_campos, objeto_registros)



    leiaute_retorno: LeiauteT = {
        "blocos": [],
        "registros": {}
    }

    # Adicionando informações sobre blocos
    for i, nome_bloco in enumerate(ORDEM_BLOCOS[modulo]):
        leiaute_retorno["blocos"].append({
            "numero": i + 1,
            "nome": nome_bloco,
            "descricao": f"Bloco {nome_bloco}",
            "abertura": f"{nome_bloco}001",
            "fechamento": f"{nome_bloco}990"
        })

    leiaute_retorno["registros"] = objeto_registros



    return leiaute_retorno










def converter_registros(modulo: ModuloT, arquivo_registros: str, objeto_registros: dict[str, RegistroT]) -> None:
    with open(arquivo_registros, encoding="utf-8", newline="") as ar:
        csv_registros = csv.DictReader(ar)

        if csv_registros.fieldnames != COLUNAS[modulo]["registros"]:
            raise ValueError(f"Colunas inválidas no arquivo registers.csv do módulo {modulo}")

        for linha_registros in csv_registros:
            assert len(linha_registros) == len(COLUNAS[modulo]["registros"]), ("registros", modulo, linha_registros)
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


            try:
                campos_variaveis = CAMPOS_VARIAVEIS[modulo][linha_registros["code"]]
            except KeyError:
                campos_variaveis = None


            objeto_registros[linha_registros["code"]] = {
                "descricao": linha_registros["desc"].strip(),
                "nivel": int(linha_registros["level"]),
                "obrigatorio": registro_obrigatorio,
                "unico": linha_registros["card"].split(":")[-1] == "1",
                "campos": [],
                "campos_exatos": campos_variaveis if isinstance(campos_variaveis, list) else None,
                "campos_faixa": campos_variaveis if isinstance(campos_variaveis, tuple) else None,
                "filhos": [],
                "pai": None
            }



    # Ordena os registros conforme a ordem definida pelos manuais, independentemente da ordem de inserção original
    itens_ordenados = sorted(
        objeto_registros.items(),
        key=lambda registro, modulo=modulo:
        ORDEM_BLOCOS[modulo].index(registro[0][0]) * 1000 + int(registro[0][1:4])
    )

    objeto_registros.clear()
    objeto_registros.update(itens_ordenados)



    ultimos_registros: list[str | None] = [None for _ in range(MAIOR_NIVEL + 1)]
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










def converter_campos(modulo: ModuloT, arquivo_campos: str, objeto_registros: dict[str, RegistroT]):
    with open(arquivo_campos, encoding="utf-8", newline="") as ac:
        csv_campos = csv.DictReader(ac)

        if csv_campos.fieldnames != COLUNAS[modulo]["campos"]:
            raise ValueError(f"Colunas inválidas no arquivo de campos do módulo {modulo}")

        for linha_campos in csv_campos:
            assert len(linha_campos) == len(COLUNAS[modulo]["campos"]), ("campos", modulo, linha_campos)
            assert all(campo is not None for campo in linha_campos.values())

            nome_registro = linha_campos["Register"]

            # NOTE: Os campos "Entr" e "Saídas" podem ser usados para identificar a obrigatoriedade geral de um campo apenas quando ambos forem "O"
            campo_obrigatorio = linha_campos["Obrig"] == "O" or (
                "Entr" in linha_campos and
                "Saídas" in linha_campos and
                linha_campos["Entr"] == "O" and
                linha_campos["Saídas"] == "O"
            )



            # Por enquanto não há distinção entre N e NS (NUMÉRICO SINALIZADO), mas possivelmente haverá no futuro
            if linha_campos["Tipo"] == "NS":
                linha_campos["Tipo"] = "N"

            # Testa se o tipo de campo é um dos valores válidos
            assert linha_campos["Tipo"] in ("C", "N"), f"Tipo inesperado: {linha_campos['Tipo']}"
            tipo_campo: CampoTipoT = linha_campos["Tipo"]
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
        modulo: ModuloT
        modulo, leiaute, manual = Path(caminho).parts  # type: ignore


        json_convertido = conversor(modulo, leiaute, manual.replace(".", "_"))


        pasta_destino = os.path.join("src", "escriturador_sped", "modulos", modulo, f"l{leiaute}", f"m{manual.replace('.', '_')}")
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        with open(os.path.join(pasta_destino, "modulo.json"), "w", encoding="utf-8") as arquivo_convertido:
            arquivo_convertido.write(json.dumps(json_convertido, indent=JSON_INDENTACAO if formatado else None, ensure_ascii=False))










if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte os módulos SPED para o formato usado pela biblioteca")
    parser.add_argument("--formatado", action="store_true", help="Gera o arquivo com uma formatação ao invés de ser minimizado")
    args = parser.parse_args()

    main(args.formatado)
