from ..efd_info import EFD_INFO
from ..types import EfdTipo










type Alfanumerico = str
type Numerico = int | float | None
type Numerico0 = int | float










class Campo:
    # Tipos de campo
    ALFANUMERICO = "C"
    NUMERICO = "N"



    @staticmethod
    def alfanumerico(valor: Alfanumerico | Numerico, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> Alfanumerico:
        if isinstance(valor, str):
            return valor[:tamanho]

        if valor is None:
            return ""

        if tamanho_exato:
            tamanho_esquerda = tamanho - (decimal + 1 if decimal else 0)
            tamanho_direita = decimal if decimal else 0

            if decimal:
                return f"{valor:0{tamanho_esquerda}.{tamanho_direita}f}".replace(".", ",")

            return f"{int(valor):0{tamanho_esquerda}d}".replace(".", ",")

        if decimal:
            return f"{valor:.{decimal}f}".replace(".", ",")

        return str(int(valor)).replace(".", ",")

    @staticmethod
    def numerico(valor: Alfanumerico | Numerico, decimal: int | None) -> Numerico:
        if valor in ("", None):
            return None

        if isinstance(valor, str):
            if decimal:
                return float(valor.replace(",", "."))

            return int(valor.replace(",", "."))

        if decimal:
            return float(valor)

        return int(valor)



    def __init__(self, valor: Alfanumerico | Numerico, nome_registro: str, numero: int, efd_tipo: EfdTipo) -> None:
        self.nome_registro = nome_registro
        self.efd_tipo = efd_tipo

        info_campos = EFD_INFO[efd_tipo]["registros"][nome_registro]["campos"][numero - 1]

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

        self._valor_alfanumerico: Alfanumerico = ""
        self._valor_numerico: Numerico = None

        # Converte o valor inicial se necessário
        self.valor = valor



    def __str__(self) -> str:
        return self.texto()

    def __repr__(self) -> str:
        return f"Campo({repr(self.nome_registro)}, {repr(self.nome)}, {repr(self.tipo)}, {repr(self.valor)})"



    def serialize(self) -> str:
        return self.texto()

    def texto(self) -> str:
        return self._valor_alfanumerico



    @property
    def valor(self) -> Alfanumerico | Numerico:
        if self.tipo == Campo.ALFANUMERICO:
            return self.valor_c

        if self.tipo == Campo.NUMERICO:
            return self.valor_n

        raise ValueError(f"Tipo de campo desconhecido ({self.tipo})")

    @valor.setter
    def valor(self, valor: Alfanumerico | Numerico) -> None:
        if not (isinstance(valor, (str, int, float)) or valor is None):
            raise TypeError(f"O valor para o campo {repr(self)} deve ser str, int, float ou None")

        if self.tipo == Campo.ALFANUMERICO:
            self._valor_numerico = None
            self._valor_alfanumerico = str(valor)[:self.tamanho] if valor not in ("", None) else ""
        elif self.tipo == Campo.NUMERICO:
            try:
                if isinstance(valor, str):
                    valor = valor.replace(",", ".")

                # Arrendondado para a quantidade exata de casas decimais
                self._valor_numerico = None if valor in (None, "") else round(float(valor), self.decimal) if self.decimal else int(valor)

                # Convertendo o campo também para a versão alfanumérica
                self._valor_alfanumerico = Campo.alfanumerico(self._valor_numerico, self.decimal, self.tamanho, self.tamanho_exato)
            except (ValueError, OverflowError) as e:
                if self.decimal:
                    raise ValueError(f"Não foi possível converter valor para float ({valor})") from e

                raise ValueError(f"Não foi possível converter valor para inteiro ({valor})") from e
        else:
            raise ValueError(f"Tipo de campo desconhecido ({self.tipo})")



    @property
    def valor_c(self) -> Alfanumerico:
        return self._valor_alfanumerico

    @valor_c.setter
    def valor_c(self, valor: Alfanumerico | Numerico) -> None:
        self.valor = valor



    @property
    def valor_n(self) -> Numerico:
        if self._valor_numerico is None:
            return None

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n.setter
    def valor_n(self, valor: Alfanumerico | Numerico) -> None:
        self.valor = valor



    @property
    def valor_n0(self) -> Numerico0:
        if self._valor_numerico is None:
            return 0

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n0.setter
    def valor_n0(self, valor: Alfanumerico | Numerico) -> None:
        self.valor = valor
