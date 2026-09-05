from typing import Any, Callable, Iterable, Never, Self, cast, overload

from ..constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI, ORDEM_BLOCOS
from ..estruturas.lista_registro import ListaRegistro
from ..estruturas.tupla_campo import TuplaCampo
from ..modulos import MODULOS, MODULOS_NOMES, ModuloT
from ..tipos import CampoTipoT, Chave, Valor, ValorC, ValorN, ValorN0
from .campo import Campo
from .componente import Componente










class Registro(Componente):
    MODULO: ModuloT

    @classmethod
    def ordem(cls, nome: str, modulo: ModuloT) -> int:
        # Exemplos:
        # 0100 ->    0 + 100 =  100
        # C500 -> 2000 + 500 = 2500
        return ORDEM_BLOCOS[modulo].index(nome[0].upper()) * 1000 + int(nome[1:4])

    @classmethod
    def ler(cls, registros: str | Iterable[str], modulo: ModuloT | None = None) -> ListaRegistro:
        from ..leitura import ler_registros  # pylint: disable=import-outside-toplevel,cyclic-import

        if not modulo:
            modulo = cls.MODULO

        return ler_registros(registros, modulo)



    def __init__(self, modulo: ModuloT, campos: str | dict[Chave, Valor] | None = None, pai: "Registro | None" = None) -> None:
        if modulo not in MODULOS_NOMES:
            raise ValueError(f"Valor inválido para parâmetro 'modulo' ({modulo})")

        if campos is not None and not isinstance(campos, (str, dict)):
            raise TypeError(f"Tipo inválido para parâmetro 'campos' ({campos})")

        if pai is not None and not isinstance(pai, Registro):
            raise TypeError(f"Tipo inválido para parâmetro 'pai' ({pai})")

        campos = campos or {}

        # Lida com o caso de uma subclasse informar o nome diretamente
        if getattr(self, "nome", None):
            if isinstance(campos, dict):
                campos["REG"] = self.nome
            if isinstance(campos, str) and not campos.startswith(f"|{self.nome}"):
                raise ValueError(f"A linha fornecida ({campos!r}) se inicia com um campo diferente do esperado ({self.nome!r})")



        info_registros = MODULOS[modulo]["registros"]

        # Caso TEXTO
        # Exemplo: '|NOME|VALOR|'
        if isinstance(campos, str):
            textos_campos = campos.split("|")[1:-1]
            nome_registro = textos_campos[0].upper()
            info_registro = info_registros[nome_registro]

            super().__init__(modulo, nome_registro, ListaRegistro["Registro"]())

            info_campos = info_registro["campos"]

            campos_encontrados = len(textos_campos)

            campos_exatos = MODULOS[modulo]["registros"][nome_registro]["campos_exatos"]
            campos_faixa = MODULOS[modulo]["registros"][nome_registro]["campos_faixa"]

            # Testando se a quantidade de campos encontrados é válida
            if campos_exatos:
                # Registro precisa ter uma de várias quantidades possíveis de campos
                if campos_encontrados not in campos_exatos:
                    raise SyntaxError(
                        f"A quantidade de campos ({campos_encontrados}) não está presente na lista de "
                        f"quantidades esperadas ({campos_exatos!r}) no registro '{self.nome}'"
                    )
            elif campos_faixa:
                # Registro precisa ter uma quantidade de campos entre dois limites (inclusive)
                if not campos_faixa[0] <= campos_encontrados <= campos_faixa[1]:
                    raise SyntaxError(
                        f"A quantidade de campos ({campos_encontrados}) não está dentro da faixa de "
                        f"quantidades esperadas ({tuple(campos_faixa)!r}) no registro '{self.nome}'"
                    )
            else:
                # Registro precisa ter uma quantidade exata de campos
                campos_esperados = len(info_campos)
                if campos_encontrados != campos_esperados:
                    raise SyntaxError(
                        "A quantidade de campos é diferente da esperada "
                        f"({campos_encontrados} ao invés de {campos_esperados} no registro {self.nome})."
                        f"{' É provável que o tipo da escrituração esteja incorreto' if self.nome == '0000' else ''}"
                    )

            self.campos = TuplaCampo(
                Campo(modulo, nome_registro, i, valor)
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

            super().__init__(modulo, nome_registro, ListaRegistro["Registro"]())

            self.campos = TuplaCampo(
                Campo(
                    modulo,
                    nome_registro,
                    info_campo["numero"],
                    campos.get(info_campo["nome"], campos.get(info_campo["numero"]))
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
        self.pai: Registro = pai  # type: ignore
        if pai:
            pai.adicionar(self)


    def __getattr__(self, nome: str) -> Campo[CampoTipoT, Valor]:
        nome_hifen = nome.replace("__", "-")
        nome_barra = nome.replace("__", "/")

        if nome_hifen in self.__getattribute__("campos"):
            return self.__getattribute__("campos")[nome_hifen]
        if nome_barra in self.__getattribute__("campos"):
            return self.__getattribute__("campos")[nome_barra]

        raise AttributeError(f"O campo com nome {nome!r} não existe em {self!r}")



    def __str__(self) -> str:
        return self.linha

    def __repr__(self) -> str:
        return f"Registro({self.linha!r})"



    def como[ComoRegistroT: Registro](self, registro: type[ComoRegistroT]) -> ComoRegistroT:  # pylint: disable=unused-argument
        return cast(ComoRegistroT, self)



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



    def valores(self, valores: dict[Chave, Valor] | None = None) -> dict[str, Valor]:
        return self.campos.valores(valores)

    def valores_c(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorC]:
        return self.campos.valores_c(valores)

    def valores_n(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN]:
        return self.campos.valores_n(valores)

    def valores_n0(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN0]:
        return self.campos.valores_n0(valores)



    def teste(
        self,
        nome: str | None = None,
        campos: dict[Chave, Valor | Iterable[Valor]] | None = None,
        *,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = None,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = None,
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
                        campo = self.campos[nome_campo]
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



    def adicionar(self, registros: "Registro | ListaRegistro[Registro] | Iterable[Registro]") -> Self:
        for novo_registro in [registros] if isinstance(registros, Registro) else registros:
            if not isinstance(novo_registro, Registro):
                raise TypeError(f"Item não é um registro ({novo_registro!r})")

            if novo_registro.nome not in MODULOS[self.modulo]["registros"][self.nome]["filhos"]:
                raise ValueError(f"O registro {novo_registro!r} não é um filho válido de {self!r}")

            if novo_registro.pai is not None:
                novo_registro.pai.remover(novo_registro)

            for i, filho in enumerate(self.filhos):
                if Registro.ordem(novo_registro.nome, self.modulo) < Registro.ordem(filho.nome, self.modulo):
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
        registros: "Registro | ListaRegistro[Registro] | Iterable[Registro]",
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
        campos: dict[Chave, Valor | Iterable[Valor]] | None = ...,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = ...,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = ...
    ) -> Self: ...

    def remover(
        self,
        registros: "Registro | ListaRegistro[Registro] | Iterable[Registro] | None" = None,
        *,
        nome: str | None = None,
        filtro: Callable[["Registro"], bool] | None = None,
        campos: dict[Chave, Valor | Iterable[Valor]] | None = None,
        campos_c: dict[Chave, ValorC | Iterable[ValorC]] | None = None,
        campos_n: dict[Chave, ValorN | Iterable[ValorN]] | None = None
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










class RegistroEcd(Registro):
    def __init__(self, campos: str | dict[Chave, Valor] | None = None, pai: Registro | None = None) -> None:
        super().__init__(ECD, campos, pai)


class RegistroEcf(Registro):
    def __init__(self, campos: str | dict[Chave, Valor] | None = None, pai: Registro | None = None) -> None:
        super().__init__(ECF, campos, pai)


class RegistroEfdIcmsIpi(Registro):
    def __init__(self, campos: str | dict[Chave, Valor] | None = None, pai: Registro | None = None) -> None:
        super().__init__(EFD_ICMS_IPI, campos, pai)


class RegistroEfdContribuicoes(Registro):
    def __init__(self, campos: str | dict[Chave, Valor] | None = None, pai: Registro | None = None) -> None:
        super().__init__(EFD_CONTRIBUICOES, campos, pai)
