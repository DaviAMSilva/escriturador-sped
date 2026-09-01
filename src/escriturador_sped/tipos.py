from typing import Literal, TypedDict


# pylint: disable=invalid-name
type ModuloT = Literal["efd_contribuicoes", "efd_icms_ipi"]
type ModulosT = dict[ModuloT, "LeiauteT"]

type CampoTipoT = Literal["C", "N"]

type Chave = str | int

type ValorC = str
type ValorN = int | float | None
type ValorN0 = int | float
type Valor = ValorC | ValorN
type Valor0 = ValorC | ValorN0
# pylint: enable=invalid-name


class LeiauteT(TypedDict):
    registros: dict[str, "RegistroT"]
    blocos: list["BlocoT"]


class BlocoT(TypedDict):
    numero: int
    nome: str
    descricao: str
    abertura: str
    fechamento: str


class RegistroT(TypedDict):
    descricao: str
    nivel: int
    obrigatorio: bool
    unico: bool
    campos: list["CampoT"]
    filhos: list[str]
    pai: str | None


class CampoT(TypedDict):
    numero: int
    nome: str
    descricao: str
    obrigatorio: bool
    tamanho: int
    tamanho_exato: bool
    decimal: int | None
    tipo: CampoTipoT
