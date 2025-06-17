import json
from abc import ABC, abstractmethod
from functools import partial

from ..classes.bloco import Bloco
from ..classes.registro import Registro
from ..ler_registros import ler_registros
from ..tabelas import EFD_INFO
from ..types import EfdTipo
from ..utilidades import remover_assinatura_escrituracao










class Escrituracao(ABC):
    @abstractmethod
    def __init__(self, escrituracao_texto, nome: str, efd_tipo: EfdTipo) -> None:
        self.nome = nome
        self.efd_tipo: EfdTipo = efd_tipo
        self.blocos: dict[str, Bloco] = {}

        self.abertura: Registro
        self.fechamento: Registro

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self.__ler_escrituracao(escrituracao_texto)



    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Escrituracao({self.nome})"

    def serialize(self) -> dict:
        return {"nome": self.nome, "filhos": self.filhos}



    @property
    def tamanho(self) -> int:
        return sum(f.tamanho for f in self.filhos)



    def json(self, *args, indent=4, ensure_ascii=False, **kwargs) -> str:
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj.serialize(), *args, **kwargs)



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    def __ler_escrituracao(self, escrituracao_texto: str) -> None:
        registros_raizes = ler_registros(escrituracao_texto, self.efd_tipo)



        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise ValueError(f"Escrituração mal formatada ({registros_raizes})")



        # Informação da escrituração em si
        self.filhos = registros_raizes
        [self.abertura, self.fechamento] = registros_raizes  # pylint: disable=unbalanced-tuple-unpacking



        # Preenchendo as informações dos blocos
        for bloco_info in EFD_INFO[self.efd_tipo]["blocos"]:
            registro_bloco_abertura: Registro | None = None
            registro_bloco_fechamento: Registro | None = None



            # Encontrando os registros de abertura e fechamento na lista de registros
            # Esse método encontra apenas os blocos presentes na escrituração atual,
            # não levando em consideração as condições de obrigatoriedade de blocos
            for escrituracao_registro in self.abertura.filhos:
                if escrituracao_registro.nome == bloco_info["abertura"]:
                    registro_bloco_abertura = escrituracao_registro
                    break

            for escrituracao_registro in self.abertura.filhos:
                if escrituracao_registro.nome == bloco_info["fechamento"]:
                    registro_bloco_fechamento = escrituracao_registro
                    break

            if registro_bloco_abertura and registro_bloco_fechamento:
                # Criando o bloco com os blocos de abertura e fechamento
                self.blocos[bloco_info["nome"]] = Bloco(bloco_info["nome"], registro_bloco_abertura, registro_bloco_fechamento, self.efd_tipo)

                # Adicionando o cálculo dinâmico dos tamanhos dos blocos para os registros de fechamento
                registro_bloco_fechamento.campos[1].configurar_valor(partial(lambda b: str(b.tamanho), self.blocos[bloco_info["nome"]]))
            elif registro_bloco_abertura is not None or registro_bloco_fechamento is not None:
                # Apenas um dos registros de abertura ou fechamento existe
                raise ValueError(f"Apenas um dos registros de abertura |{registro_bloco_abertura.nome if registro_bloco_abertura else None}|" +
                                 f" ou fechamento |{registro_bloco_fechamento.nome if registro_bloco_fechamento else None}| existe")

        # Adicionando o cálculo dinâmico do tamanho da escrituração para o registro de fechamento
        self.fechamento.campos[1].configurar_valor(partial(lambda e: str(e.tamanho), self))












class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto):
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")



class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto):
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")
