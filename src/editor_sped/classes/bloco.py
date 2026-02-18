from ..types import EfdTipo
from .registro import Registro
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Bloco(ContemRegistros):
    def __init__(self, nome: str, registro_abertura: Registro, registro_fechamento: Registro, efd_tipo: EfdTipo) -> None:
        self.abertura = registro_abertura
        self.fechamento = registro_fechamento

        super().__init__(nome, ListaRegistro([self.abertura, self.fechamento]), efd_tipo)



    def __getitem__(self, chave: str) -> ListaRegistro:
        return self.filhos.buscar(chave)

    def __contains__(self, chave: str):
        return bool(self.filhos.buscar(chave, primeiro=True))



    def __str__(self) -> str:
        return f"Bloco {self.nome}: {self.tamanho} linhas"

    def __repr__(self) -> str:
        return f"Bloco({repr(self.nome)}, tamanho={repr(self.tamanho)})"



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    @property
    def tamanho(self) -> int:
        # De acordo com o manual SPED ICMS IPI:
        # REGISTRO 0990, CAMPO QTD_LIN_0: "Para este cálculo, o registro |0000|, mesmo não pertencendo ao bloco 0, deve ser somado."
        # REGISTRO 9990, CAMPO QTD_LIN_9: "Para este cálculo, o registro |9999|, mesmo não pertencendo ao bloco 9, deve ser somado."
        return super().tamanho + (1 if self.nome in ("0", "9") else 0)
