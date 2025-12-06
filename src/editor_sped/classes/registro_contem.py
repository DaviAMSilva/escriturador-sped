import re
from abc import ABC
from typing import TYPE_CHECKING, Callable

from ..types import EfdTipo
from .registro_lista import ListaRegistro

if TYPE_CHECKING:
    from .registro import Registro









class ContemRegistros(ABC):
    def __init__(self, nome: str, efd_tipo: "EfdTipo", filhos: ListaRegistro) -> None:
        self.nome: str = nome
        self.efd_tipo: EfdTipo = efd_tipo
        self.filhos: ListaRegistro = filhos

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.nome})"

    def __len__(self) -> int:
        return self.tamanho



    def serialize(self) -> dict:
        return {"nome": self.nome, "filhos": self.filhos}



    @property
    def tamanho(self) -> int:
        return sum(filho.tamanho for filho in self.filhos)

    @property
    def contem_filhos(self) -> bool:
        return len(self.filhos) >= 1

    @property
    def registros(self) -> ListaRegistro:
        resultados = ListaRegistro()

        for filho in self.filhos:
            resultados.append(filho)
            resultados.extend(filho.pesquisar())

        return resultados



    def pesquisar(self, chave: str | re.Pattern | Callable[["Registro"], bool] | None = None) -> "ListaRegistro":
        return self.filhos.pesquisar(chave)
