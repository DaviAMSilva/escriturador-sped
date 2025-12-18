from typing import Callable, Self, overload

from ..constantes import EFD_ORDEM_BLOCOS
from ..efd_info import EFD_INFO
from ..types import EfdTipo
from .campo import Campo
from .campo_tupla import TuplaCampo
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Registro(ContemRegistros):
    @staticmethod
    def ordem(nome: str, efd_tipo: EfdTipo) -> int:
        # Exemplos:
        # 0100 ->    0 + 100 =  100
        # C500 -> 2000 + 500 = 2500
        return EFD_ORDEM_BLOCOS[efd_tipo].index(nome[0]) * 1000 + int(nome[1:4])

    @staticmethod
    def ler(registros_texto: str, efd_tipo: EfdTipo) -> ListaRegistro:
        from .registro_ler import ler_registros # pylint: disable=import-outside-toplevel,cyclic-import
        return ler_registros(registros_texto, efd_tipo)



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
        if isinstance(chave, int):
            if chave == 0:
                raise IndexError("Os campos de um registro têm a numeração iniciada pelo número 1")

            return self.campos[chave - 1] if chave > 0 else self.campos[chave]

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



    def adicionar(self, registros: "Registro | ListaRegistro | list[Registro]") -> Self:
        registros = [registros] if isinstance(registros, Registro) else registros

        for novo_registro in registros:
            if not isinstance(novo_registro, Registro):
                raise TypeError(f"Item não é um registro ({novo_registro})")

            if novo_registro.nome not in EFD_INFO[self.efd_tipo]["registros"][self.nome]["filhos"]:
                raise ValueError(f"O registro {novo_registro} não é um filho válido de {self}")

            for i, filho in enumerate(self.filhos):
                if Registro.ordem(novo_registro.nome, self.efd_tipo) < Registro.ordem(filho.nome, self.efd_tipo):
                    self.filhos.insert(i, novo_registro)
                    break
            else:
                self.filhos.append(novo_registro)

        return self

    def remover(self, registros: "Registro | ListaRegistro | list[Registro]" | Callable[["Registro"], bool]) -> Self:
        registros = [registros] if isinstance(registros, Registro) else registros

        if callable(registros):
            for i in range(len(self.filhos) - 1, -1, -1):
                if registros(self.filhos[i]):
                    del self.filhos[i]
        else:
            registros_set = set(registros)
            for i in range(len(self.filhos) - 1, -1, -1):
                if self.filhos[i] in registros_set:
                    del self.filhos[i]

        return self
