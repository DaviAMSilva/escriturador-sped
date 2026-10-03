"""Contém a classe `Escrituracao` e suas subclasses."""
from abc import ABC
from collections import Counter
from pathlib import Path
from typing import Self

from ..arquivos import abrir_escrituracao, remover_assinatura_escrituracao, salvar_escrituracao
from ..constantes import ECD, ECF, EFD_CONTRIBUICOES, EFD_ICMS_IPI, ORDEM_BLOCOS
from ..estruturas.lista_registro import ListaRegistro
from ..modulos import MODULOS, MODULOS_NOMES, ModuloT
from .bloco import Bloco
from .componente import Componente
from .registro import Registro


class Escrituracao(Componente, ABC):
    """Classe abstrata para contém informações de uma escrituração, seus blocos e registros.

    Attributes:
        blocos (dict[str, Bloco]): Dicionário de blocos da escrituração.
        abertura (Registro): Registro de abertura da escrituração.
        fechamento (Registro): Registro de fechamento da escrituração.
        modulo: Módulo ao qual a escrituração pertence.

    Args:
        escrituracao_texto: Texto da escrituração a ser criada.
        nome: Nome da escrituração.
    """

    MODULO: ModuloT
    """Nome do módulo a que essa escrituração pertence."""

    ECD = ECD
    "Nome para uma escrituração do tipo Escrituração Contábil Digital."
    ECF = ECF
    "Nome para uma escrituração do tipo Escrituração Contábil Fiscal."
    EFD_ICMS_IPI = EFD_ICMS_IPI
    "Nome para uma escrituração do tipo Escrituração Fiscal Digital Contribuições."
    EFD_CONTRIBUICOES = EFD_CONTRIBUICOES
    "Nome para uma escrituração do tipo Escrituração Fiscal Digital ICMS IPI."

    MODULOS_NOMES = MODULOS_NOMES
    """Lista dos nomes dos módulos disponíveis na biblioteca."""



    @classmethod
    def abrir(cls, arquivo: str | Path) -> Self:
        """Fábrica para criar uma escrituração diretamente de um arquivo.

        Args:
            arquivo: Caminho do arquivo a ser aberto.

        Returns:
            Instância da escrituração criada.
        """
        # Isso é estranho, mas funciona pois as subclasses usam apenas um parâmetro
        return cls(abrir_escrituracao(arquivo))  # pyright: ignore[reportCallIssue] # pylint: disable=no-value-for-parameter

    def salvar(self, arquivo: str | Path) -> Self:
        """Salva a escrituração para um arquivo.

        Args:
            arquivo: Caminho do arquivo a ser salvo.

        Returns:
            A própria escrituração.
        """
        salvar_escrituracao(arquivo, self.texto())

        return self


    def __init__(self, modulo: ModuloT, escrituracao_texto: str, nome: str) -> None:
        super().__init__(modulo, nome.upper(), ListaRegistro[Registro]())

        self.blocos: dict[str, Bloco] = {}

        self.abertura: Registro
        self.fechamento: Registro

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self._ler_escrituracao(escrituracao_texto)

        self.totalizar()



    def __getitem__(self, chave: str) -> Bloco:
        """Encontra o bloco desejado da escrituração.

        Args:
            chave: Nome do bloco.

        Raises:
            KeyError: Se o bloco não existe.

        Returns:
            Bloco desejado.
        """
        try:
            return self.blocos[chave]
        except KeyError as e:
            raise KeyError(f"Bloco não encontrado ({chave})") from e

    def __contains__(self, chave: str) -> bool:
        """Testa se um bloco existe na escrituração.

        Args:
            chave: Nome ou número do bloco a ser testado.

        Returns:
            Se o bloco existe na escrituração.
        """
        return chave in self.blocos



    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.tamanho} linhas"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tamanho={self.tamanho!r})"



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    def _ler_escrituracao(self, escrituracao_texto: str) -> None:
        registros_raizes = Registro.ler(escrituracao_texto, self.modulo)



        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise SyntaxError(f"Escrituração mal formatada ({registros_raizes})")



        # Informação da escrituração em si
        self.filhos = registros_raizes
        [self.abertura, self.fechamento] = registros_raizes



        # Preenchendo as informações dos blocos
        for info_bloco in MODULOS[self.modulo]["blocos"]:
            registro_bloco_abertura: Registro | None = None
            registro_bloco_fechamento: Registro | None = None



            # Encontrando os registros de abertura e fechamento na lista de registros
            # Esse método encontra apenas os blocos presentes na escrituração atual,
            # não levando em consideração as condições de obrigatoriedade de blocos
            for registros in self.abertura.filhos:
                if registros.nome == info_bloco["abertura"]:
                    registro_bloco_abertura = registros
                    break

            for registros in self.abertura.filhos:
                if registros.nome == info_bloco["fechamento"]:
                    registro_bloco_fechamento = registros
                    break

            if registro_bloco_abertura and registro_bloco_fechamento:
                # Criando o bloco com os blocos de abertura e fechamento
                self.blocos[info_bloco["nome"]] = Bloco(info_bloco["nome"], registro_bloco_abertura, registro_bloco_fechamento, self.modulo)
            elif registro_bloco_abertura is not None or registro_bloco_fechamento is not None:
                # Apenas um dos registros de abertura ou fechamento existe
                raise TypeError(
                    f"Apenas um dos registros de abertura |{registro_bloco_abertura.nome if registro_bloco_abertura else None}|"
                    f" ou fechamento |{registro_bloco_fechamento.nome if registro_bloco_fechamento else None}| existe"
                )



    def adicionar(self, nome_bloco: str) -> Self:
        """Adiciona um bloco a escrituração.

        Args:
            nome_bloco: Nome do bloco a ser adicionado.

        Returns:
            Própria escrituração.
        """
        nome_bloco = nome_bloco.upper()

        if nome_bloco not in self.blocos and nome_bloco in ORDEM_BLOCOS[self.modulo]:
            self.blocos[nome_bloco] = Bloco(
                nome_bloco,
                Registro(self.modulo, f"|{nome_bloco}001|1|", pai=self.abertura),
                Registro(self.modulo, f"|{nome_bloco}990|2|", pai=self.abertura),
                self.modulo
            )

        return self



    def remover(self, nome_bloco: str) -> Self:
        """Remove um bloco a escrituração.

        Args:
            nome_bloco: Nome do bloco a ser removido.

        Returns:
            Própria escrituração.
        """
        nome_bloco = nome_bloco.upper()

        if nome_bloco in self.blocos:
            self.abertura.remover(self.blocos[nome_bloco].filhos)
            del self.blocos[nome_bloco]

        return self



    def totalizar(self, ordenar_9900: bool = False) -> Self:
        """Totaliza os valores de contagem do bloco 9 e os fechamentos da escrituração.

        Args:
            ordenar_9900: Se os registros 9900 devem ser ordenados de acordo com os registros que eles totalizam.
        """
        # A totalização dos registros e dos blocos dependem um do outro
        # por isso, é necessário realizar a totalização dessa forma
        self.totalizar_blocos()
        self.totalizar_registros(ordenar_9900)
        self.totalizar_blocos()
        self.totalizar_escrituracao()

        return self

    def totalizar_escrituracao(self) -> Self:
        """Totaliza o fechamento da escrituração."""
        self.fechamento.campos[2].valor_c = self.tamanho

        return self

    def totalizar_blocos(self) -> Self:
        """Totaliza os fechamentos dos blocos da escrituração."""
        for nome in ORDEM_BLOCOS[self.modulo]:
            bloco = self.blocos.get(nome, None)

            if bloco:
                # Se o bloco estiver vazio o valor da abertura é definido como 1
                bloco.abertura.campos[2].valor_c = 0 if bloco.tamanho > 2 else 1
                bloco.fechamento.campos[2].valor_c = bloco.tamanho
            else:
                # Criando um novo bloco vazio se não existir
                self.adicionar(nome)

        # Ordenar os blocos é obrigatório
        self.abertura.filhos.sort(key=lambda r: Registro.ordem(r.nome, r.modulo))

        return self

    def totalizar_registros(self, ordenar_9900: bool = False) -> Self:
        """Totaliza os valores de contagem do bloco 9.

        Args:
            ordenar_9900: Se os registros 9900 devem ser ordenados de acordo com os registros que eles totalizam.
        """
        # Encontrando todos os nomes de registros presentes na escrituração
        registro_9001 = self.blocos["9"].abertura

        registros_9900 = registro_9001.filhos
        registros_9900_blc = [registro_9900.REG_BLC.valor_c for registro_9900 in registros_9900]

        registros_contagem = Counter(registro.nome for registro in self.registros)



        # Atualizando registros e removendo os que não existem mais
        registros_9900_remover = []

        for registro_9900 in registros_9900:
            nome_registro = registro_9900.REG_BLC.valor_c
            if nome_registro in registros_contagem:
                registro_9900.QTD_REG_BLC.valor_c = registros_contagem[nome_registro]
            else:
                registros_9900_remover.append(registro_9900)

        registro_9001.remover(registros_9900_remover)



        # Adicionando novos registros 9900 que não existiam antes
        for nome_registro in registros_contagem:
            if nome_registro not in registros_9900_blc:
                Registro(self.modulo, {
                    "REG": "9900",
                    "REG_BLC": nome_registro,
                    "QTD_REG_BLC": registros_contagem[nome_registro]
                }, pai=registro_9001)



        # Atualizando ou adicionando o Registro |9900|9900|
        try:
            registro_9900_9900 = self.blocos["9"].abertura.primeiro("9900", {"REG_BLC": "9900"}, recursivo=False)
            registro_9900_9900.QTD_REG_BLC.valor = len(registro_9001.filhos)
        except ValueError:
            Registro(self.modulo, {
                "REG": "9900",
                "REG_BLC": "9900",
                "QTD_REG_BLC": len(registro_9001.filhos) + 1
            }, pai=registro_9001)



        if ordenar_9900:
            # Ordenando os registros 9900 de acordo com o registro que ele totaliza
            registro_9001.filhos.sort(key=lambda r: Registro.ordem(r.REG_BLC.valor_c, self.modulo))

        return self










