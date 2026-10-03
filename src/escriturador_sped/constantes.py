"""Constantes usadas pela biblioteca."""

# Tipos de escriturações
ECD = "ecd"
"""Nome para uma Escrituração Contábil Digital."""
ECF = "ecf"
"""Nome para uma Escrituração Contábil Fiscal."""
EFD_CONTRIBUICOES = "efd_contribuicoes"
"""Nome para uma Escrituração Fiscal Digital Contribuições."""
EFD_ICMS_IPI = "efd_icms_ipi"
"""Nome para uma Escrituração Fiscal Digital ICMS IPI."""

# Tipos de campo
ALFANUMERICO = "C"
"""Código para campo do tipo alfanumérico."""
NUMERICO = "N"
"""Código para campo do tipo numérico."""

# Os manuais forçam a codificação ISO 8859-1 (Latin-1) e o uso de CRLF para as escriturações
ENCODING = "ISO-8859-1"
"""Codificação para um arquivo de escrituração."""
NEWLINE = "\r\n"
"""Quebra de linha para um arquivo de escrituração."""

# Maior nível encontrado em ambas EFD
MAIOR_NIVEL = 6
"""Maior nível de recursão de registros possível em uma escrituração."""

# Ordem em que cada bloco aparece em cada tipo de escrituração
ORDEM_BLOCOS = {
    ECD: ["0", "C", "I", "J", "K", "9"],
    ECF: ["0", "C", "E", "J", "K", "L", "M", "N", "P", "Q", "S", "T", "U", "V", "W", "X", "Y", "9"],
    EFD_CONTRIBUICOES: ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"],
    EFD_ICMS_IPI: ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"]
}
"""Ordem dos blocos de cada tipo de escrituração."""
