"""Contém a classe `TuplaCampo`."""
from typing import Iterable, Self, SupportsIndex, overload

from ..classes.campo import Campo
from ..tipos import CampoTipoT, Chave, Valor, ValorC, ValorN, ValorN0










class TuplaCampo(tuple["Campo[CampoTipoT, Valor]", ...]):
    """Representa uma tupla de campos com funcionalidades adicionais.

    Attributes:
        nomes (tuple[str, ...]): Tupla com os nomes dos campos presentes na tupla de campos.

    Args:
        iteravel: Iterável de campos a serem adicionados durante a criação da tupla de campos.

    Raises:
        TypeError: Se um dos argumentos não é um campo.
    """

    def __init__(self, *_) -> None:
        self.dicionario: dict[str, "Campo[CampoTipoT, Valor]"] = {}

        for campo in self:
            if not isinstance(campo, Campo):
                raise TypeError(f"Item diferente de Campo em inicialização de TuplaCampo ({campo})")

            if campo.nome in self.dicionario:
                raise ValueError(f"Campo duplicado ({campo!r} e {self.dicionario[campo.nome]!r})")

            self.dicionario[campo.nome] = campo

    @overload
    def __new__(cls) -> Self: ...

    @overload
    def __new__(cls, iteravel: Iterable["Campo[CampoTipoT, Valor]"]) -> Self: ...

    def __new__(cls, iteravel: Iterable["Campo[CampoTipoT, Valor]"] = ()):
        return super(TuplaCampo, cls).__new__(cls, tuple(iteravel))



    @overload
    def __getitem__(self, chave: Chave | SupportsIndex) -> "Campo[CampoTipoT, Valor]": ...

    @overload
    def __getitem__(self, chave: slice) -> "TuplaCampo": ...

    def __getitem__(self, chave: Chave | SupportsIndex | slice):
        """Retorna um ou mais campos na tupla de campos.

        Args:
            chave: Índice, nome ou slice dos campos buscados.

        Raises:
            IndexError: Se a chave for um valor igual a 0 (campos têm indexação iniciada em 1).
            KeyError: Se um campo com o nome igual a chave não for encontrado.
            TypeError: Se a chave não é de um tipo válido.

        Returns:
            Um campo ou uma tupla de campos.

        Examples:
            >>> campos[1]
            Campo['C']('REG': '0000')

            >>> campos['COD_VER']
            Campo['N']('COD_VER': 0)
        """
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
            raise KeyError(f"Campo não encontrado pelo valor de busca ({chave})") from e

        raise TypeError(f"Valor inválido ({chave})")



    def __contains__(self, chave: object) -> bool:
        """Determina se uma chave representa um campo na tupla de campos.

        Args:
            chave: Índice, nome ou campo a ser determinado se existe na tupla de campos.

        Returns:
            Se a chave representa pelo menos um dos campos da tupla de campos.
        """
        if isinstance(chave, str):
            return chave in self.dicionario

        if isinstance(chave, int):
            return 1 <= chave <= len(self)

        return super().__contains__(chave)



    def __repr__(self) -> str:
        return f"TuplaCampo{super().__repr__()}"



    def valores(self, valores: dict[Chave, Valor] | None = None) -> dict[str, Valor]:
        """Permite visualizar ou alterar os valores dos campos na tupla de campos.

        Diferentes variações dessa função podem retornar especificamente os valores alfanumérico, numéricos ou numéricos, não nulos:

        - `TuplaCampo.valores() -> dict[str, Valor]`
        - `TuplaCampo.valores_c() -> dict[str, ValorC]`
        - `TuplaCampo.valores_n() -> dict[str, ValorN]`
        - `TuplaCampo.valores_n0() -> dict[str, ValorN0]`

        Args:
            valores: Dicionário de valores a serem alterados na tupla de campos.

        Raises:
            TypeError: Se os valores não são de um tipo válido.

        Returns:
            Valores dos campos na tupla de campos, após a alteração se essa tiver ocorrida.

        Examples:
            >>> campos.valores()
            {'NOME': 'UM', 'VALOR': 10}

            >>> campos.valores({NOME: 'DOIS', 2: 20})
            {'NOME': 'DOIS', 'VALOR': 20}
        """
        if isinstance(valores, dict):
            for campo, valor in valores.items():
                if campo in self:
                    self[campo].valor = valor
        elif valores is not None:
            raise TypeError(f"Tipo inválido para parâmetro 'valores' ({valores})")

        return {campo.nome: campo.valor for campo in self}

    def valores_c(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorC]:
        """Consultar `TuplaCampos.valores()`."""
        self.valores(valores)
        return {campo.nome: campo.valor_c for campo in self}

    def valores_n(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN]:
        """Consultar `TuplaCampos.valores()`."""
        self.valores(valores)
        return {campo.nome: campo.valor_n for campo in self}

    def valores_n0(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN0]:
        """Consultar `TuplaCampos.valores()`."""
        self.valores(valores)
        return {campo.nome: campo.valor_n0 for campo in self}



    @property
    def nomes(self) -> tuple[str, ...]:
        """Nomes dos campos na tupla de campos."""
        return tuple(self.dicionario.keys())
