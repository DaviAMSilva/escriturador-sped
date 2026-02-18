from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Iterable, Iterator

from ..efd_info import EfdTipo
from .campo import Alfanumerico, Chave, Numerico
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

    def __iter__(self) -> Iterator["Registro"]:
        return iter(self.filhos)



    @abstractmethod
    def texto(self) -> str: ...



    @property
    def tamanho(self) -> int:
        return sum(filho.tamanho for filho in self.filhos)

    @property
    def registros(self) -> ListaRegistro:
        return self.buscar()



    def buscar(
        self,
        nome: str | None = None,
        campos: dict[Chave, Alfanumerico | Numerico | Iterable[Alfanumerico | Numerico]] | None = None,
        *,
        campos_c: dict[Chave, Alfanumerico | Iterable[Alfanumerico]] | None = None,
        campos_n: dict[Chave, Numerico | Iterable[Numerico]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo=True,
        primeiro=False
    ) -> "ListaRegistro":
        return self.filhos.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=primeiro
        )

    def primeiro(
        self,
        nome: str | None = None,
        campos: dict[Chave, Alfanumerico | Numerico | Iterable[Alfanumerico | Numerico]] | None = None,
        *,
        campos_c: dict[Chave, Alfanumerico | Iterable[Alfanumerico]] | None = None,
        campos_n: dict[Chave, Numerico | Iterable[Numerico]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo=True
    ) -> "Registro":
        encontrado = self.filhos.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro pesquisado não foi encontrado") from e
