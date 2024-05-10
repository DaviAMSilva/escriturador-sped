import json

from ..utilidades import limpar_escrituracao
from .bloco import Bloco
from .campo import Campo
from .registro import Registro










class Escrituracao:
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



    def ler_blocos(self, escrituracao_texto):
        if type(escrituracao_texto) == str:
            escrituracao_texto = limpar_escrituracao(escrituracao_texto).splitlines()



        # Removendo a assinatura ou informações extra se existirem

        if (not escrituracao_texto[0].startswith("|0000|")):
            raise ValueError("Escrituração não começa com registro |0000|")

        if (not escrituracao_texto[-1].startswith("|9999|")):
            raise ValueError("Escrituração não termina com registro |9999|")



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
