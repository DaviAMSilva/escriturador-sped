from ..classes.campo import Campo
from ..tabelas import EFD_INFO
from ..types import EfdTipo
from .contem_registros import ContemRegistros










class Registro(ContemRegistros):
    def __init__(self, campos_texto: str, efd_tipo: EfdTipo) -> None:
        campos_lista = campos_texto.split("|")[1:-1]

        super().__init__(campos_lista[0], efd_tipo, [])

        self.pai: Registro | None
        self.descricao = EFD_INFO[self.efd_tipo]["registros"][self.nome]["descricao"]
        self.campos = tuple(Campo(campo, self, i + 1, self.efd_tipo) for i, campo in enumerate(campos_lista))



    def serialize(self) -> dict:
        s = super().serialize()
        return {"nome": s["nome"], "campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": s["filhos"]}

    def linha(self) -> str:
        return f"|{'|'.join([str(c) for c in self.campos])}|\n"

    def texto(self) -> str:
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{"".join([f.texto() for f in self.filhos])}"



    @property
    def tamanho(self) -> int:
        return super().tamanho + 1
