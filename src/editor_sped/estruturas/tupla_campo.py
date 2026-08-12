from typing import Iterable, Self, SupportsIndex, overload

from ..classes.campo import Campo
from ..tipos import Chave, Valor, ValorC, ValorN, ValorN0










class TuplaCampo(tuple["Campo", ...]):
    def __init__(self, *_) -> None:
        self.dicionario: dict[str, "Campo"] = {}

        for campo in self:
            if not isinstance(campo, Campo):
                raise TypeError(f"Item diferente de Campo em inicialização de TuplaCampo ({campo})")

            if campo.nome in self.dicionario:
                raise ValueError(f"Campo duplicado ({campo!r} e {self.dicionario[campo.nome]!r})")

            self.dicionario[campo.nome] = campo

    @overload
    def __new__(cls) -> Self: ...

    @overload
    def __new__(cls, iteravel: Iterable["Campo"]) -> Self: ...

    def __new__(cls, iteravel: Iterable["Campo"] = ()):
        return super(TuplaCampo, cls).__new__(cls, tuple(iteravel))



    @overload
    def __getitem__(self, chave: Chave | SupportsIndex) -> "Campo": ...

    @overload
    def __getitem__(self, chave: slice) -> "TuplaCampo": ...

    def __getitem__(self, chave: Chave | SupportsIndex | slice):
        try:
            if isinstance(chave, int):
                if chave == 0:
                    raise IndexError("Os campos de um registro têm a numeração iniciada pelo número 1")

                return super().__getitem__(chave - 1) if chave > 0 else super().__getitem__(chave)

            if isinstance(chave, slice):
                return TuplaCampo(super().__getitem__(chave))

            if isinstance(chave, str):
                return self.dicionario[chave]
        except KeyError as e:
            raise KeyError(f"Campo não encontrado pelo valor de pesquisa ({chave})") from e

        raise TypeError(f"Valor inválido ({chave})")



    def __contains__(self, chave: object) -> bool:
        if isinstance(chave, str):
            return chave in self.dicionario

        if isinstance(chave, int):
            return 1 <= chave <= len(self)

        return super().__contains__(chave)



    def __repr__(self) -> str:
        return f"TuplaCampo{super().__repr__()}"



    def valores(self, valores: dict[Chave, Valor] | None = None) -> dict[str, Valor]:
        if isinstance(valores, dict):
            for campo, valor in valores.items():
                if campo in self:
                    self[campo].valor = valor
        elif valores is not None:
            raise TypeError(f"Tipo inválido para parâmetro 'valores' ({valores})")

        return {campo.nome: campo.valor for campo in self}

    def valores_c(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorC]:
        self.valores(valores)
        return {campo.nome: campo.valor_c for campo in self}

    def valores_n(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN]:
        self.valores(valores)
        return {campo.nome: campo.valor_n for campo in self}

    def valores_n0(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN0]:
        self.valores(valores)
        return {campo.nome: campo.valor_n0 for campo in self}



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(self.dicionario.keys())
