"""Contém a classe abstratas `Registro` e suas subclasses."""
from typing import Any, Callable, Iterable, Never, Self, cast, overload

from ..constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI, ORDEM_BLOCOS
from ..estruturas.lista_registro import ListaRegistro
from ..estruturas.tupla_campo import TuplaCampo
from ..modulos import MODULOS, MODULOS_NOMES, ModuloT
from ..tipos import CampoTipoT, Chave, Valor, ValorC, ValorN, ValorN0
from .campo import Campo
from .componente import Componente










class Registro(Componente):
    """Contém informações sobre um registro e seus campos.

    Na criação de um registro os campos podem ser informados nos seguintes modos:

    - **Texto**: Da mesma forma como a linha de uma escrituração.  
    *Todos os campos são obrigatório.*
    - **Dicionário**: Um dicionários contendo as chaves dos campos e seus valores.  
    *Campos ausentes são interpretados como vazios.*

    Se for informado o registro pai, o novo registro será automaticamente adicionado na lista de filhos do registro pai.
    Se forem informados registros filhos, eles serão automaticamente adicionados na lista de filhos do novo registro.

    Attributes:
        nome (str): Nome do registro.
        campos (TuplaCampo): Campos do registro.
        filhos (ListaRegistro): Filhos diretos do registro.
        pai (Registro | None): Pai do Registro.
        modulo (ModuloT): Módulo ao qual o bloco pertence.
        descricao (str): Descrição do registro.
        nivel (int): Nível do registro na escrituração.
        obrigatorio (bool): Se o registro é obrigatório aparecer na escrituração.
        unico (bool): Se o registro deve aparecer apenas uma vez na escrituração.

    Args:
        modulo: Módulo ao qual o bloco pertence.
        campos: Lista dos valores iniciais dos campos do registro.
        pai: Registro pai do registro a ser criado.
        filhos: Registros filhos para o registro a ser criado.

    Raises:
        ValueError: Se o valor do parâmetro modulo for inválido.
        TypeError: Se o parâmetro `campos` for do tipo inválido.
        TypeError: Se o parâmetro `pai` for do tipo inválido.
        TypeError: Se o parâmetro `filhos` for do tipo inválido.
        ValueError: Se os campos são do tipo texto e o primeiro campo for diferente do esperado pela subclasse.
        SyntaxError: Se a quantidade de campos for diferente da esperada no modo de texto.
        ValueError: Se não houver pelo menos um campo com nome REG ou número 1 no modo de dicionário.
        TypeError: Se os campos não forem do tipo texto ou dicionário.

    Examples:
        >>> novo_registro = Registro(Escrituracao.EFD_ICMS_IPI, '|NOME|10|')
        Registro('|NOME|10|')
        >>> novo_registro.pai
        None

        >>> novo_registro = Registro(Escrituracao.EFD_ICMS_IPI, {'REG': 'NOME', 2: 20}, pai=registro_pai)
        Registro('|NOME|20|')
        >>> novo_registro.pai.filhos
        ListaRegistro[Registro('|NOME|20|')]
    """
    MODULO: ModuloT



    @classmethod
    def ordem(cls, nome: str, modulo: ModuloT) -> int:
        """Calcula o número de ordem de um registro.

        Usado para realizar comparações de ordem entre registros.

        Args:
            nome: Nome do registro.
            modulo: Módulo ao qual o registro pertence.

        Returns:
            Valor numérico da ordem do registro.

        Examples:
            >>> Registro.ordem('0100', Escrituracao.EFD_ICMS_IPI)
            100

            >>> Registro.ordem('C500', Escrituracao.EFD_ICMS_IPI)
            2500
        """
        return ORDEM_BLOCOS[modulo].index(nome[0].upper()) * 1000 + int(nome[1:4])

    @classmethod
    def ler(cls, registros: str | Iterable[str], modulo: ModuloT | None = None) -> ListaRegistro:
        """Converte várias linhas para uma lista de registros.

        Args:
            registros: Uma lista de registros em forma de texto. Pode ser um texto separados por quebras de linhas ou um iterável de textos individuais.
            modulo: Módulo ao qual o registro pertence.

        Returns:
            Lista dos registros convertidos.
        """
        from ..leitura import ler_registros  # pylint: disable=import-outside-toplevel,cyclic-import

        if not modulo:
            modulo = cls.MODULO

        return ler_registros(registros, modulo)



    def __init__(self, modulo: ModuloT, campos: str | dict[Chave, Valor] | None = None, *, pai: "Registro | None" = None, filhos: "list[Registro] | ListaRegistro | Iterable[Registro] | None" = None) -> None:
        if modulo not in MODULOS_NOMES:
            raise ValueError(f"Valor inválido para parâmetro 'modulo' ({modulo})")

        if campos is not None and not isinstance(campos, (str, dict)):
            raise TypeError(f"Tipo inválido para parâmetro 'campos' ({campos})")

        if pai is not None and not isinstance(pai, Registro):
            raise TypeError(f"Tipo inválido para parâmetro 'pai' ({pai})")

        if filhos is not None and not isinstance(filhos, Iterable):
            raise TypeError(f"Tipo inválido para parâmetro 'filhos' ({filhos})")

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

        # Adicionando filhos
        if filhos:
            self.adicionar(filhos)



    def __getattr__(self, nome: str) -> Campo[CampoTipoT, Valor]:
        """Retorna o campo com o nome especificado pelo atributo.

        Args:
            nome: Nome de campo a ser retornado.

        Raises:
            AttributeError: Se o campo com esse nome não existir.

        Returns:
            Campo: O campo a ser retornado.
        """
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
        """Corrige a tipo do registro para o tipo especificado.

        Returns:
            O próprio registro, mas com o tipo corrigido.
        """
        return cast(ComoRegistroT, self)



    def texto(self) -> str:
        return (
            f"|{'|'.join([str(c) for c in self.campos])}|\n"
            f"{''.join([f.texto() for f in self.filhos])}"
        )



    @property
    def linha(self) -> str:
        """A representação do registro como uma linha de uma escrituração."""
        return f"|{'|'.join([str(c) for c in self.campos])}|"

    @property
    def tamanho(self) -> int:
        return super().tamanho + 1



    def valores(self, valores: dict[Chave, Valor] | None = None) -> dict[str, Valor]:
        """Permite visualizar ou alterar os valores dos campos do registro.

        Diferentes variações dessa função podem retornar especificamente os valores alfanumérico, numéricos ou numéricos, não nulos:

        - `Registro.valores() -> dict[str, Valor]`
        - `Registro.valores_c() -> dict[str, ValorC]`
        - `Registro.valores_n() -> dict[str, ValorN]`
        - `Registro.valores_n0() -> dict[str, ValorN0]`

        Args:
            valores: Dicionário de valores a serem alterados do registro.

        Raises:
            TypeError: Se os valores não são de um tipo válido.

        Returns:
            Valores dos campos do registro, após a alteração se essa tiver ocorrida.

        Examples:
            >>> registro.valores()
            {'NOME': 'UM', 'VALOR': 1}

            >>> registro.valores({NOME: 'DOIS', 2: 2})
            {'NOME': 'DOIS', 'VALOR': 2}
        """
        return self.campos.valores(valores)

    def valores_c(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorC]:
        """Consultar `Registro.valores()`."""
        return self.campos.valores_c(valores)

    def valores_n(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN]:
        """Consultar `Registro.valores()`."""
        return self.campos.valores_n(valores)

    def valores_n0(self, valores: dict[Chave, Valor] | None = None) -> dict[str, ValorN0]:
        """Consultar `Registro.valores()`."""
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
        """Testa se o registro é válido, de acordo com os parâmetros informados.

        Args:
            nome: Nome do registro válido.
            campos: Dicionários com chaves e um ou mais valores dos campos no registro válido.
            campos_c: Dicionários com chaves e um ou mais valores alfanuméricos dos campos no registro válido.
            campos_n: Dicionários com chaves e um ou mais valores numéricos dos campos no registro válido.
            filtro: Função que recebe um `Registro` e retorna `True` para o registro válido.

        Returns:
            Se o registro passa o teste.
        """
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
        """Adiciona registros filhos em um registro.

        Args:
            registros: Lista de registros filhos a serem adicionados ao registro pai.

        Raises:
            TypeError: Se um dos itens não for um registro.
            ValueError: Se um dos registros filhos não for um filho válido do registro pai.

        Returns:
            O próprio registro.
        """
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
        """Remove registros filhos de um registro, de acordo com os parâmetros informados.

        Args:
            registros: Lista de registros a serem removidos. Se esse parâmetro for informado não é permitido informar nenhum outro parâmetro.
            nome: Nome dos registros a serem removidos.
            filtro: Função que recebe um `Registro` e retorna `True` para os registros a serem removidos.
            campos: Dicionários com chaves e um ou mais valores dos campos nos registros a serem removidos.
            campos_c: Dicionários com chaves e um ou mais valores alfanuméricos dos campos nos registros a serem removidos.
            campos_n: Dicionários com chaves e um ou mais valores numéricos dos campos nos registros a serem removidos.

        Raises:
            TypeError: Se o parâmetros `registros` for usado, mas outro parâmetro estiver presente.

        Returns:
            O próprio registro.
        """
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
        """Limpa os filhos do registro.

        Returns:
            Próprio registro.
        """
        self.filhos.clear()

        return self










