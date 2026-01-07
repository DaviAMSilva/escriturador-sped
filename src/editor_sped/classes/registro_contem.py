from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Iterable, Iterator

from ..types import EfdTipo
from .registro_lista import ListaRegistro

if TYPE_CHECKING:
    from .registro import Registro









class ContemRegistros(ABC):
    def __init__(self, nome: str, filhos: ListaRegistro, efd_tipo: EfdTipo) -> None:
        self.nome: str = nome
        self.filhos: ListaRegistro = filhos
        self.efd_tipo: EfdTipo = efd_tipo



    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    def __len__(self) -> int:
        return self.tamanho

    def __iter__(self) -> Iterator:
        return iter(self.filhos)



    @abstractmethod
    def texto(self) -> str: ...

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
        campos: dict[str | int, str | int | float | None | Iterable[str | int | float | None]] | None = None,
        *,
        campos_c: dict[str | int, str | Iterable[str]] | None = None,
        campos_n: dict[str | int, int | float | None | Iterable[int | float | None]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
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
        campos: dict[str | int, str | int | float | None | Iterable[str | int | float | None]] | None = None,
        *,
        campos_c: dict[str | int, str | Iterable[str]] | None = None,
        campos_n: dict[str | int, int | float | None | Iterable[int | float | None]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo=True
    ) -> "Registro":
        encontrado = self.filhos.pesquisar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro pesquisado não foi encontrado") from e
