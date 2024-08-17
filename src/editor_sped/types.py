from typing import TypedDict, Literal


EfdTipo = Literal["efd_icms_ipi", "efd_pis_cofins"]
EfdInfo = dict[EfdTipo, "EfdInfoTipo"]


class EfdInfoTipo(TypedDict):
    registros: dict[str, "EfdInfoRegistro"]
    blocos: list["EfdInfoBloco"]

class EfdInfoBloco(TypedDict):
    numero: int
    nome: str
    descricao: str
    abertura: str
    fechamento: str


class EfdInfoRegistro(TypedDict):
    descricao: str
    nivel: int
    obrigatorio: bool
    unico: bool
    campos: list["EfdInfoCampo"]
    filhos: list["EfdInfoRegistro"]
    pai: str | None


class EfdInfoCampo(TypedDict):
    numero: int
    nome: str
    descricao: str
    obrigatorio: bool
    tamanho: int
    tamanho_exato: bool
    decimal: int | None
    tipo: Literal["C", "N"]
