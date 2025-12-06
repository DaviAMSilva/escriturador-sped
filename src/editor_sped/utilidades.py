from .constantes import EFD_ENCODING, EFD_NEWLINE, EFD_ORDEM_BLOCOS
from .types import EfdTipo










def remover_assinatura_escrituracao(escrituracao_texto: str):
    escrituracao_linhas = escrituracao_texto.splitlines()
    for i, linha in enumerate(escrituracao_linhas):
        campos = linha.split("|")
        if len(campos) > 1 and campos[1] == "9999":
            # A escrituração contém o número de linhas e as linhas restantes são descartadas
            # AVISO: Isso pode gerar um situação em que um arquivo que venha a conter qualquer
            # texto após o registro seja considerado válido apesar de não estar correto.
            return ("\n".join(escrituracao_linhas[:i + 1])) + "\n"

    raise ValueError("Registro |9999| de fechamento não encontrado")



def abrir_escrituracao(arquivo_nome: str, remover_assinatura: bool = True) -> str:
    with open(arquivo_nome, "r", encoding=EFD_ENCODING) as arquivo:
        escrituracao_texto = arquivo.read()

    # Decide se a assinatura deve ser removida. Como o propósito principal é validação
    # de estrutura a assinatura é removida por padrão na abertura do arquivo
    if remover_assinatura:
        return remover_assinatura_escrituracao(escrituracao_texto)

    return escrituracao_texto



def salvar_escrituracao(arquivo_nome: str, escrituracao_texto: str) -> None:
    with open(arquivo_nome, "w", encoding=EFD_ENCODING, newline=EFD_NEWLINE) as output:
        output.write(escrituracao_texto)



def registro_key(nome: str, efd_tipo: EfdTipo) -> int:
    # Exemplos:
    # 0100 ->    0 + 100 =  100
    # C500 -> 2000 + 500 = 2500
    return EFD_ORDEM_BLOCOS[efd_tipo].index(nome[0]) * 1000 + int(nome[1:4])
