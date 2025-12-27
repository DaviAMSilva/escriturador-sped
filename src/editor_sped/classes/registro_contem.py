from abc import ABC
from typing import TYPE_CHECKING, Callable

from ..types import EfdTipo
from .registro_lista import ListaRegistro

if TYPE_CHECKING:
    from .registro import Registro









class ContemRegistros(ABC):
    def __init__(self, nome: str, efd_tipo: EfdTipo, filhos: ListaRegistro) -> None:
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
    def registros(self) -> ListaRegistro:
        return self.pesquisar()



    def pesquisar(
        self,
        nome: str | None = None,
        campos: dict[str | int, str | int | float | None] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        *,
        campos_c: dict[str | int, str] | None = None,
        campos_n: dict[str | int, int | float | None] | None = None,
        recursivo=True,
        primeiro=False
    ) -> "ListaRegistro":
        return self.filhos.pesquisar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=primeiro
        )

    def primeiro(
        self,
        nome: str | None = None,
        campos: dict[str | int, str | int | float | None] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        *,
        campos_c: dict[str | int, str] | None = None,
        campos_n: dict[str | int, int | float | None] | None = None,
        recursivo=True
    ) -> "Registro":
        encontrado = self.pesquisar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro pesquisado não foi encontrado") from e
