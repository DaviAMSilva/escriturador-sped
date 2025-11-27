from typing import overload

from ..classes.campo import Campo
from ..tabelas import EFD_INFO
from ..types import EfdTipo
from .campo_tupla import TuplaCampo
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Registro(ContemRegistros):
    def __init__(self, campos_texto: str, efd_tipo: EfdTipo) -> None:
        campos_textos = campos_texto.split("|")[1:-1]

        super().__init__(campos_textos[0], efd_tipo, ListaRegistro())

        campos_esperados = len(EFD_INFO[self.efd_tipo]["registros"][self.nome]["campos"])

        if len(campos_textos) != campos_esperados:
            raise SyntaxError(f"A quantidade de campos é diferente da quantidade esperada ({len(campos_textos)} ao invés de {campos_esperados})")

        self.pai: Registro | None = None
        self.descricao = EFD_INFO[self.efd_tipo]["registros"][self.nome]["descricao"]

        self.campos = TuplaCampo(Campo(campo, i + 1, self, self.efd_tipo) for i, campo in enumerate(campos_textos))



    @overload
    def __getitem__(self, chave: int | str) -> Campo: ...

    @overload
    def __getitem__(self, chave: slice) -> TuplaCampo: ...

    def __getitem__(self, chave):
        return self.campos[chave]

    def __setitem__(self, chave: int | str, valor: str | int | float | None):
        self.campos[chave].valor = valor



    def serialize(self) -> dict:
        s = super().serialize()
        return {"nome": s["nome"], "campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": s["filhos"]}



    def texto(self) -> str:
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{''.join([f.texto() for f in self.filhos])}"



    @property
    def linha(self) -> str:
        return f"|{'|'.join([str(c) for c in self.campos])}|\n"

    @property
    def tamanho(self) -> int:
        return super().tamanho + 1
