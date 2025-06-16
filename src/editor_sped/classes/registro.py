from ..classes.campo import Campo
from ..tabelas import EFD_INFO
from ..types import EfdTipo










class Registro:
    def __init__(self, campos_texto: str, efd_tipo: EfdTipo) -> None:
        self.filhos: list[Registro] = []
        self.pai: Registro

        campos_lista = campos_texto.split("|")[1:-1]

        self.nome = campos_lista[0]
        self.efd_tipo = efd_tipo
        self.descricao = EFD_INFO[self.efd_tipo]["registros"][self.nome]["descricao"]
        self.campos = [Campo(campo, self.nome, i + 1, self.efd_tipo) for i, campo in enumerate(campos_lista)]



    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Registro({self.nome})"



    def serialize(self) -> dict:
        return {"campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": self.filhos}



    def linha(self) -> str:
        return f"|{'|'.join([str(c) for c in self.campos])}|\n"

    def texto(self) -> str:
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{"".join([f.texto() for f in self.filhos])}"



    @property
    def tamanho(self) -> int:
        return 1 + sum(f.tamanho for f in self.filhos)

    @property
    def contem_filhos(self) -> bool:
        return len(self.filhos) >= 1
