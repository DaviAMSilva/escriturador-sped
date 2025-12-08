import json
from abc import ABC, abstractmethod

from ..classes.bloco import Bloco
from ..classes.registro import Registro
from ..constantes import EFD_ORDEM_BLOCOS
from ..ler_registros import ler_registros
from ..tabelas import EFD_INFO
from ..types import EfdTipo
from ..utilidades import registro_key, remover_assinatura_escrituracao
from .registro_contem import ContemRegistros
from .registro_lista import ListaRegistro










class Escrituracao(ContemRegistros, ABC):
    @abstractmethod
    def __init__(self, escrituracao_texto: str, nome: str, efd_tipo: EfdTipo) -> None:
        super().__init__(nome, efd_tipo, ListaRegistro())

        self.blocos: dict[str, Bloco] = {}

        self.abertura: Registro
        self.fechamento: Registro

        # Removendo a assinatura ou informações extra se existirem
        escrituracao_texto = remover_assinatura_escrituracao(escrituracao_texto)

        self._ler_escrituracao(escrituracao_texto)

        self.totalizar()



    def json(self, *args, indent=4, ensure_ascii=False, **kwargs) -> str:
        return json.dumps(self, indent=indent, ensure_ascii=ensure_ascii, default=lambda obj: obj.serialize(), *args, **kwargs)



    def texto(self) -> str:
        return self.abertura.texto() + self.fechamento.texto()



    def _ler_escrituracao(self, escrituracao_texto: str) -> None:
        registros_raizes = ler_registros(escrituracao_texto, self.efd_tipo)



        if len(registros_raizes) != 2 or registros_raizes[0].nome != "0000" or registros_raizes[1].nome != "9999":
            raise SyntaxError(f"Escrituração mal formatada ({registros_raizes})")



        # Informação da escrituração em si
        self.filhos = registros_raizes
        [self.abertura, self.fechamento] = registros_raizes



        # Preenchendo as informações dos blocos
        for bloco_info in EFD_INFO[self.efd_tipo]["blocos"]:
            registro_bloco_abertura: Registro | None = None
            registro_bloco_fechamento: Registro | None = None



            # Encontrando os registros de abertura e fechamento na lista de registros
            # Esse método encontra apenas os blocos presentes na escrituração atual,
            # não levando em consideração as condições de obrigatoriedade de blocos
            for escrituracao_registro in self.abertura.filhos:
                if escrituracao_registro.nome == bloco_info["abertura"]:
                    registro_bloco_abertura = escrituracao_registro
                    break

            for escrituracao_registro in self.abertura.filhos:
                if escrituracao_registro.nome == bloco_info["fechamento"]:
                    registro_bloco_fechamento = escrituracao_registro
                    break

            if registro_bloco_abertura and registro_bloco_fechamento:
                # Criando o bloco com os blocos de abertura e fechamento
                self.blocos[bloco_info["nome"]] = Bloco(bloco_info["nome"], registro_bloco_abertura, registro_bloco_fechamento, self.efd_tipo)
            elif registro_bloco_abertura is not None or registro_bloco_fechamento is not None:
                # Apenas um dos registros de abertura ou fechamento existe
                raise TypeError(f"Apenas um dos registros de abertura |{registro_bloco_abertura.nome if registro_bloco_abertura else None}|" +
                                f" ou fechamento |{registro_bloco_fechamento.nome if registro_bloco_fechamento else None}| existe")



    def totalizar(self, ordenar_9900=False) -> None:
        # A totalização dos registros e dos blocos dependem um do outro
        # por isso, é necessário realizar a totalização dessa forma
        self.totalizar_blocos()
        self.totalizar_registros(ordenar_9900)
        self.totalizar_blocos()
        self.totalizar_escrituracao()

    def totalizar_escrituracao(self) -> None:
        self.fechamento[2].valor_c = self.tamanho

    def totalizar_blocos(self) -> None:
        for nome in EFD_ORDEM_BLOCOS[self.efd_tipo]:
            bloco = self.blocos.get(nome, None)

            if bloco:
                bloco.abertura[2].valor_c = 0 if bloco.tamanho > 2 else 1
                bloco.fechamento[2].valor_c = bloco.tamanho
            else:
                novo_abertura = Registro(f"|{nome}001|1|", self.efd_tipo)
                novo_fechamento = Registro(f"|{nome}990|2|", self.efd_tipo)

                novo_abertura.pai = self.abertura
                novo_fechamento.pai = self.abertura

                novo_bloco = Bloco(nome, novo_abertura, novo_fechamento, self.efd_tipo)
                self.blocos[nome] = novo_bloco

                self.abertura.filhos.append(novo_abertura)
                self.abertura.filhos.append(novo_fechamento)

        # Ordenar os blocos é obrigatório
        self.abertura.filhos.sort(key=lambda r: EFD_ORDEM_BLOCOS[self.efd_tipo].index(r.nome[0]))

    def totalizar_registros(self, ordenar_9900=False) -> None:
        # Encontrando todos os nomes de registros presentes na escrituração
        registro_9001 = self.pesquisar("9001")[0]

        registros_9900 = registro_9001.pesquisar("9900")
        registros_9900_blc = [registro_9900["REG_BLC"].valor_c for registro_9900 in registros_9900]

        registros_encontrados = set()
        for registro in self.pesquisar():
            nome = registro.nome
            registros_encontrados.add(nome)



        # Atualizando registros e removendo os que não existem mais
        registros_9900_remover = []

        for registro_9900 in registros_9900:
            registro_nome = registro_9900["REG_BLC"].valor_c
            if registro_nome in registros_encontrados:
                registro_9900["QTD_REG_BLC"].valor_c = len(self.pesquisar(registro_nome))
            else:
                registros_9900_remover.append(registro_9900)

        registro_9001.remover(registros_9900_remover)



        # Adicionando novos registros 9900 que não existiam antes
        for registro_nome in registros_encontrados:
            if registro_nome not in registros_9900_blc:
                novo_registro_9900 = Registro(f"|9900|{registro_nome}|{len(self.pesquisar(registro_nome))}|", self.efd_tipo)
                registro_9001.filhos.append(novo_registro_9900)



        # Atualizando ou adicionando o Registro |9900|9900|
        registro_9900_9900 = self.blocos["9"].pesquisar(lambda r: (r.nome == "9900" and r["REG_BLC"].valor_c == "9900"))
        registro_9900_9900 = registro_9900_9900[0] if registro_9900_9900 else None

        if registro_9900_9900:
            registro_9900_9900["QTD_REG_BLC"].valor_c = len(self.pesquisar("9900"))
        else:
            novo_registro_9900_9900 = Registro(f"|9900|9900|{len(self.pesquisar('9900'))}|", self.efd_tipo)
            registro_9001.filhos.append(novo_registro_9900_9900)



        if ordenar_9900:
            # Ordenando os registros 9900 de acordo com o registro que ele totaliza
            registro_9001.filhos.sort(key=lambda r: registro_key(r["REG_BLC"].valor_c, self.efd_tipo))










class EscrituracaoICMSIPI(Escrituracao):
    def __init__(self, escrituracao_texto: str) -> None:
        super().__init__(escrituracao_texto, "EFD_ICMS_IPI", "efd_icms_ipi")



class EscrituracaoPISCOFINS(Escrituracao):
    def __init__(self, escrituracao_texto: str) -> None:
        super().__init__(escrituracao_texto, "EFD_PIS_COFINS", "efd_pis_cofins")
