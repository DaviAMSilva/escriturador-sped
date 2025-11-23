import re
from abc import ABC
from typing import TYPE_CHECKING, SupportsIndex, overload

from ..classes.lista_registro import ListaRegistro
from ..types import EfdTipo

if TYPE_CHECKING:
    from ..classes.registro import Registro


class ContemRegistros(ABC):
    def __init__(self, nome: str, efd_tipo: "EfdTipo", filhos: ListaRegistro) -> None:
        self.nome: str = nome
        self.efd_tipo: EfdTipo = efd_tipo
        self.filhos: ListaRegistro = ListaRegistro(filhos)

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.nome})"

    def __len__(self) -> int:
        return self.tamanho



    @overload
    def __getitem__(self, chave: SupportsIndex | int) -> "Registro": ...

    @overload
    def __getitem__(self, chave: str | re.Pattern | slice | None) -> "ListaRegistro": ...

    def __getitem__(self, chave):
        if isinstance(chave, slice):
            return ListaRegistro(self.pesquisar()[chave])
        
        if isinstance(chave, (SupportsIndex, int)):
            return self.pesquisar()[chave]

        if isinstance(chave, (str, re.Pattern)) or chave is None:
            return self.pesquisar(chave)

        raise ValueError(f"Valor de pesquisa inválido ({chave})")



    def serialize(self) -> dict:
        return {"nome": self.nome, "filhos": self.filhos}



    @property
    def tamanho(self) -> int:
        return sum(f.tamanho for f in self.filhos)

    @property
    def contem_filhos(self) -> bool:
        return len(self.filhos) >= 1



    def pesquisar(self, chave: str | re.Pattern | None = None) -> "ListaRegistro":
        # Se for apenas um caractere o caso especial é pesquisar todos desse bloco
        if isinstance(chave, str) and len(chave) == 1:
            chave += "..."

        regex = re.compile(chave) if isinstance(chave, str) else chave

        resultados = ListaRegistro()

        for filho in self.filhos:
            if regex is None or regex.fullmatch(filho.nome):
                resultados.append(filho)
            resultados.extend(filho.pesquisar(chave))

        return resultados
