import os

from editor_sped.classes.escrituracao import Escrituracao, EscrituracaoICMSIPI, EscrituracaoPISCOFINS
from editor_sped.constantes import EFD_ICMS_IPI, EFD_PIS_COFINS
from editor_sped.utilidades import abrir_escrituracao


class Cache():
    def __init__(self) -> None:
        self.textos: dict[str, str] = {}
        self.escrituracoes: dict[str, Escrituracao] = {}

    def texto(self, arquivo: str) -> str:
        if arquivo not in self.textos:
            self.textos[arquivo] = abrir_escrituracao(os.path.join("exemplos", arquivo))

        return self.textos[arquivo]

    def escrituracao(self, arquivo: str) -> Escrituracao:
        if arquivo not in self.escrituracoes:
            if EFD_ICMS_IPI in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoICMSIPI(self.texto(arquivo))
            if EFD_PIS_COFINS in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoPISCOFINS(self.texto(arquivo))

        return self.escrituracoes[arquivo]


cache = Cache()
