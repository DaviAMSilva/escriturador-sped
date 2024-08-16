import json

from ..utilidades import remover_assinatura_escrituracao
from ..ler_registros import ler_registros










class Escrituracao:
    def __init__(self, escrituracao_texto, nome, tipo_efd) -> None:
        self.nome = nome
        self.tipo_efd = tipo_efd
        self.blocos = {}

        self.abertura = None
        self.fechamento = None

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self.__ler_escrituracao(escrituracao_texto)



    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Escrituracao({self.nome})"

    def _json(self):
        return {"nome": self.nome, "filhos": self.filhos}



    @property
    def tamanho(self) -> str:
        return sum(f.tamanho for f in self.filhos)



    def json(self, indent=4, ensure_ascii=False, *args, **kwargs):
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj._json(), *args, **kwargs)



    def texto(self):
        return \
            self.abertura.texto() + \
            self.fechamento.texto()



    def __ler_escrituracao(self, escrituracao_texto):
        registros_raizes = ler_registros(escrituracao_texto, self.tipo_efd)

        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise ValueError(f"Escrituração mal formatada ({registros_raizes})")

        self.abertura = registros_raizes[0]
        self.fechamento = registros_raizes[1]

        self.filhos = [self.abertura, self.fechamento]












class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")



class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")
