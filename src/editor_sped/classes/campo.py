from ..efd_info import EFD_INFO
from ..types import EfdTipo











class Campo:
    # Tipos de campo
    ALFANUMERICO = "C"
    NUMERICO = "N"



    @staticmethod
    def valor_para_texto(valor: str | int | float | None, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> str:
        if isinstance(valor, str):
            return str(valor)[:tamanho]

        if valor is None:
            return ""

        if tamanho_exato:
            tamanho_esquerda = tamanho - (decimal + 1 if decimal else 0)
            tamanho_direita = decimal if decimal else 0
            return f"{valor:0{tamanho_esquerda}.{tamanho_direita}f}".replace(".", ",") if decimal \
                else f"{int(valor):0{tamanho_esquerda}d}".replace(".", ",")

        return f"{valor:.{decimal or 0}f}".replace(".", ",") if decimal\
            else str(int(valor)).replace(".", ",")

    @staticmethod
    def texto_para_valor(valor: str, decimal: int | None) -> int | float | None:
        if valor in ("", None):
            return None

        if decimal:
            return float((valor or "").replace(",", "."))

        return int(float((valor or "").replace(",", ".")))



    def __init__(self, valor: str | int | float | None, nome_registro: str, numero: int, efd_tipo: EfdTipo) -> None:
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

        self._valor_alfanumerico: str = ""
        self._valor_numerico: int | float | None = None

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
    def valor(self) -> str | int | float:
        if self.tipo == Campo.ALFANUMERICO:
            return self.valor_c

        if self.tipo == Campo.NUMERICO:
            return self.valor_n

        raise ValueError(f"Tipo de campo desconhecido: {self.tipo}")

    @valor.setter
    def valor(self, valor: str | int | float | None) -> None:
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
                self._valor_alfanumerico = Campo.valor_para_texto(
                    float(self._valor_numerico) if self.decimal else int(self._valor_numerico),
                    self.decimal,
                    self.tamanho,
                    self.tamanho_exato
                ) if self._valor_numerico is not None else ""
            except (ValueError, OverflowError) as e:
                if self.decimal:
                    raise ValueError(f"Não foi possível converter valor para float ({valor})") from e

                raise ValueError(f"Não foi possível converter valor para inteiro ({valor})") from e
        else:
            raise ValueError(f"Tipo de campo desconhecido ({self.tipo})")

    @property
    def valor_c(self) -> str:
        return self._valor_alfanumerico

    @valor_c.setter
    def valor_c(self, valor: str | int | float | None) -> None:
        self.valor = valor


    @property
    def valor_n(self) -> int | float:
        if self._valor_numerico is None:
            # Infelizmente não é prático informar corretamente o tipo de retorno, pois ferramentas
            # como Pylance irão reclamar que o seguinte código, por exemplo, pode gerar erros:
            # campo.valor_n += 10 (None + 10 geraria erro)
            return None  # type: ignore

        if self.decimal:
            return float(self._valor_numerico)

        return int(self._valor_numerico)

    @valor_n.setter
    def valor_n(self, valor: str | int | float | None) -> None:
        self.valor = valor
