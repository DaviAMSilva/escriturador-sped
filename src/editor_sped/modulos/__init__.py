from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..efd_info import EfdTipo

# Controla qual versão de cada módulo será carregada por padrão
MODULOS_PADROES: dict["EfdTipo", tuple[str, str]] = {
    "contribuicoes": ("006", "1.35"),
    "icms_ipi": ("020", "3.2.3")
}
