from typing import Literal, TypeVar, TypedDict


# pylint: disable=invalid-name
type CampoTipoT = Literal["C", "N"]
type ModuloT = Literal["efd_pis_cofins", "efd_icms_ipi"]
type ModulosT = dict[ModuloT, "LeiauteT"]
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




type Chave = str | int
ChaveT = TypeVar("ChaveT", bound=Chave)
# pylint: disable=invalid-name
type ValorC = str
type ValorN = int | float | None
type ValorN0 = int | float
type Valor = ValorC | ValorN
type Valor0 = ValorC | ValorN0
# pylint: enable=invalid-name
