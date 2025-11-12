from .classes.registro import Registro
from .constantes import EFD_MAIOR_NIVEL
from .tabelas import EFD_INFO
from .types import EfdTipo










def ler_registros(registros_texto: str, efd_tipo: EfdTipo) -> list[Registro]:
    if registros_texto == "" or not isinstance(registros_texto, str):
        return []

    nivel_anterior = -1

    # Lista do último registro visitado em cada nível
    ultimos_registros: list[Registro | None] = [None for _ in range(EFD_MAIOR_NIVEL + 1)]

    # Para a lista atual de registros é usado para os registros que estão na raiz e não têm pais
    registros_raiz: list[Registro] = []

    # Para cada registro informado
    for registro_atual in registros_texto.splitlines():
        registro_atual_campos = registro_atual.split("|")

        # Um registro precisa começar e iniciar com o caractere |
        if registro_atual_campos[0] != "" or registro_atual_campos[-1] != "":
            raise SyntaxError(f"Linha inválida, o início ou o fim da linha não estão presentes ({registro_atual})")

        # Um registro precisa ter no mínimo dois campos mais um início e um fim
        if len(registro_atual_campos) < 4:
            raise SyntaxError(f"Linha inválida, quantidade insuficiente de campos ({registro_atual})")

        try:
            # Pega o nome do registro e encontra o seu nível dentro da tabela
            nivel_atual = EFD_INFO[efd_tipo]["registros"][registro_atual_campos[1]]["nivel"]
        except KeyError as e:
            # O registro não existe ou a linha foi mal-formatada
            raise KeyError(f"Linha inválida, registro não encontrado ({registro_atual})") from e

        # Compara o nível do registro anterior com o nível do registro atual
        if nivel_atual > nivel_anterior + 1 and nivel_anterior != -1:
            # Se a diferença entre o nível anterior e o atual for maior que 1 positivo há um erro de estrutura
            raise SyntaxError(f"Registros fora da ordem válida. (de {nivel_anterior} para {nivel_atual})")

        ultimos_registros[nivel_atual] = Registro(registro_atual, efd_tipo)

        ultimos_registros_registro_atual = ultimos_registros[nivel_atual]
        ultimos_registros_registro_anterior = ultimos_registros[nivel_atual - 1]
        if ultimos_registros_registro_atual is not None:
            # Verificamos se existe um registro pai válido
            if nivel_atual - 1 >= 0 and ultimos_registros_registro_anterior is not None:
                # Se existir:
                # Adicionamos o registro atual como filho do registro acima dele (nível - 1)
                # De maneira inversa criamos a ligação do registro filho com o registro pai
                ultimos_registros_registro_anterior.filhos.append(ultimos_registros_registro_atual)
                ultimos_registros_registro_atual.pai = ultimos_registros_registro_anterior
            else:
                # Se não existir:
                # Adicionamos o registro na lista de registros raízes da lista de registros atuais
                registros_raiz.append(ultimos_registros_registro_atual)

        # O nível anterior foi alterado
        nivel_anterior = nivel_atual

    return registros_raiz
