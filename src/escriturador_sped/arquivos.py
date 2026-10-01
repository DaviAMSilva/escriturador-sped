"""Funções de tratamento de arquivos usadas pela biblioteca."""
from pathlib import Path

from .constantes import ENCODING, NEWLINE










def remover_assinatura_escrituracao(escrituracao_texto: str):
    """Remove a assinatura de uma escrituração em forma de texto.

    Args:
        escrituracao_texto: Texto da escrituração contendo a assinatura a ser removida.

    Raises:
        ValueError: Se o registro `|9999|` de fechamento não for encontrado.

    Returns:
        Texto da escrituração com a assinatura removida.
    """
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
    """Abre um arquivo de escrituração.

    Args:
        arquivo: Caminho do arquivo a ser aberto.

    Returns:
        O texto da escrituração aberta.
    """
    with open(arquivo, "r", encoding=ENCODING) as entrada:
        escrituracao_texto = entrada.read()

    # Como o propósito é validação de estrutura a assinatura é removida por padrão na abertura do arquivo
    return remover_assinatura_escrituracao(escrituracao_texto)



def salvar_escrituracao(arquivo: str | Path, texto: str) -> None:
    """Salva um arquivo de escrituração.

    Args:
        arquivo: Caminho do arquivo a ser salvo.
        texto: Texto da escrituração a ser salva.
    """
    with open(arquivo, "w", encoding=ENCODING, newline=NEWLINE) as saida:
        saida.write(texto)
