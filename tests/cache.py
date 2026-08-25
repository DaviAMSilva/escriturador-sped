import os

from escriturador_sped.arquivos import abrir_escrituracao
from escriturador_sped.classes.escrituracao import EfdIcmsIpi, EfdPisCofins, Escrituracao
from escriturador_sped.constantes import EFD_ICMS_IPI, EFD_PIS_COFINS


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
                self.escrituracoes[arquivo] = EfdIcmsIpi(self.texto(arquivo))
            if EFD_PIS_COFINS in arquivo:
                self.escrituracoes[arquivo] = EfdPisCofins(self.texto(arquivo))

        return self.escrituracoes[arquivo]


cache = Cache()
