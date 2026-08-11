from typing import Iterable, Mapping

from ..modulos import ModuloT
from ..tipos import ChaveT, Valor
from .registro import Registro
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Bloco(ContemRegistros):
    def __init__(self, nome: str, registro_abertura: Registro, registro_fechamento: Registro, modulo: ModuloT) -> None:
        self.abertura = registro_abertura
        self.fechamento = registro_fechamento

        super().__init__(nome.upper(), ListaRegistro([self.abertura, self.fechamento]), modulo)



    def __getitem__(self, chave: str | tuple[str, Mapping[ChaveT, Valor | Iterable[Valor]]]) -> ListaRegistro:
        if isinstance(chave, str):
            return self.filhos.buscar(chave)

        if isinstance(chave, tuple) and len(chave) == 2:
            if (isinstance(chave[0], str) or chave[0] is None) and (isinstance(chave[1], dict) or chave[1] is None):
                return self.buscar(chave[0], chave[1])

            raise TypeError(f"Tupla com valores inválidos ({chave})")

        raise TypeError(f"Valor inválido ({chave})")

    def __contains__(self, chave: str):
        return bool(self.filhos.buscar(chave, primeiro=True))



    def __str__(self) -> str:
        return f"Bloco {self.nome}: {self.tamanho} linhas"

    def __repr__(self) -> str:
        return f"Bloco({self.nome!r}, tamanho={self.tamanho!r})"



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    @property
    def tamanho(self) -> int:
        # De acordo com o manual SPED ICMS IPI:
        # REGISTRO 0990, CAMPO QTD_LIN_0: "Para este cálculo, o registro |0000|, mesmo não pertencendo ao bloco 0, deve ser somado."
        # REGISTRO 9990, CAMPO QTD_LIN_9: "Para este cálculo, o registro |9999|, mesmo não pertencendo ao bloco 9, deve ser somado."
        return super().tamanho + (1 if self.nome in ("0", "9") else 0)
