from typing import TYPE_CHECKING, Callable, Iterable, SupportsIndex, cast, overload

from ..tipos import Chave, Valor, ValorC, ValorN

if TYPE_CHECKING:
    from ..classes.registro import Registro










class ListaRegistro[RegistroT: Registro](list[RegistroT]):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iteravel: Iterable[RegistroT]) -> None: ...

    def __init__(self, iteravel: Iterable[RegistroT] = ()) -> None:
        super().__init__(iteravel)



    @overload
    def __getitem__(self, chave: SupportsIndex) -> RegistroT: ...

    @overload
    def __getitem__(self, chave: slice) -> "ListaRegistro[RegistroT]": ...

    def __getitem__(self, chave: SupportsIndex | slice):
        if isinstance(chave, slice):
            return ListaRegistro[RegistroT](super().__getitem__(chave))

        return super().__getitem__(chave)



    def __repr__(self) -> str:
        return f"ListaRegistro{super().__repr__()}"



    def como[ComoRegistroT: Registro](self, registro: type[ComoRegistroT]) -> "ListaRegistro[ComoRegistroT]":  # pylint: disable=unused-argument
        return cast(ListaRegistro[ComoRegistroT], self)



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
    ) -> "ListaRegistro[Registro]":
        encontrados = ListaRegistro["Registro"]()

        if nome:
            nome = nome.upper()

        for filho in self:
            valido = filho.teste(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro)

            if valido:
                if primeiro:
                    return ListaRegistro["Registro"]([filho])

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
