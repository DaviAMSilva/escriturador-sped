from ..tabelas import EFD_INFO










class Campo:
    def __init__(self, valor, registro, numero, tipo_efd) -> str:
        self.numero = numero
        self.valor = valor

        self.tipo_efd = tipo_efd
        self.__nome = EFD_INFO[self.tipo_efd][registro]["campos"][self.numero - 1]["nome"]




    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Campo({self.__nome})"



    def _json_registros(self):
        return self.valor



    @property
    def nome(self) -> str:
        return self.__nome
