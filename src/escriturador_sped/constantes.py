# Tipos de escriturações
ECD = "ecd"
ECF = "ecf"
EFD_CONTRIBUICOES = "efd_contribuicoes"
EFD_ICMS_IPI = "efd_icms_ipi"

# Tipos de campo
ALFANUMERICO = "C"
NUMERICO = "N"

# Os manuais forçam a codificação ISO 8859-1 (Latin-1) e o uso de CRLF para as escriturações
ENCODING = "ISO-8859-1"
NEWLINE = "\r\n"

# Maior nível encontrado em ambas EFD
MAIOR_NIVEL = 6

# Ordem em que cada bloco aparece em cada tipo de escrituração
ORDEM_BLOCOS = {
    ECD: ["0", "C", "I", "J", "K", "9"],
    ECF: ["0", "C", "E", "J", "K", "L", "M", "N", "P", "Q", "S", "T", "U", "V", "W", "X", "Y", "9"],
    EFD_CONTRIBUICOES: ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"],
    EFD_ICMS_IPI: ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"]
}