class EscrituracaoEcd(Escrituracao):
    """Contém informações sobre uma escrituração do módulo ECD e seus blocos e registros.

    Args:
        escrituracao_texto: Texto da escrituração a ser criada. Se não informado a escrituração é criada minimamente preenchida.

    Raises:
        TypeError: Se o texto não é de um tipo válido.
    """

    MODULO = Escrituracao.ECD
    """Nome do módulo ECD."""

    def __init__(self, escrituracao_texto: str | None = None) -> None:
        if isinstance(escrituracao_texto, str):
            super().__init__(ECD, escrituracao_texto, ECD.upper())
        elif escrituracao_texto is None:
            super().__init__(ECD, "|0000|||||||||||||||||||||||\n|9999|2|", ECD.upper())
        else:
            raise TypeError("Texto da escrituração inválido")



class EscrituracaoEcf(Escrituracao):
    """Contém informações sobre uma escrituração do módulo ECF e seus blocos e registros.

    Args:
        escrituracao_texto: Texto da escrituração a ser criada. Se não informado a escrituração é criada minimamente preenchida.

    Raises:
        TypeError: Se o texto não é de um tipo válido.
    """

    MODULO = Escrituracao.ECF
    """Nome do módulo ECF."""

    def __init__(self, escrituracao_texto: str | None = None) -> None:
        if isinstance(escrituracao_texto, str):
            super().__init__(ECF, escrituracao_texto, ECF.upper())
        elif escrituracao_texto is None:
            super().__init__(ECF, "|0000||||||||||||||||\n|9999|2|", ECF.upper())
        else:
            raise TypeError("Texto da escrituração inválido")



