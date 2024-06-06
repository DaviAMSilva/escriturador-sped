import json

from ..utilidades import remover_assinatura_escrituracao
from .bloco import Bloco
from .campo import Campo
from .registro import Registro










class Escrituracao:
    def __init__(self, escrituracao_texto, nome, tipo_efd) -> None:
        self.__nome = nome
        self.__tipo_efd = tipo_efd
        self.blocos = {}

        self.abertura = None
        self.fechamento = None



        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto).splitlines()



        if (not escrituracao_texto[0].startswith("|0000|")):
            raise ValueError("Escrituração não começa com registro |0000|")

        if (not escrituracao_texto[-1].startswith("|9999|")):
            raise ValueError("Escrituração não termina com registro |9999|")



        self.abertura = Registro(escrituracao_texto.pop(0), "0", self.__tipo_efd)
        self.fechamento = Registro(escrituracao_texto.pop(-1), "9", self.__tipo_efd)

        self.filhos = [self.abertura, self.fechamento]



        self.ler_blocos(escrituracao_texto)



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Escrituracao({self.__nome})"

    def _json_registros(self):
        return {"nome": self.__nome, "filhos": self.filhos}



    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def tipo_efd(self) -> str:
        return self.__tipo_efd

    @property
    def tamanho(self) -> str:
        return sum(f.tamanho for f in self.filhos)



    def converter_para_json(self, indent=4, ensure_ascii=False, *args, **kwargs):
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj._json_registros(), *args, **kwargs)


    def converter_para_texto(self):
        return \
            self.abertura.converter_para_texto() + \
            self.fechamento.converter_para_texto()



    def ler_blocos(self, escrituracao_texto):
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
            self.blocos[k_nome_bloco] = Bloco(k_nome_bloco, v_registros_texto, self.__tipo_efd)
            self.abertura.filhos.append(self.blocos[k_nome_bloco].abertura)
            self.abertura.filhos.append(self.blocos[k_nome_bloco].fechamento)

            self.blocos[k_nome_bloco].abertura.pai = self.abertura










class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")



class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")
