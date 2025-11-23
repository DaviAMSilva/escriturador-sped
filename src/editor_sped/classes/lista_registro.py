import re
from typing import TYPE_CHECKING, Iterable, SupportsIndex, overload

if TYPE_CHECKING:
    from ..classes.registro import Registro



class ListaRegistro(list["Registro"]):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iteravel: Iterable["Registro"], /) -> None: ...

    def __init__(self, iteravel=None) -> None:
        if iteravel:
            super().__init__(iteravel)
        else:
            super().__init__()



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

        raise ValueError(f"Valor de pesquisa inválido ({chave})")
