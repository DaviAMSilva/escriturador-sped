from typing import Callable

from ..tabelas import EFD_INFO
from ..types import EfdTipo










class Campo:
    def __init__(self, valor: str, registro_nome: str, numero: int, efd_tipo: EfdTipo) -> None:
        self.__valor: str = valor

        self.__retorna_valor: Callable[[], str] = None

        self.efd_tipo: EfdTipo = efd_tipo

        info_campos = EFD_INFO[efd_tipo]["registros"][registro_nome]["campos"][numero - 1]

        # fmt: off
        self.nome          = info_campos["nome"]
        self.descricao     = info_campos["descricao"]

        self.decimal       = info_campos["decimal"]
        self.numero        = info_campos["numero"]
        self.obrigatorio   = info_campos["obrigatorio"]
        self.tamanho       = info_campos["tamanho"]
        self.tamanho_exato = info_campos["tamanho_exato"]
        self.tipo          = info_campos["tipo"]
        # fmt: on



    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Campo({self.nome})"



    def serialize(self) -> str:
        return self.valor



    def texto(self) -> str:
        return self.valor



    @property
    def valor(self) -> str:
        return self.__retorna_valor() if self.__retorna_valor else self.__valor

    @valor.setter
    def valor(self, valor) -> str:
        self.__valor = valor



    def configurar_valor(self, retorna_valor: Callable[[], str]) -> None:
        if not isinstance(retorna_valor, Callable):
            raise ValueError(f"O parâmetro '{retorna_valor}' não é uma função")

        self.__retorna_valor = retorna_valor
