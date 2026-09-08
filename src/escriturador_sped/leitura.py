from typing import Iterable

from .classes.registro import Registro
from .constantes import MAIOR_NIVEL
from .estruturas.lista_registro import ListaRegistro
from .modulos import MODULOS, ModuloT










def ler_registros(registros: str | Iterable[str], modulo: ModuloT) -> ListaRegistro[Registro]:
    if not registros or not isinstance(registros, (str, Iterable)):
        raise TypeError(f"Tipo inválido para parâmetro 'registros' ({registros})")

    # Transformando em lista
    if isinstance(registros, str):
        registros = registros.splitlines()

    nivel_anterior = -1

    # Lista do último registro visitado em cada nível
    ultimos_registros: list[Registro | None] = [None for _ in range(MAIOR_NIVEL + 1)]

    # Para a lista atual de registros é usado para os registros que estão na raiz e não têm pais
    registros_raiz = ListaRegistro[Registro]()

    # Para cada registro informado
    for registro_atual in registros:
        if not registro_atual or not isinstance(registro_atual, str):
            raise TypeError(f"Tipo inválido para parâmetro 'registros' ({registro_atual})")

        registro_atual_campos = registro_atual.split("|")

        # Um registro precisa começar e iniciar com o caractere |
        if registro_atual_campos[0] != "" or registro_atual_campos[-1] != "":
            raise SyntaxError(f"Linha inválida, o início ou o fim da linha não estão presentes ({registro_atual})")

        # Um registro precisa ter no mínimo dois campos mais um início e um fim
        if len(registro_atual_campos) < 4:
            raise SyntaxError(f"Linha inválida, quantidade insuficiente de campos ({registro_atual})")

        try:
            # Pega o nome do registro e encontra o seu nível dentro do leiaute do módulo
            nivel_atual = MODULOS[modulo]["registros"][registro_atual_campos[1]]["nivel"]
        except KeyError as e:
            # O registro não existe ou a linha foi mal-formatada
            raise KeyError(f"Linha inválida, registro não encontrado ({registro_atual})") from e

        # Compara o nível do registro anterior com o nível do registro atual
        if nivel_atual > nivel_anterior + 1 and nivel_anterior != -1:
            # Se a diferença entre o nível anterior e o atual for maior que 1 positivo há um erro de estrutura
            raise SyntaxError(f"Registros fora da ordem válida. (de {nivel_anterior} para {nivel_atual})")



        # Criando o objeto registro em si
        ultimos_registros[nivel_atual] = Registro(modulo, registro_atual)



        ultimos_registros_registro_atual = ultimos_registros[nivel_atual]
        ultimos_registros_registro_anterior = ultimos_registros[nivel_atual - 1]

        if ultimos_registros_registro_atual is not None:
            # Verificamos se existe um registro pai com nível válido
            if nivel_atual - 1 >= 0 and ultimos_registros_registro_anterior is not None:
                # Verificamos se existe um registro pai com nome válido
                if MODULOS[modulo]["registros"][ultimos_registros_registro_atual.nome]["pai"] != ultimos_registros_registro_anterior.nome:
                    raise SyntaxError(f"{ultimos_registros_registro_atual!r} não é um filho válido de {ultimos_registros_registro_anterior!r}")

                # Se existir e for válido:
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
