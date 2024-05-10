from typing import *

from .constantes import EFD_ENCODING, EFD_NEWLINE










def limpar_escrituracao(escrituracao_texto):
    escrituracao_texto = escrituracao_texto.splitlines()
    for i, linha in enumerate(escrituracao_texto):
        campos = linha.split("|")
        if len(campos) > 1 and campos[1] == "9999":
            # A escrituração contém o número de linhas e as linhas restantes são descartadas
            # AVISO: Entretanto isso pode gerar um situação em que um arquivo que venha a conter
            # qualquer texto após o registro seja considerado válido apesar de não estar correto.
            return ("\n".join(escrituracao_texto[:i + 1])) + "\n"



def abrir_escrituracao(nome_arquivo: TextIO, limpar_assinatura=True):
    with open(nome_arquivo, "r", encoding=EFD_ENCODING) as arquivo:
        escrituracao_texto = arquivo.read()

    # Decide se a assinatura deve ser ignorada. Como o propósito principal é validação
    # de estrutura a assinatura é ignorada por padrão na abertura do arquivo
    if limpar_assinatura:
        return limpar_escrituracao(escrituracao_texto)
    else:
        return escrituracao_texto



def salvar_escrituracao(nome_arquivo: TextIO, escrituracao_texto: str):
    with open(nome_arquivo, "w", encoding=EFD_ENCODING, newline=EFD_NEWLINE) as output:
        output.write(escrituracao_texto)
