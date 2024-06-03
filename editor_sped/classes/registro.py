from ..tabelas import EFD_INFO
from .campo import Campo










class Registro:
    def __init__(self, campos_texto, nome_bloco, tipo_efd) -> None:
        self.campos = []
        self.filhos = []
        self.pai = None

        if type(campos_texto) == str:
            campos_texto = campos_texto.split("|")[1:-1]

        self.bloco = nome_bloco

        self.__nome = campos_texto[0]
        self.__tipo_efd = tipo_efd
        self.campos.extend([Campo(campo, self.__nome, i + 1, self.__tipo_efd) for i, campo in enumerate(campos_texto)])



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
    def contem_filhos(self):
        return len(self.filhos) >= 1
