import json
import os
from importlib.resources import files

from ..constantes import EFD_ICMS_IPI, EFD_PIS_COFINS
from ..tipos import ModulosT, ModuloT


# Controla qual versão de cada módulo será carregada por padrão
MODULOS_PADROES: dict[ModuloT, tuple[str, str]] = {
    EFD_PIS_COFINS: ("006", "1.35"),
    EFD_ICMS_IPI: ("020", "3.2.3")
}
MODULOS_NOMES: tuple[ModuloT, ...] = tuple(MODULOS_PADROES.keys())


# Usado para escolher qual versão a ser carregada
def carregar_modulo(modulo: ModuloT, leiaute: str, versao: str):
    with files("editor_sped.modulos").joinpath(
        modulo, f"l{leiaute}", f"v{versao.replace('.', '_')}", "leiaute.json"
    ).open("r", encoding="utf-8") as arquivo_modulo:
        MODULOS[modulo] = json.loads(arquivo_modulo.read())


# pylint: disable=invalid-name
MODULOS: ModulosT = {}

try:
    for _modulo, (_leiaute, _versao) in MODULOS_PADROES.items():
        carregar_modulo(_modulo, _leiaute, _versao)
except FileNotFoundError as e:
    if not os.environ.get("__CONVERSAO__"):
        raise FileNotFoundError("Um dos módulos não foi encontrado durante a inicialização. O conversor foi executado?") from e
    MODULOS = {}
# pylint: enable=invalid-name
