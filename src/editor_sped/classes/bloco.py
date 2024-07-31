class Bloco:
    def __init__(self, nome_bloco, registro_abertura, registro_fechamento, tipo_efd) -> None:
        self.__nome = nome_bloco
        self.__tipo_efd = tipo_efd

        self.abertura = registro_abertura
        self.fechamento = registro_fechamento

        self.filhos = [self.abertura, self.fechamento]


    def __str__(self) -> str:
        return self.__nome

    def __repr__(self) -> str:
        return f"Bloco({self.__nome})"

    def _json_registros(self):
        return {"nome": self.__nome, "filhos": self.filhos}



    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def tipo_efd(self) -> str:
        return self.__tipo_efd

    @property
    def tamanho(self) -> str:
        # De acordo com o manual SPED ICMS IPI:
        # REGISTRO 0990, CAMPO QTD_LIN_0: "Para este cálculo, o registro 0000, mesmo não pertencendo ao bloco 0, deve ser somado."
        # REGISTRO 9990, CAMPO QTD_LIN_9: "Para este cálculo, o registro 9999, mesmo não pertencendo ao bloco 9, deve ser somado."
        return sum(f.tamanho for f in self.filhos) + (1 if self.__nome in ("0", "9") else 0)
