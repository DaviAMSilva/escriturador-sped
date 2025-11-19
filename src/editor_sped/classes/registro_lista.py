from typing import Any, Iterable, SupportsIndex, overload

from editor_sped.classes.registro import Registro


class ListaRegistro(list[Registro]):
    def __init__(self, iterable: Iterable[Registro], /) -> None:
        super().__init__(iterable)


    @overload
    def __getitem__(self, key: SupportsIndex) -> Any: ...

    @overload
    def __getitem__(self, key: slice) -> list[Any]: ...

    @overload
    def __getitem__(self, key: str) -> "ListaRegistro": ...

    def __getitem__(self, key):
        if isinstance(key, str):
            return ListaRegistro(r for r in self if r.nome == key)

        return super().__getitem__(key)
