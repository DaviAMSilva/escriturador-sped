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
            resultados = ListaRegistro()

            for registro in self:
                resultados.extend(registro.pesquisar(chave))

            return resultados

        raise TypeError(f"Valor inválido ({chave})")



    def pesquisar(self, chave: str | re.Pattern | None = None) -> "ListaRegistro":
        # Se for apenas um caractere o caso especial é pesquisar todos desse bloco
        if isinstance(chave, str) and len(chave) == 1:
            chave += "..."

        regex = re.compile(chave) if isinstance(chave, str) else chave

        resultados = ListaRegistro()

        for filho in self:
            if regex is None or regex.fullmatch(filho.nome):
                resultados.append(filho)
            resultados.extend(filho.pesquisar(chave))

        return resultados

    def filtrar(self, filtro: str | re.Pattern | Callable[["Registro"], bool]):
        resultados = ListaRegistro()

        if isinstance(filtro, (str, re.Pattern)):
            regex = re.compile(filtro) if isinstance(filtro, str) else filtro

            for registro in self:
                if regex.fullmatch(registro.nome):
                    resultados.append(registro)

            return resultados

        if callable(filtro):
            for registro in self:
                if filtro(registro):
                    resultados.append(registro)

            return resultados

        raise TypeError(f"Valor de filtro inválido ({filtro})")



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(r.nome for r in self)
