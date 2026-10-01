"""Biblioteca para auxiliar a criação e edição de arquivos de escrituração do SPED brasileiro."""
from .arquivos import abrir_escrituracao, remover_assinatura_escrituracao, salvar_escrituracao
from .classes import *
from .constantes import *
from .estruturas import *
from .leitura import ler_registros
from .modulos import MODULOS, MODULOS_NOMES, MODULOS_PADROES, ModulosT, ModuloT, carregar_modulo
from .tipos import *
