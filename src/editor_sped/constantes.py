EFD_TIPOS = "efd_icms_ipi", "efd_pis_cofins"

# Os manuais forçam a codificação ISO 8859-1 (Latin-1) e o uso de CRLF para as escriturações
EFD_ENCODING = "ISO-8859-1"
EFD_NEWLINE = "\r\n"

# Maior nível encontrado em ambas EFD
EFD_MAIOR_NIVEL = 6

# Ordem em que cada bloco aparece em cada tipo de escrituração
EFD_ORDEM_BLOCOS = {
    "efd_icms_ipi": ["0", "B", "C", "D", "E", "G", "H", "K", "1", "9"],
    "efd_pis_cofins": ["0", "A", "C", "D", "F", "I", "M", "P", "1", "9"]
}
