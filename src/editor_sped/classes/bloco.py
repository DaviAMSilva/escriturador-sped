import re
from typing import Callable, overload

from ..classes.registro import Registro
from ..types import EfdTipo
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Bloco(ContemRegistros):
    def __init__(self, nome: str, registro_abertura: Registro, registro_fechamento: Registro, efd_tipo: EfdTipo) -> None:
        self.abertura = registro_abertura
        self.fechamento = registro_fechamento

        super().__init__(nome, efd_tipo, ListaRegistro([self.abertura, self.fechamento]))



    @overload
    def __getitem__(self, chave: int) -> "Registro": ...

    @overload
    def __getitem__(self, chave: str | re.Pattern | Callable[["Registro"], bool] | slice | None) -> "ListaRegistro": ...

    def __getitem__(self, chave):
        if isinstance(chave, (int, slice)):
            return self.pesquisar()[chave]

        if isinstance(chave, (str, re.Pattern, Callable)) or chave is None:
            return self.pesquisar(chave)

        raise ValueError(f"Valor de pesquisa inválido ({chave})")



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    @property
    def tamanho(self) -> int:
        # De acordo com o manual SPED ICMS IPI:
        # REGISTRO 0990, CAMPO QTD_LIN_0: "Para este cálculo, o registro |0000|, mesmo não pertencendo ao bloco 0, deve ser somado."
        # REGISTRO 9990, CAMPO QTD_LIN_9: "Para este cálculo, o registro |9999|, mesmo não pertencendo ao bloco 9, deve ser somado."
        return super().tamanho + (1 if self.nome in ("0", "9") else 0)
