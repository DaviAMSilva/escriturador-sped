from typing import TYPE_CHECKING, Iterable, Self, SupportsIndex, overload

if TYPE_CHECKING:
    from .campo import Campo










class TuplaCampo(tuple["Campo", ...]):
    def __init__(self, *_) -> None:
        self.dicionario: dict[str, "Campo"] = {}

        for campo in self:
            self.dicionario[campo.nome] = campo

    @overload
    def __new__(cls) -> Self: ...

    @overload
    def __new__(cls, iteravel: Iterable["Campo"]) -> Self: ...

    def __new__(cls, iteravel=()):
        return super(TuplaCampo, cls).__new__(cls, tuple(iteravel))



    @overload
    def __getitem__(self, chave: SupportsIndex | int | str) -> "Campo": ...

    @overload
    def __getitem__(self, chave: slice) -> "TuplaCampo": ...

    def __getitem__(self, chave):
        try:
            if isinstance(chave, int):
                if chave == 0:
                    raise IndexError("Os campos de um registro têm a numeração iniciada pelo número 1")

                return super().__getitem__(chave - 1) if chave >= 1 else super().__getitem__(chave)

            if isinstance(chave, SupportsIndex):
                return super().__getitem__(chave)

            if isinstance(chave, slice):
                return TuplaCampo(super().__getitem__(chave))

            if isinstance(chave, str):
                return self.dicionario[chave]
        except KeyError as e:
            raise KeyError(f"Campo não encontrado pelo valor de pesquisa ({chave})") from e

        raise TypeError(f"Valor inválido ({chave})")



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(self.dicionario.keys())