class EscrituracaoEfdContribuicoes(Escrituracao):
    """Contém informações sobre uma escrituração do módulo EFD_CONTRIBUICOES e seus blocos e registros.

    Args:
        escrituracao_texto: Texto da escrituração a ser criada. Se não informado a escrituração é criada minimamente preenchida.

    Raises:
        TypeError: Se o texto não é de um tipo válido.
    """

    MODULO = Escrituracao.EFD_CONTRIBUICOES
    """Nome do módulo EFD_CONTRIBUICOES."""

    def __init__(self, escrituracao_texto: str | None = None) -> None:
        if isinstance(escrituracao_texto, str):
            super().__init__(EFD_CONTRIBUICOES, escrituracao_texto, EFD_CONTRIBUICOES.upper())
        elif escrituracao_texto is None:
            super().__init__(EFD_CONTRIBUICOES, "|0000||||||||||||||\n|9999|2|", EFD_CONTRIBUICOES.upper())
        else:
            raise TypeError("Texto da escrituração inválido")



class EscrituracaoEfdIcmsIpi(Escrituracao):
    """Contém informações sobre uma escrituração do módulo EFD_ICMS_IPI e seus blocos e registros.

    Args:
        escrituracao_texto: Texto da escrituração a ser criada. Se não informado a escrituração é criada minimamente preenchida.

    Raises:
        TypeError: Se o texto não é de um tipo válido.
    """

    MODULO = Escrituracao.EFD_ICMS_IPI
    """Nome do módulo EFD_ICMS_IPI."""

    def __init__(self, escrituracao_texto: str | None = None) -> None:
        if isinstance(escrituracao_texto, str):
            super().__init__(EFD_ICMS_IPI, escrituracao_texto, EFD_ICMS_IPI.upper())
        elif escrituracao_texto is None:
            super().__init__(EFD_ICMS_IPI, "|0000|||||||||||||||\n|9999|2|", EFD_ICMS_IPI.upper())
        else:
            raise TypeError("Texto da escrituração inválido")
