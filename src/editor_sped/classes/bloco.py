from ..classes.registro import Registro
from ..types import EfdTipo










class Bloco:
    def __init__(self, bloco_nome: str, registro_abertura: Registro, registro_fechamento: Registro, efd_tipo: EfdTipo) -> None:
        self.nome = bloco_nome
        self.efd_tipo = efd_tipo

        self.abertura = registro_abertura
        self.fechamento = registro_fechamento

        self.filhos = [self.abertura, self.fechamento]


    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Bloco({self.nome})"

    def serialize(self) -> dict[str, list[Registro]]:
        return {"nome": self.nome, "filhos": self.filhos}



    @property
    def tamanho(self) -> int:
        # De acordo com o manual SPED ICMS IPI:
        # REGISTRO 0990, CAMPO QTD_LIN_0: "Para este cálculo, o registro |0000|, mesmo não pertencendo ao bloco 0, deve ser somado."
        # REGISTRO 9990, CAMPO QTD_LIN_9: "Para este cálculo, o registro |9999|, mesmo não pertencendo ao bloco 9, deve ser somado."
        return sum(f.tamanho for f in self.filhos) + (1 if self.nome in ("0", "9") else 0)