class RegistroEcd(Registro):
    """Contém informações sobre um registro do módulo ECD e seus campos"""

    def __init__(self, campos: str | dict[Chave, Valor] | None = None, *, pai: Registro | None = None, filhos: list[Registro] | ListaRegistro | Iterable[Registro] | None = None) -> None:
        super().__init__(ECD, campos, pai=pai, filhos=filhos)


class RegistroEcf(Registro):
    """Contém informações sobre um registro do módulo ECF e seus campos"""

    def __init__(self, campos: str | dict[Chave, Valor] | None = None, *, pai: Registro | None = None, filhos: list[Registro] | ListaRegistro | Iterable[Registro] | None = None) -> None:
        super().__init__(ECF, campos, pai=pai, filhos=filhos)


class RegistroEfdIcmsIpi(Registro):
    """Contém informações sobre um registro do módulo EFD_ICMS_IPI e seus campos"""

    def __init__(self, campos: str | dict[Chave, Valor] | None = None, *, pai: Registro | None = None, filhos: list[Registro] | ListaRegistro | Iterable[Registro] | None = None) -> None:
        super().__init__(EFD_ICMS_IPI, campos, pai=pai, filhos=filhos)


class RegistroEfdContribuicoes(Registro):
    """Contém informações sobre um registro do módulo EFD_CONTRIBUICOES e seus campos"""

    def __init__(self, campos: str | dict[Chave, Valor] | None = None, *, pai: Registro | None = None, filhos: list[Registro] | ListaRegistro | Iterable[Registro] | None = None) -> None:
        super().__init__(EFD_CONTRIBUICOES, campos, pai=pai, filhos=filhos)
