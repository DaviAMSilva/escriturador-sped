from inspect import signature
from typing import TYPE_CHECKING, Callable

from ..tabelas import EFD_INFO
from ..types import EfdTipo

# Útil para evitar importações circulares
if TYPE_CHECKING:
    from ..classes.registro import Registro










class Campo:
    def __init__(self, valor: str, registro_pai: "Registro", numero: int, efd_tipo: EfdTipo) -> None:
        self._valor: str = valor

        self.__retorna_valor: Callable[[], str] | None = None

        self.efd_tipo: EfdTipo = efd_tipo
        self.registro_pai = registro_pai

        info_campos = EFD_INFO[efd_tipo]["registros"][self.registro_pai.nome]["campos"][numero - 1]

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
        return self.__retorna_valor() if self.__retorna_valor else self._valor

    @valor.setter
    def valor(self, valor) -> str:
        self._valor = valor
        return valor



    def configurar_valor(self, retorna_valor: Callable[[], str]) -> None:
        # Verifica se retorna_valor é uma função sem argumentos e retorna str
        if not callable(retorna_valor):
            raise ValueError(f"O parâmetro '{retorna_valor}' não é uma função")

        sig = signature(retorna_valor)
        if len(sig.parameters) != 0:
            raise TypeError("A função fornecida deve ser sem argumentos")
        if sig.return_annotation not in (str, sig.empty):
            raise TypeError("A função fornecida deve retornar uma string (str)")

        self.__retorna_valor = retorna_valor
