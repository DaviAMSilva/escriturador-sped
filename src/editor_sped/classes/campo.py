from ..constantes import ALFANUMERICO, NUMERICO
from ..efd_info import EFD_INFO, EfdTipo










Chave = str | int

Alfanumerico = str
Numerico = int | float | None
Numerico0 = int | float










class Campo:
    # Tipos de campo
    ALFANUMERICO = ALFANUMERICO
    NUMERICO = NUMERICO



    @staticmethod
    def alfanumerico(valor: Alfanumerico | Numerico, decimal: int | None = None, tamanho: int = 255, tamanho_exato: bool = False) -> Alfanumerico:
        if isinstance(valor, str):
            if len(valor) > tamanho:
                return valor[:tamanho]
            return valor

        if valor is None:
            return ""

        if decimal:
            # Números decimais tem casas decimais extras removidas
            resultado = f"{valor:.{decimal}f}".rstrip("0").rstrip(".")
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



    def __init__(self, chave: Chave, valor: Alfanumerico | Numerico, nome_registro: str, efd_tipo: EfdTipo) -> None:
        info_campos = EFD_INFO[efd_tipo]["registros"][nome_registro.upper()]["campos"]

        # Descobrindo o info_campo correto
        if isinstance(chave, int):
            # Caso for o número, verificar que é maior que 0
            if chave <= 0:
                raise ValueError("Os campos de um registro têm a numeração iniciada pelo número 1")

            info_campo = info_campos[chave - 1]
        elif isinstance(chave, str):
            # Caso for o nome, encontrar o info_campo com esse nome
            for info_campo in info_campos:
                if info_campo["nome"] == chave:
                    break
            else:
                raise ValueError(f"Campo não encontrado pelo nome ({chave})")
        else:
            raise TypeError(f"Tipo inválido para parâmetro 'chave' ({chave})")

        # fmt: off
        self.nome          = info_campo["nome"]
        self.descricao     = info_campo["descricao"]
        self.decimal       = info_campo["decimal"]
        self.obrigatorio   = info_campo["obrigatorio"]
        self.tamanho       = info_campo["tamanho"]
        self.tamanho_exato = info_campo["tamanho_exato"]
        self.tipo          = info_campo["tipo"]
        # fmt: on

        self._valor_alfanumerico: Alfanumerico = ""
        self._valor_numerico: Numerico = None

        # Converte o valor passado para os valores interno corretos
        self.valor = valor



    def __str__(self) -> str:
        return self.texto()

    def __repr__(self) -> str:
        return f"Campo[{self.tipo!r}]({self.nome!r}: {self.valor!r})"



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
        if not isinstance(valor, str):
            if not isinstance(valor, (int, float)) and valor is not None:
                raise TypeError(f"O valor para um campo deve ser do tipo str, int, float ou None ({valor})")



        # A maioria dos campos é numérico, então testamos esse tipo primeiro
        if self.tipo == Campo.NUMERICO:
            # Convertermos o valor para numérico para normalizar o valor de comparação
            valor_numerico = Campo.numerico(valor, self.decimal)

            # 0 e "" são os dois valores mais abundantes, então é mais eficiente filtra-los
            if valor_numerico == 0 and not self.tamanho_exato:
                self._valor_numerico = 0
                self._valor_alfanumerico = "0"
                return

            if valor_numerico is None:
                self._valor_numerico = None
                self._valor_alfanumerico = ""
                return

            self._valor_numerico = valor_numerico
            self._valor_alfanumerico = Campo.alfanumerico(valor_numerico, self.decimal, self.tamanho, self.tamanho_exato)
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
