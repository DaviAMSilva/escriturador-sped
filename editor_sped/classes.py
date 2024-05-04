import json
from abc import ABC
from typing import *

from .tabelas import EFD_INFO
from .constantes import EFD_MAIOR_NIVEL










class Campo:
    def __init__(self, valor, registro, numero, tipo_efd) -> str:
        self.numero = numero
        self.valor = valor

        # OTIMIZAR AQUI
        # multiprocessing?

        self.tipo_efd = tipo_efd
        self.__nome = EFD_INFO[self.tipo_efd][registro]["campos"][self.numero - 1]["nome"]
        # self.__nome = df_campos.loc[(registro, self.numero), "code"]




    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Campo({self.__nome})"



    def _json_registros(self):
        return self.valor



    @property
    def nome(self) -> str:
        return self.__nome










class Registro:
    def __init__(self, campos_texto: str | List[str], nivel, nome_bloco, tipo_efd) -> None:
        self.campos = []
        self.filhos = []
        self.pai = None

        self.nivel = nivel

        if type(campos_texto) == str:
            campos_texto = campos_texto.split("|")[1:-1]

        self.bloco = nome_bloco

        # OTIMIZAR AQUI
        # multiprocessing?

        self.__nome = campos_texto[0]
        self.tipo_efd = tipo_efd
        self.campos.extend([Campo(campo, self.__nome, i + 1, self.tipo_efd) for i, campo in enumerate(campos_texto)])



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Registro({self.__nome})"



    def _json_registros(self):
        if self.contem_filhos:
            return {"campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": self.filhos}
        else:
            return f"|{'|'.join([str(c) for c in self.campos])}|"



    def converter_para_texto(self):
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{"".join([f.converter_para_texto() for f in self.filhos])}"



    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def contem_filhos(self):
        return len(self.filhos) >= 1










class Bloco:
    def __init__(self, nome_bloco, registros_texto: str | List[str], tipo_efd) -> None:
        self.registro_inicial = None
        self.registro_final = None

        self.__nome = nome_bloco
        self.tipo_efd = tipo_efd

        if type(registros_texto) == str:
            registros_texto = registros_texto.split("\n")

        if (not registros_texto[0].startswith(f"|{self.__nome}001|")) or (not registros_texto[-1].startswith(f"|{self.__nome}990|")):
            raise ValueError("Bloco não começa e termina com |_001| e |_990|")

        self.registro_inicial = Registro(registros_texto.pop(0), 1, self.__nome, self.tipo_efd)
        self.registro_final = Registro(registros_texto.pop(-1), 1, self.__nome, self.tipo_efd)

        self.filhos = [self.registro_inicial, self.registro_final]

        self.ler_registros(registros_texto)



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Bloco({self.__nome})"

    def _json_registros(self):
        return {"nome": self.__nome, "filhos": self.filhos}



    @property
    def nome(self) -> str:
        return self.__nome



    def ler_registros(self, registros_texto):
        # self.registros = self.registro_inicial.filhos

        # Lista do último registro visitado em cada nível
        ultimos_registros = [None for _ in range(EFD_MAIOR_NIVEL + 1)]
        ultimos_registros[1] = self.registro_inicial
        nivel_anterior = 1

        # Para cada registro informado
        for registro_atual in registros_texto:
            # Pega o nome do registro e encontra o seu nível dentro da tabela
            nivel_atual = EFD_INFO[self.tipo_efd][registro_atual.split("|")[1]]["nivel"]

            # Compara o nível do registro anterior com o nível do registro atual
            if nivel_atual > nivel_anterior + 1:
                # Se a diferença entre o nível anterior e o atual for maior que 1 positivo há um erro de estrutura
                raise ValueError(f"Registros foram da ordem válida. De ${nivel_anterior} para ${nivel_atual}")
            elif nivel_atual == nivel_anterior + 1 or nivel_atual <= nivel_anterior:
                ultimos_registros[nivel_atual] = Registro(registro_atual, nivel_atual, self.__nome, self.tipo_efd)

            # Adicionamos o registro atual como filho do registro acima dele (nível - 1)
            # De maneira inversa criamos a ligação do registro filho com o registro pai
            ultimos_registros[nivel_atual - 1].filhos.append(ultimos_registros[nivel_atual])
            ultimos_registros[nivel_atual].pai = ultimos_registros[nivel_atual - 1]

            # O nível anterior foi alterado
            nivel_anterior = nivel_atual










class Escrituracao(ABC):
    def __init__(self, escrituracao_texto, nome, tipo_efd) -> None:
        self.__nome = nome
        self.tipo_efd = tipo_efd
        self.blocos = {}

        self.registro_inicial = None
        self.registro_final = None

        self.filhos = []

        self.importar_escrituracao(escrituracao_texto)



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Escrituracao({self.__nome})"

    def _json_registros(self):
        return {"nome": self.__nome, "filhos": self.filhos}



    @property
    def nome(self) -> str:
        return self.__nome



    def importar_escrituracao(self, escrituracao_texto):
        if escrituracao_texto and escrituracao_texto != "":
            self.ler_blocos(escrituracao_texto)


    def converter_para_json(self, indent=4, ensure_ascii=False, *args, **kwargs):
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj._json_registros(), *args, **kwargs)


    def converter_para_texto(self):
        return \
            self.registro_inicial.converter_para_texto() + \
            self.registro_final.converter_para_texto()



    def ler_blocos(self, escrituracao_texto: str | List[str]):
        # Esperando List[str], mas aceita str também
        if type(escrituracao_texto) == str:
            escrituracao_texto = escrituracao_texto.splitlines()

        if (not escrituracao_texto[0].startswith("|0000|")):
            raise ValueError("Escrituração não começa com registro |0000|")

        for i, linha in enumerate(reversed(escrituracao_texto)):
            campos = linha.split("|")

            # Percorre o arquivo ao contrário até achar o registro 9999 e verifica se a quantidade de linhas está correta
            # Caso não ache o registro retorno um erro
            if len(campos) > 1 and campos[1] == "9999":
                if len(escrituracao_texto) - i != int(campos[2]):
                    raise ValueError(f"Escrituração com número de linhas diferente do campo QTD_LIN do registro |9999|: (len:{len(campos)} != QTD_LIN:{campos[2]})")
                break
        else:
            raise ValueError("Escrituração não contém registro |9999|")



        self.registro_inicial = Registro(escrituracao_texto.pop(0), 0, "0", self.tipo_efd)
        self.registro_final = Registro(escrituracao_texto.pop(-1), 0, "9", self.tipo_efd)

        self.filhos = [self.registro_inicial, self.registro_final]

        blocos_temp = {}

        for linha in escrituracao_texto:
            if linha == "" or linha == "\n":
                continue

            nome_bloco = linha[1]

            # Chegamos no final do arquivo
            if linha.split("|")[1] == "9999":
                break

            if not nome_bloco in blocos_temp:
                blocos_temp[nome_bloco] = []

            blocos_temp[nome_bloco].append(linha)

        for k_nome_bloco, v_registros_texto in blocos_temp.items():
            self.blocos[k_nome_bloco] = Bloco(k_nome_bloco, v_registros_texto, self.tipo_efd)
            self.registro_inicial.filhos.append(self.blocos[k_nome_bloco].registro_inicial)
            self.registro_inicial.filhos.append(self.blocos[k_nome_bloco].registro_final)

            self.blocos[k_nome_bloco].registro_inicial.pai = self.registro_inicial










class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")










class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")
