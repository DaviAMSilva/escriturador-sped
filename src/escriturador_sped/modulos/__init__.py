"""Carrega as informações dos módulos para uso pela biblioteca."""
import json
import os
from importlib.resources import files

from ..constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI
from ..tipos import ModulosT, ModuloT


# Controla qual manual de cada módulo será carregado por padrão
MODULOS_NOMES: tuple[ModuloT, ...] = (ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI)
"""Lista dos nomes dos módulos disponíveis na biblioteca."""
MODULOS_PADROES: dict[ModuloT, tuple[str, str]] = {
    ECD: ("009", "2026.01"),
    ECF: ("012", "2026.02"),
    EFD_CONTRIBUICOES: ("006", "1.35"),
    EFD_ICMS_IPI: ("020", "3.2.4")
}
"""Lista dos parâmetros de módulos carregados por padrão."""


# Usado para escolher qual manual a ser carregado
def carregar_modulo(modulo: ModuloT, leiaute: str, manual: str):
    """Carrega uma versão específica de um módulo para ser usado internamente pela biblioteca.

    Args:
        modulo: Nome do módulo a ser carregado.
        leiaute: Versão do leiaute a ser carregado.
        manual: Versão do manual a ser carregado.

    Examples:
        >>> carregar_modulo("efd_icms_ipi", "020", "3.2.4")

    Raises:
        FileNotFoundError: Quando um módulo com os parâmetros informados não existe.
    """
    try:
        with files("escriturador_sped.modulos").joinpath(
            modulo, f"l{leiaute}", f"m{manual.replace('.', '_')}", "modulo.json"
        ).open("r", encoding="utf-8") as arquivo_modulo:
            MODULOS[modulo] = json.loads(arquivo_modulo.read())
    except FileNotFoundError as e:
        raise FileNotFoundError(f"O módulo {(modulo, leiaute, manual)!r} não existe ou não foi encontrado") from e


# pylint: disable=invalid-name
MODULOS: ModulosT = {}
"""Objeto que representa as informações dos registros e campos dos módulos atualmente carregados."""

try:
    for _modulo, (_leiaute, _manual) in MODULOS_PADROES.items():
        carregar_modulo(_modulo, _leiaute, _manual)
except FileNotFoundError as e:
    if not os.environ.get("__CONVERSAO__"):
        raise FileNotFoundError("Um dos módulos padrões não foi encontrado durante a inicialização. O conversor foi executado?") from e
    MODULOS.clear()
# pylint: enable=invalid-name
