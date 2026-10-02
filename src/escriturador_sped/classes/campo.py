"""Contém a classe `Campo`."""
from typing import Literal, assert_never

from ..constantes import ALFANUMERICO, NUMERICO
from ..modulos import MODULOS, ModuloT
from ..tipos import CampoT, CampoTipoT, Chave, Valor, ValorC, ValorN, ValorN0










# Tipagem para tipos de campos específicos
# pylint: disable=invalid-name
type CampoC = Campo[Literal["C"], ValorC]
"""Tipo que representa um campo alfanumérico."""
type CampoN = Campo[Literal["N"], ValorN]
"""Tipo que representa um campo numérico."""
# pylint: enable=invalid-name










class Campo[TipoT: CampoTipoT, ValorT: Valor]:
    """Contém informações sobre um campo.

    Attributes:
        nome (str): Nome do campo.
        descricao (str): Descrição do campo.
        tipo (TipoT): Tipo do campo.
        modulo (ModuloT): Módulo ao qual o campo pertence.
        decimal (int | None): Quantidade de casas decimais.
        obrigatorio (bool): Se o campo é obrigatório.
        tamanho (int): Tamanho máximo da forma alfanumérica.
        tamanho_exato (bool): Se o tamanho precisa ser exato.

    Args:
        modulo: Módulo ao qual o campo pertence.
        nome_registro: Nome do registro a que o campo pertence.
        chave: Número ou nome do campo no registro a que o campo pertence (campos têm indexação iniciada em 1).
        valor: Valor inicial do campo.

    Raises:
        IndexError: Se a chave for um valor menor que 1 (campos têm indexação iniciada em 1).
        ValueError: Se a chave não for um nome de campo válido.
        TypeError: Se a chave não é de um tipo válido.
    """
    tipo: TipoT

    # Tipos de campo
    ALFANUMERICO = ALFANUMERICO
    """Código para campo do tipo alfanumérico."""
    NUMERICO = NUMERICO
    """Código para campo do tipo numérico."""



    @staticmethod
    def alfanumerico(valor: Valor, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> ValorC:
        """Converte um valor para a forma alfanumérica.

        Args:
            valor: Valor a ser convertido.
            decimal: Quantidade de casas decimais.
            tamanho: Tamanho máximo da forma alfanumérica.
            tamanho_exato: Se o tamanho precisa ser exato.

        Returns:
            A forma alfanumérica do valor.
        """
        if isinstance(valor, str):
            if len(valor) > tamanho:
                return valor[:tamanho]
            return valor

        if valor is None:
            return ""

        if decimal:
            # Números decimais tem casas decimais extras removidas
            resultado = f"{valor:.{decimal}f}".rstrip("0").rstrip(".")
            return resultado.replace(".", ",") if "." in resultado else resultado

        # Abaixo dessa linhas apenas números inteiros fazem sentido
        if not isinstance(valor, int):
            valor = int(valor)

        if tamanho_exato:
            return f"{valor:0{tamanho}d}"

        return str(valor)

    @staticmethod
    def numerico(valor: Valor, decimal: int | None) -> ValorN:
        """Converte um valor para a forma numérica.

        Args:
            valor: Valor a ser convertido.
            decimal: Quantidade de casas decimais.

        Returns:
            A forma numérica do valor.
        """
        if valor in ("", None):
            return None

        if isinstance(valor, str):
            if decimal:
                return round(float(valor.replace(",", ".")), decimal)

            return int(valor.replace(",", "."))

        if decimal:
            return round(float(valor), decimal)

        return int(valor)



    def __init__(self, modulo: ModuloT, nome_registro: str, chave: Chave, valor: Valor) -> None:
        info_campos = MODULOS[modulo]["registros"][nome_registro.upper()]["campos"]

        # Descobrindo o info_campo correto
        if isinstance(chave, int):
            # Caso for o número, verificar que é maior que 0
            if chave <= 0:
                raise ValueError("Os campos de um registro têm a numeração iniciada pelo número 1")

            try:
                info_campo = info_campos[chave - 1]
            except IndexError:
                # A execução só é suposta a chegar aqui se uma quantidade válida de campos for
                # maior que a quantidade de campos fixos existentes (módulo ECD, I550 e I555)
                # Nesse caso todos os campos restantes são tratados como campos alfanuméricos
                info_campo: CampoT = {
                    "numero": chave - 1,
                    "nome": f"CAMPO{chave:02d}",
                    "descricao": "",
                    "obrigatorio": False,
                    "tamanho": 255,
                    "tamanho_exato": False,
                    "decimal": None,
                    "tipo": "C"
                }
        elif isinstance(chave, str):
            # Caso for o nome, encontrar o info_campo com esse nome
            for info_campo in info_campos:
                if info_campo["nome"] == chave:
                    break
            else:
                raise ValueError(f"Campo não encontrado pelo nome ({chave})")
        else:
            raise TypeError(f"Tipo inválido para parâmetro 'chave' ({chave})")

        # fmt: off
        self.nome          = info_campo["nome"]
        self.descricao     = info_campo["descricao"]
        self.decimal       = info_campo["decimal"]
        self.obrigatorio   = info_campo["obrigatorio"]
        self.tamanho       = info_campo["tamanho"]
        self.tamanho_exato = info_campo["tamanho_exato"]
        self.tipo          = info_campo["tipo"]  # type: ignore
        # fmt: on

        self._valor_alfanumerico: ValorC = ""
        self._valor_numerico: ValorN = None

        # Converte o valor passado para os valores interno corretos
        self.valor = valor



    def __str__(self) -> str:
        return self.texto()

    def __repr__(self) -> str:
        return f"Campo[{self.tipo!r}]({self.nome!r}: {self.valor!r})"



    def texto(self) -> str:
        """Converte o campo para texto.

        Returns:
            O valor do campo em forma de texto.
        """
        return self._valor_alfanumerico



    @property
    def valor(self) -> ValorT:
        """Permite obter e modificar o valor do campo.

        Args:
            valor (Valor): Novo valor do campo.

        Raises:
            TypeError: Se o novo valor não for do tipo `Valor`.
        """
        if self.tipo == Campo.ALFANUMERICO:
            return self.valor_c  # type: ignore

        if self.tipo == Campo.NUMERICO:
            return self.valor_n  # type: ignore

        assert_never(self.tipo)

    @valor.setter
    def valor(self, valor: Valor) -> None:
        # Como o mais comum é valor ser str, testa-se somente str primeiro
        if not isinstance(valor, str):
            if not isinstance(valor, (int, float)) and valor is not None:
                raise TypeError(f"O valor para um campo deve ser do tipo str, int, float ou None ({valor})")



        # A maioria dos campos é numérico, então testamos esse tipo primeiro
        if self.tipo == Campo.NUMERICO:
            # Convertermos o valor para numérico para normalizar o valor de comparação
            valor_numerico = Campo.numerico(valor, self.decimal)

            # 0 e "" são os dois valores mais abundantes, então é mais eficiente filtra-los
            if valor_numerico == 0 and not self.tamanho_exato:
                self._valor_numerico = 0
                self._valor_alfanumerico = "0"
                return

            if valor_numerico is None:
                self._valor_numerico = None
                self._valor_alfanumerico = ""
                return

            self._valor_numerico = valor_numerico
            self._valor_alfanumerico = Campo.alfanumerico(valor_numerico, self.decimal, self.tamanho, self.tamanho_exato)
            return



        if self.tipo == Campo.ALFANUMERICO:
            self._valor_numerico = None

            if valor == "" or valor is None:
                self._valor_alfanumerico = ""
                return

            self._valor_alfanumerico = valor[:self.tamanho] if isinstance(valor, str) else str(valor)[:self.tamanho]
            return



        assert_never(self.tipo)



    @property
    def valor_c(self) -> ValorC:
        """Permite obter e modificar o valor alfanumérico do campo.

        Args:
            valor (Valor): Novo valor do campo.

        Raises:
            TypeError: Se o novo valor não for do tipo `Valor`.
        """
        return self._valor_alfanumerico

    @valor_c.setter
    def valor_c(self, valor: Valor) -> None:
        self.valor = valor



    @property
    def valor_n(self) -> ValorN:
        """Permite obter e modificar o valor numérico do campo.

        Args:
            valor (Valor): Novo valor do campo.

        Raises:
            TypeError: Se o novo valor não for do tipo `Valor`.
        """
        if self._valor_numerico is None:
            return None

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n.setter
    def valor_n(self, valor: Valor) -> None:
        self.valor = valor



    @property
    def valor_n0(self) -> ValorN0:
        """Permite obter e modificar o valor numérico, não nulo, do campo.

        Em contraste a `valor_n`, usando essa propriedade um campo vazio irá retornar `0` ao invés de `None`.

        Args:
            valor (Valor): Novo valor do campo.

        Raises:
            TypeError: Se o novo valor não for do tipo `Valor`.
        """
        if self._valor_numerico is None:
            return 0

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n0.setter
    def valor_n0(self, valor: Valor) -> None:
        self.valor = valor
