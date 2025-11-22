import re
from abc import ABC
from typing import TYPE_CHECKING

from editor_sped.classes.lista_registro import ListaRegistro
from editor_sped.types import EfdTipo

if TYPE_CHECKING:
    from editor_sped.classes.registro import Registro



class ContemRegistros(ABC):
    def __init__(self, nome: str, efd_tipo: "EfdTipo", filhos: list["Registro"]) -> None:
        self.nome: str = nome
        self.efd_tipo: EfdTipo = efd_tipo
        self.filhos = ListaRegistro(filhos)

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.nome})"

    def __len__(self) -> int:
        return self.tamanho

    def __getitem__(self, chave: str | tuple[str | None, bool] | None):
        if isinstance(chave, tuple) and len(chave) == 2:
            return self.pesquisar(chave[0], chave[1])

        if isinstance(chave, str) or chave is None:
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

    def pesquisar(self, chave: str | re.Pattern | None = None, recursivo: bool = False):
        regex = re.compile(chave) if isinstance(chave, str) else chave

        if recursivo:
            resultados = ListaRegistro()
            for filho in self.filhos:
                if regex is None or regex.fullmatch(filho.nome):
                    resultados.append(filho)
                resultados.extend(filho.pesquisar(chave, recursivo=True))
            return resultados

        return ListaRegistro(r for r in self.filhos if regex is None or regex.fullmatch(r.nome))
