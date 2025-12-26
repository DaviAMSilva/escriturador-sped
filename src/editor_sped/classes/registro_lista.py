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

        # Isso é necessário pois se Registro for importado no topo
        # do arquivo ocorrem erros devido a uma importação circular
        from .registro import Registro  # pylint: disable=import-outside-toplevel
        for registro in self:
            if not isinstance(registro, Registro):
                raise TypeError(f"Item diferente de Registro em inicialização de ListaRegistro ({registro})")



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



    def __repr__(self):
        return f"ListaRegistro{super().__repr__()}"



    def pesquisar(
        self,
        nome: str | re.Pattern | None = None,
        campos: dict[str | int, str | int | float | None] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        *,
        campos_c: dict[str | int, str] | None = None,
        campos_n: dict[str | int, int | float | None] | None = None,
        recursivo=True,
        primeiro=False
    ) -> "ListaRegistro":
        encontrados = ListaRegistro()

        for filho in self:
            valido = filho.teste(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro)

            if valido:
                if primeiro:
                    return ListaRegistro([filho])

                encontrados.append(filho)

            if recursivo and filho.filhos:
                encontrados.extend(filho.pesquisar(
                    nome,
                    campos,
                    campos_c=campos_c,
                    campos_n=campos_n,
                    filtro=filtro,
                    recursivo=recursivo,
                    primeiro=primeiro
                ))

                if primeiro and encontrados:
                    return encontrados[0:1]

        return encontrados

    def primeiro(
        self,
        nome: str | re.Pattern | None = None,
        campos: dict[str | int, str | int | float | None] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        *,
        campos_c: dict[str | int, str] | None = None,
        campos_n: dict[str | int, int | float | None] | None = None,
        recursivo=True
    ) -> "Registro":
        encontrado = self.pesquisar(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro, recursivo=recursivo, primeiro=True)

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro pesquisado não foi encontrado") from e



    @property
    def nomes(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(r.nome for r in self))
