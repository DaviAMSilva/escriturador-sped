# Tipos de escriturações
EFD_ICMS_IPI = "efd_icms_ipi"
EFD_PIS_COFINS = "efd_pis_cofins"

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
    EFD_ICMS_IPI: ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"],
    EFD_PIS_COFINS: ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"]
}
