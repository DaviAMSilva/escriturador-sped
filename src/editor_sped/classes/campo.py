from decimal import Decimal, InvalidOperation
from inspect import signature
from typing import TYPE_CHECKING, Callable

from ..tabelas import EFD_INFO
from ..types import EfdTipo

# Útil para evitar importações circulares
if TYPE_CHECKING:
    from ..classes.registro import Registro










class Campo:
    # Tipos de campo
    ALFANUMERICO = "C"
    NUMERICO = "N"

    @staticmethod
    def valor_para_texto(valor: str | int | float | None, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> str:
        if isinstance(valor, str):
            valor_str = str(valor)[:tamanho]
        elif valor is None:
            valor_str = ""
        elif tamanho_exato:
            tamanho_esquerda = tamanho - (decimal + 1 if decimal else 0)
            tamanho_direita = decimal if decimal else 0
            valor_str = f"{valor:0{tamanho_esquerda}.{tamanho_direita}f}" if decimal else f"{int(valor):0{tamanho_esquerda}d}".replace(".", ",")
        else:
            valor_str = f"{valor:.{decimal or 0}f}" if decimal else str(int(valor)).replace(".", ",")

        return valor_str

    @staticmethod
    def texto_para_valor(valor: str, decimal: int | None) -> int | float | None:
        if valor in ("", None):
            return None

        if decimal:
            return float((valor or "").replace(",", "."))

        return int(valor)



    def __init__(self, valor: str | int | float | None, numero: int, registro_pai: "Registro", efd_tipo: EfdTipo) -> None:
        self.efd_tipo: EfdTipo = efd_tipo
        self.registro_pai = registro_pai

        info_campos = EFD_INFO[efd_tipo]["registros"][self.registro_pai.nome]["campos"][numero - 1]

        # fmt: off
        self.nome          = info_campos["nome"]
        self.descricao     = info_campos["descricao"]

        self.decimal       = info_campos["decimal"]
        self.numero        = info_campos["numero"]
        self.obrigatorio   = info_campos["obrigatorio"]
        self.tamanho       = info_campos["tamanho"]
        self.tamanho_exato = info_campos["tamanho_exato"]
        self.tipo          = info_campos["tipo"]
        # fmt: on

        self._valor_alfanumerico: str = ""
        self._valor_numerico: Decimal | None = None
        self._retorna_valor: Callable[[], str | int | float] | None = None

        # Converte o valor inicial se necessário
        self.valor = valor



    def __str__(self) -> str:
        return self.texto()

    def __repr__(self) -> str:
        return f"Campo({self.nome})"



    def serialize(self) -> str:
        return self.texto()



    def texto(self) -> str:
        if self._retorna_valor:
            return Campo.valor_para_texto(self._retorna_valor(), self.decimal, self.tamanho, self.tamanho_exato)

        return self._valor_alfanumerico



    @property
    def valor(self) -> str | int | float | None:
        if self.tipo == Campo.ALFANUMERICO:
            return self.valor_c

        if self.tipo == Campo.NUMERICO:
            return self.valor_n

        raise ValueError(f"Tipo de campo desconhecido: {self.tipo}")

    @valor.setter
    def valor(self, valor: str | int | float | None) -> None:
        if isinstance(valor, (str, int, float)) or valor is None:
            if self.tipo == Campo.ALFANUMERICO:
                self.valor_c = valor
            elif self.tipo == Campo.NUMERICO:
                self.valor_n = valor
            else:
                raise ValueError(f"Tipo de campo desconhecido: {self.tipo}")
        else:
            raise TypeError(f"O valor para o campo '{self.nome}' deve ser str, int, float ou None")



    @property
    def valor_n(self) -> int | float | None:
        if self._valor_numerico is None:
            return None

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n.setter
    def valor_n(self, valor: str | int | float | None) -> None:
        if self._retorna_valor:
            raise ValueError("Não é possível definir o valor de um campo configurado")

        if not (isinstance(valor, (str, int, float)) or valor is None):
            raise TypeError(f"O valor para o campo '{self.nome}' deve ser str, int, float ou None")

        try:
            self._valor_numerico = Decimal(str(valor).replace(",", ".")) if valor not in ("", None) else None
            self._valor_alfanumerico = Campo.valor_para_texto(
                float(self._valor_numerico) if self.decimal else int(self._valor_numerico),
                self.decimal,
                self.tamanho,
                self.tamanho_exato
            ) if self._valor_numerico is not None else ""
        except InvalidOperation as e:
            raise ValueError(f"Não foi possível converter valor para Decimal ({valor})") from e

    @property
    def valor_c(self) -> str:
        return self._valor_alfanumerico

    @valor_c.setter
    def valor_c(self, valor: str | int | float | None) -> None:
        if self._retorna_valor:
            raise ValueError("Não é possível definir o valor de um campo configurado")

        if not (isinstance(valor, (str, int, float)) or valor is None):
            raise TypeError(f"O valor para o campo '{self.nome}' deve ser str, int, float ou None")

        self._valor_alfanumerico = str(valor)[:self.tamanho] if valor not in ("", None) else ""

        if self.tipo == Campo.ALFANUMERICO:
            self._valor_numerico = None
        elif self.tipo == Campo.NUMERICO:
            novo_valor_n = Campo.texto_para_valor(self._valor_alfanumerico, self.decimal)

            self._valor_numerico = Decimal(str(novo_valor_n)) if novo_valor_n not in ("", None) else None
        else:
            raise ValueError(f"Tipo de campo desconhecido: {self.tipo}")



    def configurar_valor(self, retorna_valor: Callable[[], str | int | float]) -> None:
        # Verifica se retorna_valor é uma função sem argumentos e retorna str
        if not callable(retorna_valor):
            raise ValueError(f"O parâmetro '{retorna_valor}' não é uma função")

        sig = signature(retorna_valor)
        if len(sig.parameters) != 0:
            raise TypeError("A função fornecida não deve conter argumentos")
        if sig.return_annotation not in (sig.empty, str, int, float):
            raise TypeError("A função fornecida deve retornar str, int, float ou None")

        self._retorna_valor = retorna_valor

    def desconfigurar_valor(self) -> None:
        self._retorna_valor = None
        self._valor_alfanumerico = ""
        self._valor_numerico = None
