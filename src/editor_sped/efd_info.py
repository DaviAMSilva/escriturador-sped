import json
from importlib.resources import files
from typing import Literal, TypedDict
from .modulos import MODULOS_PADROES


CampoTipo = Literal["C", "N"]

EfdTipo = Literal["contribuicoes", "icms_ipi"]
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
    filhos: list[str]
    pai: str | None


class EfdInfoCampo(TypedDict):
    numero: int
    nome: str
    descricao: str
    obrigatorio: bool
    tamanho: int
    tamanho_exato: bool
    decimal: int | None
    tipo: CampoTipo


# Usado para escolher qual versão a ser carregada
def carregar_modulos(efd: EfdTipo, leiaute: str, versao: str):
    with files("editor_sped.modulos").joinpath(efd, leiaute, versao, "leiaute.json").open("r", encoding="utf-8") as efd_info_arquivo:
        EFD_INFO[efd] = json.loads(efd_info_arquivo.read())


EFD_INFO: EfdInfo = {}

try:
    for e, (l, v) in MODULOS_PADROES.items():
        carregar_modulos(e, l, v)
except FileNotFoundError:
    EFD_INFO = {}
