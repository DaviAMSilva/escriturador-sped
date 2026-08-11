from typing import TypeVar

# Tipos de escriturações
EFD_ICMS_IPI = "efd_icms_ipi"
EFD_PIS_COFINS = "efd_pis_cofins"

EFD_TIPOS = EFD_ICMS_IPI, EFD_PIS_COFINS

# Tipos de campo
ALFANUMERICO = "C"
NUMERICO = "N"

# Os manuais forçam a codificação ISO 8859-1 (Latin-1) e o uso de CRLF para as escriturações
EFD_ENCODING = "ISO-8859-1"
EFD_NEWLINE = "\r\n"

# Maior nível encontrado em ambas EFD
EFD_MAIOR_NIVEL = 6

# Ordem em que cada bloco aparece em cada tipo de escrituração
EFD_ORDEM_BLOCOS = {
    EFD_ICMS_IPI: ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"],
    EFD_PIS_COFINS: ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"]
}

# Tipos para pesquisa e criação
Chave = str | int
ChaveT = TypeVar("ChaveT", bound=Chave)
# pylint: disable=invalid-name
ValorC = str
ValorN = int | float | None
ValorN0 = int | float
Valor = ValorC | ValorN
Valor0 = ValorC | ValorN0
# pylint: enable=invalid-name
