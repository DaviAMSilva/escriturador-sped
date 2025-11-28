import re
from typing import TYPE_CHECKING, Callable, Iterable, SupportsIndex, overload

if TYPE_CHECKING:
    from .registro import Registro










class ListaRegistro(list["Registro"]):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iteravel: Iterable["Registro"]) -> None: ...

    def __init__(self, iteravel=()) -> None:
        super().__init__(iteravel)



    @overload
    def __getitem__(self, chave: SupportsIndex | int) -> "Registro": ...

    @overload
    def __getitem__(self, chave: str | re.Pattern | slice | None) -> "ListaRegistro": ...

    def __getitem__(self, chave):
        if isinstance(chave, (SupportsIndex, int)):
            return super().__getitem__(chave)

        if isinstance(chave, slice):
            return ListaRegistro(super().__getitem__(chave))

        if isinstance(chave, (str, re.Pattern)) or chave is None:
            return self.pesquisar(chave)

        raise TypeError(f"Valor inválido ({chave})")



    def pesquisar(self, chave: str | re.Pattern | Callable[["Registro"], bool] | None = None) -> "ListaRegistro":
        # Se for apenas um caractere o caso especial é pesquisar todos desse bloco
        if isinstance(chave, str) and len(chave) == 1:
            chave += "..."

        resultados = ListaRegistro()

        if isinstance(chave, (str, re.Pattern)):
            for filho in self:
                if re.compile(chave).fullmatch(filho.nome):
                    resultados.append(filho)
                if filho.contem_filhos:
                    resultados.extend(filho.pesquisar(chave))
            return resultados

        if callable(chave):
            for filho in self:
                if chave(filho):
                    resultados.append(filho)
                if filho.contem_filhos:
                    resultados.extend(filho.pesquisar(chave))
            return resultados

        if chave is None:
            for filho in self:
                resultados.append(filho)
                if filho.contem_filhos:
                    resultados.extend(filho.pesquisar(chave))
            return resultados

        raise TypeError(f"Valor de chave inválido ({chave})")

    def filtrar(self, filtro: str | re.Pattern | Callable[["Registro"], bool] | None = None):
        resultados = ListaRegistro()

        if isinstance(filtro, (str, re.Pattern)):
            for filho in self:
                if re.compile(filtro).fullmatch(filho.nome):
                    resultados.append(filho)
            return resultados

        if callable(filtro):
            for filho in self:
                if filtro(filho):
                    resultados.append(filho)
            return resultados

        if filtro is None:
            return ListaRegistro(self)

        raise TypeError(f"Valor de filtro inválido ({filtro})")



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(r.nome for r in self))
