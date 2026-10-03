"""Contém a classe `Componente`."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Iterable, Iterator

from ..estruturas.lista_registro import ListaRegistro
from ..modulos import ModuloT
from ..tipos import Chave, Valor, ValorC, ValorN

if TYPE_CHECKING:
    from .registro import Registro










class Componente(ABC):
    """Contém informações sobre um componente de uma escrituração.

    Attributes:
        nome (str): Nome do componente.
        filhos (ListaRegistro): Lista de filhos do componente.
        modulo (ModuloT): Módulo ao qual o componente pertence.
        tamanho (int): Quantidade registro que o componente representa.
        registros (ListaRegistro): Lista contendo todos os registros filhos recursivamente.

    Args:
        nome: Nome do componente.
        filhos: Lista inicial de filhos do componente.
        modulo: Módulo ao qual o componente pertence.
    """

    def __init__(self, modulo: ModuloT, nome: str, filhos: ListaRegistro) -> None:
        self.nome: str = nome
        self.filhos: ListaRegistro[Registro] = filhos
        self.modulo: ModuloT = modulo



    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    def __len__(self) -> int:
        return self.tamanho

    def __iter__(self) -> Iterator["Registro"]:
        """Usado para iterar os registros filhos do componente.

        Returns:
            Um iterador de todos os registros filhos do componente.
        """
        return iter(self.filhos)



    @abstractmethod
    def texto(self) -> str:
        """Converte o componente para texto, da messa forma como ele estaria presente em um arquivo de escrituração, inclusive contendo quebras de linhas.

        Returns:
            Representação textual do componente.
        """



    @property
    def tamanho(self) -> int:
        """Tamanho do componente, sendo a quantidade de linhas que o componente e seus filhos ocupariam em uma escrituração.

        Especificamente para os blocos `0` e `9` os registros `0000` e `9999` são considerados como registros filhos.
        """
        return sum(filho.tamanho for filho in self.filhos)

    @property
    def registros(self) -> "ListaRegistro[Registro]":
        """Lista contendo todos os registros filhos diretos e recursivos."""
        return self.buscar()



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
        """Realiza uma busca de registros válidos por todos os registros filhos do componente, de acordo com os parâmetros informados.

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
            >>> registro.buscar("NOME", {"CAMPO": [1, 2]}, filtro=lambda r: True)
            ListaRegistro[Registro('|NOME|1|'), Registro('|NOME|2|')]
        """
        return self.filhos.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=primeiro
        )

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
        """Realiza uma busca pelo primeiro registro válido por todos os registros filhos do componente, de acordo com os parâmetros informados.

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
            >>> registro.primeiro("NOME", {"CAMPO": [1, 2]}, filtro=lambda r: True)
            Registro('|NOME|1|')

            >>> registro.primeiro("ERRO")
            ValueError: O registro buscado não foi encontrado
        """
        encontrado = self.filhos.buscar(
            nome, campos, campos_c=campos_c, campos_n=campos_n,
            filtro=filtro, recursivo=recursivo, primeiro=True
        )

        try:
            return encontrado[0]
        except IndexError as e:
            raise ValueError("O registro buscado não foi encontrado") from e
