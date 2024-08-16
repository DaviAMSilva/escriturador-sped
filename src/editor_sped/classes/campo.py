from ..tabelas import EFD_INFO










class Campo:
    def __init__(self, valor, registro, numero, tipo_efd) -> str:
        self.numero = numero
        self.valor = valor

        self.tipo_efd = tipo_efd
        self.nome = EFD_INFO[self.tipo_efd][registro]["campos"][self.numero - 1]["nome"]




    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Campo({self.nome})"



    def _json(self):
        return self.valor



    def texto(self):
        return self.valor
