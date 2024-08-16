from ..tabelas import EFD_INFO










class Campo:
    def __init__(self, valor, registro, numero, tipo_efd) -> str:
        self.numero = numero
        self.__valor = valor

        self.tipo_efd = tipo_efd
        self.nome = EFD_INFO[self.tipo_efd][registro]["campos"][self.numero - 1]["nome"]




    def __str__(self) -> str:
        return self.__valor

    def __repr__(self) -> str:
        return f"Campo({self.nome})"



    def _json(self):
        return self.__valor



    @property
    def valor(self):
        return self.__valor



    def texto(self):
        return self.__valor



class CampoCalculado(Campo):
    def __init__(self, valor, registro, numero, tipo_efd, retorna_valor):
        super.__init__()
        self.__retorna_valor = retorna_valor

    @property
    def valor(self):
        return self.__retorna_valor()
