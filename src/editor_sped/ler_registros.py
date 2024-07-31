from .constantes import EFD_MAIOR_NIVEL
from .classes.registro import Registro
from .tabelas import EFD_INFO










def ler_registros(registros_texto: str | list[str], tipo_efd: str):
    nivel_anterior = -1

    # Lista do último registro visitado em cada nível
    ultimos_registros = [None for _ in range(EFD_MAIOR_NIVEL + 1)]

    # Para a lista atual de registros é usado para os registros que estão na raiz e não têm pais
    registros_raiz = []

    # Para cada registro informado
    for registro_atual in registros_texto.splitlines():
        # Pega o nome do registro e encontra o seu nível dentro da tabela
        nivel_atual = EFD_INFO[tipo_efd][registro_atual.split("|")[1]]["nivel"]

        # Compara o nível do registro anterior com o nível do registro atual
        if nivel_atual > nivel_anterior + 1:
            # Se a diferença entre o nível anterior e o atual for maior que 1 positivo há um erro de estrutura
            raise ValueError(f"Registros fora da ordem válida. De {nivel_anterior} para {nivel_atual}.")

        ultimos_registros[nivel_atual] = Registro(registro_atual, tipo_efd)

        # Verificar se existe um registro pai válido
        if nivel_atual - 1 >= 0 and not ultimos_registros[nivel_atual - 1] == None:
            # Se existir:
            # Adicionamos o registro atual como filho do registro acima dele (nível - 1)
            # De maneira inversa criamos a ligação do registro filho com o registro pai
            ultimos_registros[nivel_atual - 1].filhos.append(ultimos_registros[nivel_atual])
            ultimos_registros[nivel_atual].pai = ultimos_registros[nivel_atual - 1]
        else:
            # Se não existir:
            # Adicionamos o registro na lista de registros raízes da lista de registros atuais
            registros_raiz.append(ultimos_registros[nivel_atual])

        # O nível anterior foi alterado
        nivel_anterior = nivel_atual

    return registros_raiz
