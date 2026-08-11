from typing import Literal, TypeVar, TypedDict


CampoTipoT = Literal["C", "N"]
ModuloT = Literal["efd_pis_cofins", "efd_icms_ipi"]
ModulosT = dict[ModuloT, "LeiauteT"]


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




Chave = str | int
ChaveT = TypeVar("ChaveT", bound=Chave)
# pylint: disable=invalid-name
ValorC = str
ValorN = int | float | None
ValorN0 = int | float
Valor = ValorC | ValorN
Valor0 = ValorC | ValorN0
# pylint: enable=invalid-name
