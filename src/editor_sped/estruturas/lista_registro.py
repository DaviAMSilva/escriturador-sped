from typing import TYPE_CHECKING, Callable, Iterable, Mapping, SupportsIndex, overload

from ..tipos import Chave, ChaveT, Valor, ValorC, ValorN

if TYPE_CHECKING:
    from ..classes.registro import Registro










class ListaRegistro(list["Registro"]):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iteravel: Iterable["Registro"]) -> None: ...

    def __init__(self, iteravel: Iterable["Registro"] = ()) -> None:
        super().__init__(iteravel)



    @overload
    def __getitem__(self, chave: int | SupportsIndex) -> "Registro": ...

    @overload
    def __getitem__(self, chave: str | tuple[str, Mapping[ChaveT, Valor | Iterable[Valor]]] | slice | None) -> "ListaRegistro": ...

    def __getitem__(self, chave: str | tuple[str, Mapping[ChaveT, Valor | Iterable[Valor]]] | int | SupportsIndex | slice | None):
        if isinstance(chave, (SupportsIndex, int)):
            return super().__getitem__(chave)

        if isinstance(chave, slice):
            return ListaRegistro(super().__getitem__(chave))

        if isinstance(chave, str) or chave is None:
            return self.buscar(chave)

        if isinstance(chave, tuple) and len(chave) == 2:
            if (isinstance(chave[0], str) or chave[0] is None) and (isinstance(chave[1], dict) or chave[1] is None):
                return self.buscar(chave[0], chave[1])

            raise TypeError(f"Tupla com valores inválidos ({chave})")

        raise TypeError(f"Valor inválido ({chave})")



    def __repr__(self) -> str:
        return f"ListaRegistro{super().__repr__()}"



    def buscar(
        self,
        nome: str | None = None,
        campos: dict[Chave, Valor | Iterable[Valor]] | None = None,
        *,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = None,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo=True,
        primeiro=False
    ) -> "ListaRegistro":
        encontrados = ListaRegistro()

        if nome:
            nome = nome.upper()

        for filho in self:
            valido = filho.teste(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro)

            if valido:
                if primeiro:
                    return ListaRegistro([filho])

                encontrados.append(filho)

            if recursivo and filho.filhos:
                encontrados.extend(filho.filhos.buscar(
                    nome, campos, campos_c=campos_c, campos_n=campos_n,
                    filtro=filtro, recursivo=recursivo, primeiro=primeiro
                ))

                if primeiro and encontrados:
                    return encontrados[0:1]

        return encontrados

    def primeiro(
        self,
        nome: str | None = None,
        campos: dict[Chave, Valor | Iterable[Valor]] | None = None,
        *,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = None,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo=True
    ) -> "Registro":
        encontrado = self.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro pesquisado não foi encontrado") from e



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(r.nome for r in self))
