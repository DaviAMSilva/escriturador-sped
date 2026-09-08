import os

from escriturador_sped.arquivos import abrir_escrituracao
from escriturador_sped.classes.escrituracao import Escrituracao, EscrituracaoEcd, EscrituracaoEcf, EscrituracaoEfdContribuicoes, EscrituracaoEfdIcmsIpi
from escriturador_sped.constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI


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
            if ECD in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoEcd(self.texto(arquivo))
            elif ECF in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoEcf(self.texto(arquivo))
            elif EFD_CONTRIBUICOES in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoEfdContribuicoes(self.texto(arquivo))
            elif EFD_ICMS_IPI in arquivo:
                self.escrituracoes[arquivo] = EscrituracaoEfdIcmsIpi(self.texto(arquivo))
            else:
                raise ValueError(f"Arquivo inválido: {arquivo}")

        return self.escrituracoes[arquivo]


cache = Cache()
