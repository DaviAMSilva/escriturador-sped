from ..constantes import EFD_MAIOR_NIVEL
from ..tabelas import EFD_INFO
from .registro import Registro










class Bloco:
    def __init__(self, nome_bloco, registros_texto, tipo_efd) -> None:
        self.registro_inicial = None
        self.registro_final = None

        self.__nome = nome_bloco
        self.tipo_efd = tipo_efd

        if type(registros_texto) == str:
            registros_texto = registros_texto.split("\n")

        if (not registros_texto[0].startswith(f"|{self.__nome}001|")) or (not registros_texto[-1].startswith(f"|{self.__nome}990|")):
            raise ValueError("Bloco não começa e termina com |_001| e |_990|")

        self.registro_inicial = Registro(registros_texto.pop(0), 1, self.__nome, self.tipo_efd)
        self.registro_final = Registro(registros_texto.pop(-1), 1, self.__nome, self.tipo_efd)

        self.filhos = [self.registro_inicial, self.registro_final]

        self.ler_registros(registros_texto)



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Bloco({self.__nome})"

    def _json_registros(self):
        return {"nome": self.__nome, "filhos": self.filhos}



    @property
    def nome(self) -> str:
        return self.__nome



    def ler_registros(self, registros_texto):
        # self.registros = self.registro_inicial.filhos

        # Lista do último registro visitado em cada nível
        ultimos_registros = [None for _ in range(EFD_MAIOR_NIVEL + 1)]
        ultimos_registros[1] = self.registro_inicial
        nivel_anterior = 1

        # Para cada registro informado
        for registro_atual in registros_texto:
            # Pega o nome do registro e encontra o seu nível dentro da tabela
            nivel_atual = EFD_INFO[self.tipo_efd][registro_atual.split("|")[1]]["nivel"]

            # Compara o nível do registro anterior com o nível do registro atual
            if nivel_atual > nivel_anterior + 1:
                # Se a diferença entre o nível anterior e o atual for maior que 1 positivo há um erro de estrutura
                raise ValueError(f"Registros foram da ordem válida. De ${nivel_anterior} para ${nivel_atual}")
            elif nivel_atual == nivel_anterior + 1 or nivel_atual <= nivel_anterior:
                ultimos_registros[nivel_atual] = Registro(registro_atual, nivel_atual, self.__nome, self.tipo_efd)

            # Adicionamos o registro atual como filho do registro acima dele (nível - 1)
            # De maneira inversa criamos a ligação do registro filho com o registro pai
            ultimos_registros[nivel_atual - 1].filhos.append(ultimos_registros[nivel_atual])
            ultimos_registros[nivel_atual].pai = ultimos_registros[nivel_atual - 1]

            # O nível anterior foi alterado
            nivel_anterior = nivel_atual
