from .campo import Campo










class Registro:
    def __init__(self, campos_texto, tipo_efd) -> None:
        self.filhos = []
        self.pai = None

        campos_lista = campos_texto.split("|")[1:-1]

        self.nome = campos_lista[0]
        self.tipo_efd = tipo_efd
        self.campos = [Campo(campo, self.nome, i + 1, self.tipo_efd) for i, campo in enumerate(campos_lista)]



    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Registro({self.nome})"



    def _json(self):
        if self.contem_filhos:
            return {"campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": self.filhos}
        else:
            return f"|{'|'.join([str(c) for c in self.campos])}|"



    def linha(self):
        return f"|{'|'.join([str(c) for c in self.campos])}|\n"

    def texto(self):
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{"".join([f.texto() for f in self.filhos])}"



    @property
    def tamanho(self) -> str:
        return 1 + sum(f.tamanho for f in self.filhos)

    @property
    def contem_filhos(self):
        return len(self.filhos) >= 1
