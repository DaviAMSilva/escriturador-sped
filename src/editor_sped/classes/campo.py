from ..efd_info import EFD_INFO
from ..types import EfdTipo










Chave = str | int

Alfanumerico = str
Numerico = int | float | None
Numerico0 = int | float










class Campo:
    # Tipos de campo
    ALFANUMERICO = "C"
    NUMERICO = "N"



    @staticmethod
    def alfanumerico(valor: Alfanumerico | Numerico, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> Alfanumerico:
        if isinstance(valor, str):
            if len(valor) > tamanho:
                return valor[:tamanho]
            return valor

        if valor is None:
            return ""

        if decimal:
            resultado = f"{valor:.{decimal}f}"
            return resultado.replace(".", ",") if "." in resultado else resultado

        # Abaixo dessa linhas apenas números inteiros fazem sentido
        if not isinstance(valor, int):
            valor = int(valor)

        if tamanho_exato:
            return f"{valor:0{tamanho}d}"

        return str(valor)

    @staticmethod
    def numerico(valor: Alfanumerico | Numerico, decimal: int | None) -> Numerico:
        if valor in ("", None):
            return None

        if isinstance(valor, str):
            if decimal:
                return round(float(valor.replace(",", ".")), decimal)

            return int(valor.replace(",", "."))

        if decimal:
            return round(float(valor), decimal)

        return int(valor)



    def __init__(self, valor: Alfanumerico | Numerico, nome_registro: str, numero: int, efd_tipo: EfdTipo) -> None:
        info_campos = EFD_INFO[efd_tipo]["registros"][nome_registro]["campos"][numero - 1]

        # fmt: off
        self.nome          = info_campos["nome"]
        self.descricao     = info_campos["descricao"]
        self.decimal       = info_campos["decimal"]
        self.obrigatorio   = info_campos["obrigatorio"]
        self.tamanho       = info_campos["tamanho"]
        self.tamanho_exato = info_campos["tamanho_exato"]
        self.tipo          = info_campos["tipo"]
        # fmt: on

        self._valor_alfanumerico: Alfanumerico = ""
        self._valor_numerico: Numerico = None

        # Converte o valor passado para os valores interno corretos
        self.valor = valor



    def __str__(self) -> str:
        return self.texto()

    def __repr__(self) -> str:
        return f"Campo({repr(self.nome)}, {repr(self.tipo)}, {repr(self.valor)})"



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
        # Como o mais comum é valor ser str, testa-se somente str primeiro
        if valor is not None and not isinstance(valor, str):
            if not isinstance(valor, (int, float)):
                raise TypeError(f"O valor para o campo {repr(self)} deve ser str, int, float ou None")



        # A maioria dos campos é numérico, então testamos esse tipo primeiro
        if self.tipo == Campo.NUMERICO:
            # Os casos "" e "0" são tão comuns que merecem tratamento especial
            if valor == "":
                self._valor_numerico = None
                self._valor_alfanumerico = ""
                return

            if valor == "0":
                self._valor_numerico = 0
                self._valor_alfanumerico = "0"
                return

            # Todos os outros casos numéricos
            try:
                # Remover vírgulas apenas se presente
                if isinstance(valor, str) and "," in valor:
                    valor = valor.replace(",", ".")

                if valor is None:
                    novo_valor = None
                elif self.decimal:
                    novo_valor = round(float(valor), self.decimal)
                else:
                    novo_valor = int(valor)
            except (ValueError, OverflowError) as e:
                if self.decimal:
                    raise ValueError(f"Não foi possível converter valor para float ({valor})") from e
                raise ValueError(f"Não foi possível converter valor para int ({valor})") from e

            self._valor_numerico = novo_valor
            self._valor_alfanumerico = Campo.alfanumerico(novo_valor, self.decimal, self.tamanho, self.tamanho_exato)
            return



        if self.tipo == Campo.ALFANUMERICO:
            self._valor_numerico = None

            if valor == "" or valor is None:
                self._valor_alfanumerico = ""
                return

            self._valor_alfanumerico = valor[:self.tamanho] if isinstance(valor, str) else str(valor)[:self.tamanho]
            return



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
