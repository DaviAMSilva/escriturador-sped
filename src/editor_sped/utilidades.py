from pathlib import Path

from .constantes import EFD_ENCODING, EFD_NEWLINE










def remover_assinatura_escrituracao(escrituracao_texto: str):
    linhas = escrituracao_texto.splitlines()
    for i, linha in enumerate(linhas):
        campos = linha.split("|")
        if len(campos) > 1 and campos[1] == "9999":
            # A escrituração contém o número de linhas e as linhas restantes são descartadas
            # AVISO: Isso pode gerar um situação em que um arquivo que venha a conter qualquer
            # texto após o registro seja considerado válido apesar de não estar correto.
            return ("\n".join(linhas[:i + 1])) + "\n"

    raise ValueError("Registro |9999| de fechamento não encontrado")



def abrir_escrituracao(arquivo: str | Path) -> str:
    with open(arquivo, "r", encoding=EFD_ENCODING) as entrada:
        escrituracao_texto = entrada.read()

    # Como o propósito é validação de estrutura a assinatura é removida por padrão na abertura do arquivo
    return remover_assinatura_escrituracao(escrituracao_texto)



def salvar_escrituracao(arquivo: str | Path, texto: str) -> None:
    with open(arquivo, "w", encoding=EFD_ENCODING, newline=EFD_NEWLINE) as saida:
        saida.write(texto)
