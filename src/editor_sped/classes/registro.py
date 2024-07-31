from .campo import Campo










class Registro:
    def __init__(self, campos_texto, tipo_efd) -> None:
        self.filhos = []
        self.pai = None

        campos_lista = campos_texto.split("|")[1:-1]

        self.__nome = campos_lista[0]
        self.__tipo_efd = tipo_efd
        self.campos = [Campo(campo, self.__nome, i + 1, self.__tipo_efd) for i, campo in enumerate(campos_lista)]



    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Registro({self.__nome})"



    def _json_registros(self):
        if self.contem_filhos:
            return {"campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": self.filhos}
        else:
            return f"|{'|'.join([str(c) for c in self.campos])}|"



    def converter_para_texto(self):
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{"".join([f.converter_para_texto() for f in self.filhos])}"



    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def tipo_efd(self) -> str:
        return self.__tipo_efd

    @property
    def tamanho(self) -> str:
        return 1 + sum(f.tamanho for f in self.filhos)

    @property
    def contem_filhos(self):
        return len(self.filhos) >= 1
