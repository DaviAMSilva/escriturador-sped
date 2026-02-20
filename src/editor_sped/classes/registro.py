from typing import Any, Callable, Iterable, Never, Self, overload

from ..constantes import EFD_ORDEM_BLOCOS
from ..efd_info import EFD_INFO, EfdTipo
from .campo import Alfanumerico, Campo, Chave, Numerico, Numerico0
from .campo_tupla import TuplaCampo
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Registro(ContemRegistros):
    @staticmethod
    def ordem(nome: str, efd_tipo: EfdTipo) -> int:
        # Exemplos:
        # 0100 ->    0 + 100 =  100
        # C500 -> 2000 + 500 = 2500
        return EFD_ORDEM_BLOCOS[efd_tipo].index(nome[0].upper()) * 1000 + int(nome[1:4])

    @staticmethod
    def ler(registros: str | Iterable[str], efd_tipo: EfdTipo) -> ListaRegistro:
        from ..ler_registros import ler_registros  # pylint: disable=import-outside-toplevel,cyclic-import
        return ler_registros(registros, efd_tipo)



    def __init__(self, campos: str | dict[Chave, Alfanumerico | Numerico], efd_tipo: EfdTipo, *, pai: "Registro | None" = None) -> None:
        if pai is not None and not isinstance(pai, Registro):
            raise TypeError(f"Tipo inválido para parâmetro 'pai' ({pai})")



        info_registros = EFD_INFO[efd_tipo]["registros"]

        # Caso TEXTO
        # Exemplo: '|NOME|VALOR|'
        if isinstance(campos, str):
            textos_campos = campos.split("|")[1:-1]
            nome_registro = textos_campos[0].upper()
            info_registro = info_registros[nome_registro]

            super().__init__(nome_registro, ListaRegistro(), efd_tipo)

            info_campos = info_registro["campos"]
            esperado = len(info_campos)
            recebido = len(textos_campos)

            if recebido != esperado:
                raise SyntaxError(
                    "A quantidade de campos é diferente da esperada "
                    f"({recebido} ao invés de {esperado} no registro {self.nome})"
                    ". É provável que o tipo da escrituração esteja incorreto" if self.nome == "0000" else ""
                )

            self.campos = TuplaCampo(
                Campo(i, valor, nome_registro, efd_tipo)
                for i, valor in enumerate(textos_campos, 1)
            )



        # Caso DICIONÁRIO
        # Exemplo: {'REG': 'NOME', 2: 'VALOR'}
        elif isinstance(campos, dict):
            nome_registro = None

            reg = campos.get("REG")  # REG é um campo obrigatório
            if reg in info_registros and isinstance(reg, str):
                nome_registro = reg.upper()
            else:
                reg = campos.get(1)  # 1 (REG) é um campo obrigatório
                if reg in info_registros and isinstance(reg, str):
                    nome_registro = reg.upper()

            if not nome_registro:
                raise ValueError("Pelo menos um nome de registro válido com chave 'REG' ou 1 deve existir")

            info_registro = info_registros[nome_registro]

            super().__init__(nome_registro, ListaRegistro(), efd_tipo)

            self.campos = TuplaCampo(
                Campo(
                    info_campo["numero"],
                    campos.get(info_campo["nome"], campos.get(info_campo["numero"])),
                    nome_registro,
                    efd_tipo
                )
                for info_campo in info_registro["campos"]
            )
        else:
            raise TypeError(f"Tipo inválido para parâmetro 'campos' ({campos})")



        # fmt: off
        self.descricao   = info_registro["descricao"]
        self.nivel       = info_registro["nivel"]
        self.obrigatorio = info_registro["obrigatorio"]
        self.unico       = info_registro["unico"]
        # fmt: on



        # Configurando a associação pai/filho
        self.pai = pai
        if pai:
            pai.adicionar(self)



    @overload
    def __getitem__(self, chave: Chave) -> Campo: ...

    @overload
    def __getitem__(self, chave: slice) -> TuplaCampo: ...

    def __getitem__(self, chave: Chave | slice):
        return self.campos[chave]

    def __setitem__(self, chave: Chave, valor: Alfanumerico | Numerico):
        self.campos[chave].valor = valor

    def __contains__(self, chave: Chave | Campo):
        return chave in self.campos



    def __str__(self) -> str:
        return self.linha

    def __repr__(self) -> str:
        return f"Registro({self.linha!r})"



    def texto(self) -> str:
        return (
            f"|{'|'.join([str(c) for c in self.campos])}|\n"
            f"{''.join([f.texto() for f in self.filhos])}"
        )



    @property
    def linha(self) -> str:
        return f"|{'|'.join([str(c) for c in self.campos])}|"

    @property
    def tamanho(self) -> int:
        return super().tamanho + 1



    def valores(self, valores: dict[Chave, Alfanumerico | Numerico] | None = None) -> dict[str, Alfanumerico | Numerico]:
        return self.campos.valores(valores)

    def valores_c(self, valores: dict[Chave, Alfanumerico | Numerico] | None = None) -> dict[str, Alfanumerico]:
        return self.campos.valores_c(valores)

    def valores_n(self, valores: dict[Chave, Alfanumerico | Numerico] | None = None) -> dict[str, Numerico]:
        return self.campos.valores_n(valores)

    def valores_n0(self, valores: dict[Chave, Alfanumerico | Numerico] | None = None) -> dict[str, Numerico0]:
        return self.campos.valores_n0(valores)



    def teste(
        self,
        nome: str | None = None,
        campos: dict[Chave, Alfanumerico | Numerico | Iterable[Alfanumerico | Numerico]] | None = None,
        *,
        campos_c: dict[Chave, Alfanumerico | Iterable[Alfanumerico]] | None = None,
        campos_n: dict[Chave, Numerico | Iterable[Numerico]] | None = None,
        filtro: Callable[["Registro"], bool] | None = None
    ) -> bool:
        if nome is not None and nome != self.nome:
            return False

        if filtro is not None and not filtro(self):
            return False

        if campos is not None or campos_c is not None or campos_n is not None:
            campos_todos: list[tuple[dict[Chave, Any], str]] = [
                (campos or {}, ""),
                (campos_c or {}, Campo.ALFANUMERICO),
                (campos_n or {}, Campo.NUMERICO)
            ]

            for campos_atual, atributo in campos_todos:
                for nome_campo, valor_campo in campos_atual.items():
                    try:
                        campo = self[nome_campo]
                    except KeyError:
                        continue

                    if atributo == Campo.ALFANUMERICO:
                        valor_teste = campo.valor_c
                    elif atributo == Campo.NUMERICO:
                        valor_teste = campo.valor_n
                    else:
                        valor_teste = campo.valor

                    if isinstance(valor_campo, Iterable) and not isinstance(valor_campo, str):
                        if valor_teste not in valor_campo:
                            return False
                    else:
                        if valor_teste != valor_campo:
                            return False

        return True



    def adicionar(self, registros: "Registro | ListaRegistro | Iterable[Registro]") -> Self:
        for novo_registro in [registros] if isinstance(registros, Registro) else registros:
            if not isinstance(novo_registro, Registro):
                raise TypeError(f"Item não é um registro ({novo_registro!r})")

            if novo_registro.nome not in EFD_INFO[self.efd_tipo]["registros"][self.nome]["filhos"]:
                raise ValueError(f"O registro {novo_registro!r} não é um filho válido de {self!r}")

            if novo_registro.pai is not None:
                novo_registro.pai.remover(novo_registro)

            for i, filho in enumerate(self.filhos):
                if Registro.ordem(novo_registro.nome, self.efd_tipo) < Registro.ordem(filho.nome, self.efd_tipo):
                    novo_registro.pai = self
                    self.filhos.insert(i, novo_registro)
                    break
            else:
                novo_registro.pai = self
                self.filhos.append(novo_registro)

        return self

    @overload
    def remover(
        self,
        registros: "Registro | ListaRegistro | Iterable[Registro]",
        *,
        nome: Never = ...,
        filtro: Never = ...,
        campos: Never = ...,
        campos_c: Never = ...,
        campos_n: Never = ...
    ) -> Self: ...

    @overload
    def remover(
        self, registros: None = None,
        *,
        nome: str | None = ...,
        filtro: Callable[["Registro"], bool] | None = ...,
        campos: dict[Chave, Alfanumerico | Numerico | Iterable[Alfanumerico | Numerico]] | None = ...,
        campos_c: dict[Chave, Alfanumerico | Iterable[Alfanumerico]] | None = ...,
        campos_n: dict[Chave, Numerico | Iterable[Numerico]] | None = ...
    ) -> Self: ...

    def remover(
        self,
        registros: "Registro | ListaRegistro | Iterable[Registro] | None" = None,
        *,
        nome: str | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        campos: dict[Chave, Alfanumerico | Numerico | Iterable[Alfanumerico | Numerico]] | None = None,
        campos_c: dict[Chave, Alfanumerico | Iterable[Alfanumerico]] | None = None,
        campos_n: dict[Chave, Numerico | Iterable[Numerico]] | None = None
    ) -> Self:
        if registros:
            if nome or filtro or campos or campos_c or campos_n:
                raise TypeError("Não são permitidos outros parâmetros se 'registros' estiver presente")

            registros_set = set([registros] if isinstance(registros, Registro) else registros)

            for i in range(len(self.filhos) - 1, -1, -1):
                if self.filhos[i] in registros_set:
                    self.filhos[i].pai = None  # type: ignore
                    del self.filhos[i]
        elif nome or filtro or campos or campos_c or campos_n:
            if nome:
                nome = nome.upper()

            for i in range(len(self.filhos) - 1, -1, -1):
                if self.filhos[i].teste(nome, campos, campos_c=campos_c, campos_n=campos_n, filtro=filtro):
                    self.filhos[i].pai = None  # type: ignore
                    del self.filhos[i]

        return self

    def limpar(self) -> Self:
        self.filhos.clear()

        return self
