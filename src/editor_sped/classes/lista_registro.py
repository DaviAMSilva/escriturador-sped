import re
from typing import TYPE_CHECKING, Iterable, SupportsIndex, overload

if TYPE_CHECKING:
    from editor_sped.classes.registro import Registro



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
    def __getitem__(self, chave: slice) -> list["Registro"]: ...

    @overload
    def __getitem__(self, chave: str | re.Pattern | tuple[str | None, bool] | None) -> "ListaRegistro": ...

    def __getitem__(self, chave):
        if isinstance(chave, (SupportsIndex, slice)):
            return super().__getitem__(chave)

        resultados = ListaRegistro()

        if isinstance(chave, tuple) and len(chave) == 2:
            for registro in self:
                resultados.extend(registro.pesquisar(chave[0], chave[1]))

        if isinstance(chave, str) or chave is None:
            for registro in self:
                resultados.extend(registro.pesquisar(chave))

        return resultados
