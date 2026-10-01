"""Contém vários tipos usados pela biblioteca."""
from typing import Literal, TypedDict


# pylint: disable=invalid-name
type ModuloT = Literal["ecd", "ecf", "efd_contribuicoes", "efd_icms_ipi"]
"""Tipo que representa o nome de um módulo."""
type ModulosT = dict[ModuloT, "LeiauteT"]
"""Tipo que representa as informações dos módulos."""

type CampoTipoT = Literal["C", "N"]
"""Tipo que representa os diferentes tipos de campos."""

type Chave = str | int
"""Tipo que representam os valores que podem ser usados para indexar um campo."""

type ValorC = str
"""Tipo que representa o valor alfanumérico de um campo."""
type ValorN = int | float | None
"""Tipo que representa o valor numérico de um campo."""
type ValorN0 = int | float
"""Tipo que representa o valor numérico, não nulo, de um campo."""
type Valor = ValorC | ValorN
"""Tipo que representa o valor de um campo."""
type Valor0 = ValorC | ValorN0
"""Tipo que representa o valor, não nulo, de um campo."""
# pylint: enable=invalid-name


class LeiauteT(TypedDict):
    """Tipo que representa as informações de um leiaute de módulo.

    Attributes:
        registros: Informações sobre registros.
        blocos: Informações sobre blocos.
    """
    registros: dict[str, "RegistroT"]
    blocos: list["BlocoT"]


class BlocoT(TypedDict):
    """Tipo que representa as informações de um bloco.

    Attributes:
        numero: Ordem do bloco na escrituração.
        nome: Nome do bloco.
        descricao: Descrição do bloco.
        abertura: Nome do registro de abertura do bloco.
        fechamento: Nome do registro de fechamento do bloco.
    """
    numero: int
    nome: str
    descricao: str
    abertura: str
    fechamento: str


class RegistroT(TypedDict):
    """Tipo que representa as informações de um registro.

    Attributes:
        descricao: Descrição do registro.
        nivel: Nível do registro na escrituração.
        obrigatorio: Se o registro é obrigatório estar presente na escrituração.
        unico: Se o registro é único na escrituração.
        campos: Informações sobres os campos do registro.
        campos_exatos: Quando diferente de `None`, é uma lista de quantidade de campos permitidos.
        campos_faixa: Quando diferente de `None`, é uma tupla com a quantidade mínima e máxima de campos permitidos.
        filhos: Lista de nomes de registros filhos válidos do registro.
        pai: Nome do pai do registro, se existir.
    """
    descricao: str
    nivel: int
    obrigatorio: bool
    unico: bool
    campos: list["CampoT"]
    campos_exatos: list[int] | None
    campos_faixa: tuple[int, int] | None
    filhos: list[str]
    pai: str | None


class CampoT(TypedDict):
    """Tipo que representa as informações de um campo.

    Attributes:
        numero: Ordem do campo no registro.
        nome: Nome do campo.
        descricao: Descrição do campo.
        obrigatorio: Se o preenchimento do campo é obrigatório.
        tamanho: Tamanho máximo do campo.
        tamanho_exato: Se o tamanho do campo precisa ser exato.
        decimal: Quantidade de casas decimais do campo.
        tipo: Tipo do campo.
    """
    numero: int
    nome: str
    descricao: str
    obrigatorio: bool
    tamanho: int
    tamanho_exato: bool
    decimal: int | None
    tipo: CampoTipoT
