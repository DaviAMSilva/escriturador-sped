import json

with open("tabelas/efd_info.json", newline="", encoding="utf-8") as __efd_info_arquivo:
    EFD_INFO = json.loads(__efd_info_arquivo.read())
