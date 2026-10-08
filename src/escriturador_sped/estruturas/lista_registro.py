"""Contém a classe `ListaRegistro`."""
from typing import TYPE_CHECKING, Callable, Iterable, SupportsIndex, cast, overload

from ..tipos import Chave, Valor, ValorC, ValorN

if TYPE_CHECKING:
    from ..classes.registro import Registro










class ListaRegistro[RegistroT: Registro](list[RegistroT]):
    """Representa uma lista de registros com funcionalidades adicionais.

    Attributes:
        nomes (tuple[str, ...]): Tupla com os nomes dos registros presentes na lista de registros.

    Args:
        iterable: Iterável de registros a serem adicionados durante a criação da lista de registros.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[RegistroT]) -> None: ...

    def __init__(self, iterable: Iterable[RegistroT] = ()) -> None:
        super().__init__(iterable)



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
        """Corrige a tipo dos registros na lista para o tipo especificado.

        Returns:
            A própria lista, mas com o tipo dos registros corrigido.
        """
        return cast(ListaRegistro[ComoRegistroT], self)



    def buscar(
        self,
        nome: str | None = None,
        campos: dict[Chave, Valor | Iterable[Valor]] | None = None,
        *,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = None,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        recursivo: bool = True,
        primeiro: bool = False
    ) -> "ListaRegistro[Registro]":
        """Realiza uma busca de registros válidos entre os registros na lista de registros, de acordo com os parâmetros informados.

        Args:
            nome: Nome dos registros buscados.
            campos: Dicionários com chaves e um ou mais valores dos campos nos registros buscados.
            campos_c: Dicionários com chaves e um ou mais valores alfanuméricos dos campos nos registros buscados.
            campos_n: Dicionários com chaves e um ou mais valores numéricos dos campos nos registros buscados.
            filtro: Função que recebe um `Registro` e retorna `True` para os registros buscados.
            recursivo: Se a busca é feita de forma recursiva.
            primeiro: Se a busca deve ser encerrada após o primeiro registro ser encontrado.

        Returns:
            Lista de registros contendo todos os registros válidos encontrados na busca.

        Examples:
            >>> registros.buscar("NOME", {"CAMPO": [1, 2]}, filtro=lambda r: True)
            ListaRegistro[Registro('|NOME|1|'), Registro('|NOME|2|')]
        """
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
        recursivo: bool = True
    ) -> "Registro":
        """Realiza uma busca pelo primeiro registro válido entre os registros na lista de registros, de acordo com os parâmetros informados.

        Args:
            nome: Nome dos registros buscados.
            campos: Dicionários com chaves e um ou mais valores dos campos nos registros buscados.
            campos_c: Dicionários com chaves e um ou mais valores alfanuméricos dos campos nos registros buscados.
            campos_n: Dicionários com chaves e um ou mais valores numéricos dos campos nos registros buscados.
            filtro: Função que recebe um `Registro` e retorna `True` para os registros buscados.
            recursivo: Se a busca é feita de forma recursiva.

        Returns:
            Primeiro registro válido encontrado na busca.

        Raises:
            ValueError: Se nenhum registro válido for encontrado.

        Examples:
            >>> registros.primeiro("NOME", {"CAMPO": [1, 2]}, filtro=lambda r: True)
            Registro('|NOME|1|')

            >>> registros.primeiro("ERRO")
            ValueError: O registro buscado não foi encontrado
        """
        encontrado = self.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro buscado não foi encontrado") from e



    @property
    def nomes(self) -> tuple[str, ...]:
        """Nomes dos registros na lista de registros, sem repetição."""
        return tuple(dict.fromkeys(r.nome for r in self))
