from typing import Any, Callable, Iterable, Never, overload

from ..constantes import EFD_ORDEM_BLOCOS
from ..efd_info import EFD_INFO
from ..types import EfdTipo
from .campo import Campo
from .campo_tupla import TuplaCampo
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Registro(ContemRegistros):
    @staticmethod
    def ordem(nome: str, efd_tipo: EfdTipo) -> int:
        # Exemplos:
        # 0100 ->    0 + 100 =  100
        # C500 -> 2000 + 500 = 2500
        return EFD_ORDEM_BLOCOS[efd_tipo].index(nome[0]) * 1000 + int(nome[1:4])

    @staticmethod
    def ler(registros: str, efd_tipo: EfdTipo) -> "Registro":
        from .registro_ler import ler_registros  # pylint: disable=import-outside-toplevel,cyclic-import
        try:
            return ler_registros(registros, efd_tipo)[0]
        except IndexError as e:
            raise ValueError("Não foi possível ler o registro") from e

    @staticmethod
    def ler_varios(registros: str | list[str], efd_tipo: EfdTipo) -> ListaRegistro:
        from .registro_ler import ler_registros  # pylint: disable=import-outside-toplevel,cyclic-import
        return ler_registros(registros, efd_tipo)



    def __init__(self, campos_texto: str, efd_tipo: EfdTipo) -> None:
        campos_textos = campos_texto.split("|")[1:-1]

        super().__init__(campos_textos[0], efd_tipo, ListaRegistro())

        campos_esperados = len(EFD_INFO[self.efd_tipo]["registros"][self.nome]["campos"])

        if len(campos_textos) != campos_esperados:
            raise SyntaxError(f"A quantidade de campos é diferente da quantidade esperada ({len(campos_textos)} ao invés de {campos_esperados})")

        # fmt: off
        self.descricao   = EFD_INFO[self.efd_tipo]["registros"][self.nome]["descricao"]
        self.nivel       = EFD_INFO[self.efd_tipo]["registros"][self.nome]["nivel"]
        self.obrigatorio = EFD_INFO[self.efd_tipo]["registros"][self.nome]["obrigatorio"]
        self.unico       = EFD_INFO[self.efd_tipo]["registros"][self.nome]["unico"]
        # fmt: on

        # self.pai é Registro ao invés de Registro | None por motivos de praticidade
        # O único caso em que pai é None é na abertura e fechamento da escrituração
        self.pai: Registro = None  # type: ignore
        self.campos = TuplaCampo(Campo(campo, i + 1, self, self.efd_tipo) for i, campo in enumerate(campos_textos))



    @overload
    def __getitem__(self, chave: int | str) -> Campo: ...

    @overload
    def __getitem__(self, chave: slice) -> TuplaCampo: ...

    def __getitem__(self, chave):
        if isinstance(chave, int):
            return self.campos[chave]

        return self.campos[chave]

    def __setitem__(self, chave: int | str, valor: str | int | float | None):
        self.campos[chave].valor = valor



    def __repr__(self) -> str:
        return f"Registro({repr(self.linha)})"

    def __contains__(self, chave: str | int | Campo):
        return chave in self.campos



    def serialize(self) -> dict:
        s = super().serialize()
        return {"nome": s["nome"], "campos": f"|{'|'.join([str(c) for c in self.campos])}|", "filhos": s["filhos"]}



    def texto(self) -> str:
        return \
            f"|{'|'.join([str(c) for c in self.campos])}|\n" + \
            f"{''.join([f.texto() for f in self.filhos])}"



    @property
    def linha(self) -> str:
        return f"|{'|'.join([str(c) for c in self.campos])}|"

    @property
    def tamanho(self) -> int:
        return super().tamanho + 1



    def teste(
        self,
        nome: str | None = None,
        campos: dict[str | int, str | int | float | None | Iterable[str | int | float | None]] | None = None,
        *,
        campos_c: dict[str | int, str | Iterable[str]] | None = None,
        campos_n: dict[str | int, int | float | None | Iterable[int | float | None]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None
    ) -> bool:
        if nome and nome != self.nome:
            return False

        if filtro and not filtro(self):
            return False

        if campos or campos_c or campos_n:
            campos_todos: list[tuple[dict[str | int, Any], str]] = [
                (campos or {}, ""),
                (campos_c or {}, Campo.ALFANUMERICO),
                (campos_n or {}, Campo.NUMERICO)
            ]

            for campos_atual, atributo in campos_todos:
                for campo_nome, campo_valor in campos_atual.items():
                    try:
                        campo = self[campo_nome]
                    except KeyError:
                        continue

                    if atributo == Campo.ALFANUMERICO:
                        valor_teste = campo.valor_c
                    elif atributo == Campo.NUMERICO:
                        valor_teste = campo.valor_n
                    else:
                        valor_teste = campo.valor

                    if isinstance(campo_valor, Iterable):
                        if valor_teste not in campo_valor:
                            return False
                    else:
                        if valor_teste != campo_valor:
                            return False

        return True



    def adicionar(self, registros: "Registro | ListaRegistro" | Iterable["Registro"]) -> ListaRegistro:
        registros_adicionados = ListaRegistro()

        for novo_registro in [registros] if isinstance(registros, Registro) else registros:
            if not isinstance(novo_registro, Registro):
                raise TypeError(f"Item não é um registro ({novo_registro})")

            if novo_registro.nome not in EFD_INFO[self.efd_tipo]["registros"][self.nome]["filhos"]:
                raise ValueError(f"O registro {novo_registro} não é um filho válido de {self}")

            for i, filho in enumerate(self.filhos):
                if Registro.ordem(novo_registro.nome, self.efd_tipo) < Registro.ordem(filho.nome, self.efd_tipo):
                    registros_adicionados.append(novo_registro)
                    self.filhos.insert(i, novo_registro)
                    break
            else:
                registros_adicionados.append(novo_registro)
                self.filhos.append(novo_registro)

        return registros_adicionados

    @overload
    def remover(
        self, registros: "Registro | ListaRegistro" | Iterable["Registro"], *,
        nome: Never = ..., filtro: Never = ..., campos: Never = ..., campos_c: Never = ..., campos_n: Never = ...
    ) -> ListaRegistro: ...

    @overload
    def remover(
        self, registros: None = None, *,
        nome: str | None = ...,
        filtro: Callable[["Registro"], bool] | None = ...,
        campos: dict[str | int, str | int | float | None] | None = ...,
        campos_c: dict[str | int, str] | None = ...,
        campos_n: dict[str | int, int | float | None] | None = ...
    ) -> ListaRegistro: ...

    def remover(self, registros=None, *, nome=None, filtro=None, campos=None, campos_c=None, campos_n=None) -> ListaRegistro:
        registros_removidos = ListaRegistro()

        if registros:
            if nome or filtro or campos or campos_c or campos_n:
                raise TypeError("Não são permitidos outros parâmetros se 'registros' estiver presente")

            registros_set = set([registros] if isinstance(registros, Registro) else registros)

            for i in range(len(self.filhos) - 1, -1, -1):
                if self.filhos[i] in registros_set:
                    registros_removidos.append(self.filhos[i])
                    del self.filhos[i]
        elif nome or filtro or campos or campos_c or campos_n:
            for i in range(len(self.filhos) - 1, -1, -1):
                if self.filhos[i].teste(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro):
                    registros_removidos.append(self.filhos[i])
                    del self.filhos[i]

        return registros_removidos
