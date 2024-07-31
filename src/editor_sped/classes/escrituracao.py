import json

from ..utilidades import remover_assinatura_escrituracao
from ..ler_registros import ler_registros










class Escrituracao:
    LISTA_BLOCOS = None

    def __init__(self, escrituracao_texto, nome, tipo_efd) -> None:
        self.__nome = nome
        self.__tipo_efd = tipo_efd
        self.blocos = {}

        self.abertura = None
        self.fechamento = None

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self.__ler_escrituracao(escrituracao_texto)



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



    def __ler_escrituracao(self, escrituracao_texto):
        registros_raizes = ler_registros(escrituracao_texto, self.__tipo_efd)

        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise ValueError(f"Escrituração mal formatada ({registros_raizes})")

        self.abertura = registros_raizes[0]
        self.fechamento = registros_raizes[1]

        self.filhos = [self.abertura, self.fechamento]












class EscrituracaoPISCOFINS(Escrituracao):
    LISTA_BLOCOS = None # FIXME

    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")



class EscrituracaoICMSIPI(Escrituracao):
    LISTA_BLOCOS = None # FIXME

    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")
