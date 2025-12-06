import json
import re
from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, overload

from ..classes.bloco import Bloco
from ..classes.registro import Registro
from ..ler_registros import ler_registros
from ..tabelas import EFD_INFO
from ..types import EfdTipo
from ..utilidades import remover_assinatura_escrituracao
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Escrituracao(ContemRegistros, ABC):
    def __init__(self, escrituracao_texto: str, nome: str, efd_tipo: EfdTipo) -> None:
        super().__init__(nome, efd_tipo, ListaRegistro())

        self.blocos: dict[str, Bloco] = {}

        self.abertura: Registro
        self.fechamento: Registro

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self._ler_escrituracao(escrituracao_texto)



    @overload
    def __getitem__(self, chave: int) -> "Registro": ...

    @overload
    def __getitem__(self, chave: str | re.Pattern | Callable[["Registro"], bool] | slice | None) -> "ListaRegistro": ...

    def __getitem__(self, chave):
        if isinstance(chave, (int, slice)):
            return self.pesquisar()[chave]

        if isinstance(chave, (str, re.Pattern, Callable)) or chave is None:
            return self.pesquisar(chave)

        raise ValueError(f"Valor de pesquisa inválido ({chave})")



    def json(self, *args, indent=4, ensure_ascii=False, **kwargs) -> str:
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj.serialize(), *args, **kwargs)



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    def _ler_escrituracao(self, escrituracao_texto: str) -> None:
        registros_raizes = ler_registros(escrituracao_texto, self.efd_tipo)



        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise SyntaxError(f"Escrituração mal formatada ({registros_raizes})")



        # Informação da escrituração em si
        self.filhos = registros_raizes
        [self.abertura, self.fechamento] = registros_raizes



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
                registro_bloco_fechamento.campos[2].configurar_valor(partial(lambda b: str(b.tamanho), self.blocos[bloco_info["nome"]]))
            elif registro_bloco_abertura is not None or registro_bloco_fechamento is not None:
                # Apenas um dos registros de abertura ou fechamento existe
                raise TypeError(f"Apenas um dos registros de abertura |{registro_bloco_abertura.nome if registro_bloco_abertura else None}|" +
                                f" ou fechamento |{registro_bloco_fechamento.nome if registro_bloco_fechamento else None}| existe")

        # Adicionando o cálculo dinâmico do tamanho da escrituração para o registro de fechamento
        self.fechamento.campos[2].configurar_valor(partial(lambda e: str(e.tamanho), self))



    def totalizar_9900(self):
        # Encontrando todos os nomes de registros presentes na escrituração
        registro_9001 = self.pesquisar("9001")[0]

        registros_9900 = registro_9001.pesquisar("9900")
        registros_9900_blc = [registro_9900["REG_BLC"].valor_c for registro_9900 in registros_9900]

        registros_encontrados = set()
        for registro in self.pesquisar():
            nome = registro.nome
            registros_encontrados.add(nome)



        # Removendo os registros os que não existem mais
        registros_9900_remover = []

        for registro_9900 in registros_9900:
            registro_nome = registro_9900["REG_BLC"].valor_c
            if registro_nome in registros_encontrados:
                if not registro_9900["QTD_REG_BLC"].valor_configurado:
                    registro_9900["QTD_REG_BLC"].configurar_valor(partial(lambda e, rn: len(e.pesquisar(rn)), self, registro_nome))
            else:
                registros_9900_remover.append(registro_9900)

        for registro_9900_remover in registros_9900_remover:
            registro_9001.filhos.remove(registro_9900_remover)



        # Adicionando novos registros 9900 que não existiam antes
        for registro_nome in registros_encontrados:
            if registro_nome not in registros_9900_blc:
                novo_registro_9900 = Registro(f"|9900|{registro_nome}||", self.efd_tipo)
                novo_registro_9900["QTD_REG_BLC"].configurar_valor(partial(lambda e, rn: len(e.pesquisar(rn)), self, registro_nome))
                registro_9001.filhos.append(novo_registro_9900)



        # Atualizando ou adicionando o Registro |9900|9900|
        registro_9900_9900 = self.blocos["9"].pesquisar(lambda r: (r.nome == "9900" and r["REG_BLC"].valor_c == "9900"))
        registro_9900_9900 = registro_9900_9900[0] if registro_9900_9900 else None

        if registro_9900_9900:
            registro_9900_9900["QTD_REG_BLC"].valor = len(self.blocos["9"].pesquisar("9900"))
        else:
            novo_registro_9900_9900 = Registro(f"|9900|9900|{len(self.blocos['9'].pesquisar('9900')) + 1}|", self.efd_tipo)
            registro_9001.filhos.append(novo_registro_9900_9900)










class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto: str) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")



class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto: str) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")
