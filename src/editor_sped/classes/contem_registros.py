from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .registro import Registro
    from ..types import EfdTipo



class ContemRegistros(ABC):
    def __init__(self, nome: str, efd_tipo: "EfdTipo", filhos: list["Registro"]) -> None:
        self.nome: str = nome
        self.efd_tipo: EfdTipo = efd_tipo
        self.filhos: list[Registro] = filhos

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
        return sum(f.tamanho for f in self.filhos)

    @property
    def contem_filhos(self) -> bool:
        return len(self.filhos) >= 1
