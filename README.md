<!-- markdownlint-disable first-line-h1 no-inline-html -->

[![pytest](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml)
[![pylint](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml)

# Escriturador SPED

<div align="center">
<img src="docs/logo.webp" alt="Logo and title of the project" width="30%" />
</div>

A biblioteca **Escriturador SPED** tem como objetivo providenciar uma API de acesso, criação e manipulação de arquivos de escrituração pertencentes ao projeto [SPED](https://www.gov.br/sped/pt-br) do governo brasileiro. A biblioteca escrita em [Python](http://python.org/) é destinada a programadores, ou usuários avançados, que trabalham com módulos do projeto SPED que envolvam a criação ou edição de escriturações.

## Módulos Suportados

<table>
    <tr>
        <td>Nome</td>
        <td>Identificador Interno</td>
        <td>Versão do Leiaute</td>
        <td>Versão do Manual</td>
        <td>Caminho Importação</td>
    </tr>
    <tr>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd">ECD</a></td>
        <td>ecd</td>
        <td>009</td>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd/manuais-e-documentos-tecnicos/manual_de_orientacao_da_ecd_leiaute_9_janeiro_2026.pdf/@@display-file/file">2026.01</a> (Cofis nº 01/2026)</td>
        <td><code>ecd.l009.v2026_01</code></td>
    </tr>
    <tr>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf">ECF</a></td>
        <td>ecf</td>
        <td>012</td>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf/manuais-e-documentos-tecnicos/manual_ecf_leiaute_12_20_05_2026_ac_2025_sit_esp_2026.pdf/@@display-file/file">2026.02</a> (Cofis nº 02/2026)</td>
        <td><code>ecf.l012.v2026_02</code></td>
    </tr>
    <tr>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes">EFD&nbsp;Contribuições</a></td>
        <td>efd_contribuicoes</td>
        <td>006</td>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes/manuais/guia_pratico_efd_contribuicoes_versao_1_35-18_06_2021.pdf/@@display-file/file">1.35</a></td>
        <td><code>efd_contribuicoes.l006.v1_35</code></td>
    </tr>
    <tr>
        <td rowspan="3"><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-icms-ipi">EFD ICMS IPI</a></td>
        <td rowspan="3">efd_icms_ipi</td>
        <td rowspan="2">020</td>
        <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-icms-ipi/manuais-e-documentos-tecnicos/guia-pratico-efd-versao-3-2-3.pdf/@@display-file/file">3.2.3</a></td>
        <td><code>efd_icms_ipi.l020.v3_2_3</code></td>
    </tr>
    <tr>
        <td rowspan="2"><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-icms-ipi/manuais-e-documentos-tecnicos/guia-pratico-efd-versao-3-2-4.pdf/@@display-file/file">3.2.4</a></td>
        <td><code>efd_icms_ipi.l020.v3_2_4</code></td>
    </tr>
    <tr>
        <td>021</td>
        <td><code>efd_icms_ipi.l021.v3_2_4</code></td>
    </tr>
</table>

## Instalação

Futuramente estará disponível em [PyPI](https://pypi.org/), mas por enquanto pode ser instalado diretamente do GitHub:

```bash
pip install git+https://github.com/DaviAMSilva/escriturador-sped
```

Ou instalação para desenvolvimento:

```bash
# Clonagem
git clone https://github.com/DaviAMSilva/escriturador-sped
cd escriturador-sped

# Crie o ambiente virtual (opcional)
python -m venv venv

# Ative o ambiente virtual:
# - Linux/MacOS: source venv/bin/activate
# - CMD: .\venv\Scripts\activate.bat
# - Powershell: .\venv\Scripts\Activate.ps1

# Instalação editável com ferramentas de desenvolvimento
pip install -e .[DEV]

# Scripts intermediários
invoke conversor
invoke tipagem

# Scripts de teste e lintagem
invoke test
invoke lint
```

## Exemplo de Uso

### Exemplo Básico

O exemplo abaixo abre uma escrituração que já existe, encontra todas as notas avulsas de entrada e defini a situação do documento como 08

```python
from escriturador_sped import EscrituracaoEfdIcmsIpi as Registro

# Abrindo uma escrituração de um arquivo já existente
escrituracao = Registro.abrir("escrituracao.txt")

# Conseguindo o bloco C
bloco_c = escrituracao["C"]

# Loop de todos os registros do tipo C100
for registro_C100 in bloco_c.buscar("C100"):
    # Todos os campos contém duas representações do mesmo valor interno e a
    # extração desses valores segue a definição de tipos de campos dos manuais:
    # valor_c: Valor Alfanumérico
    # valor_n: Valor Numérico
    operacao = registro_C100.IND_OPER.valor_c
    emissor = registro_C100.IND_EMIT.valor_c
    situacao = registro_C100.COD_SIT.valor_c
    cnpj_chave = registro_C100.CHV_NFE.valor_c[6:20]
    cnpj_empresa = registro_C100.COD_PART.valor_c # Assumindo código igual a CNPJ

    # operacao == "0": Operação de entrada
    # emissor  == "1": Emissão de terceiros
    if operacao == "0" and emissor == "1" and situacao != 8 and cnpj_chave and cnpj_chave != cnpj_empresa:
        # Alterando o valor do campo (valor = "08" também seria válido)
        registro_C100.COD_SIT.valor = 8

# Atualizando os registros de totalização do bloco 9 se registros forem adicionados ou removidos
escrituracao.totalizar()

# Salvando a escrituração em um arquivo separado
escrituracao.salvar("escrituracao_corrigida.txt")
```

### Exemplo Avançado

O exemplo abaixo gera um relatório com estrutura idêntica ao relatório de saídas presente no programa Validador EFD ICMS IPI. Para isso a biblioteca [pandas](https://pandas.pydata.org) é utilizada.

```python
import pandas as pd

# Importando a escrituração desejada e a função de carregar uma combinação módulo/leiaute/manual específica
from escriturador_sped import EscrituracaoEfdIcmsIpi as Registro, carregar_modulo

# Importando os registros derivados para uma combinação módulo/leiaute/manual específica
# É possível importar todos os registros ou apenas os registros a serem usados
from escriturador_sped.modulos.efd_icms_ipi.l020.m3_2_4.registros import *

# Carregando uma das combinações módulo/leiaute/manual suportadas pela a biblioteca
# Use 'python -m escriturador_sped' para listar as combinações suportadas
# Por padrão a biblioteca sempre irá carregar os módulos vigentes mais recentes
carregar_modulo(Registro.MODULO, "020", "3.2.4")

# Abrindo o arquivo da escrituração
escrituracao = Registro.abrir("escrituracao.txt")

# Lista das colunas no relatório final (mesmos nomes que os campos dos registros C100 e C190)
COLUNAS = [
    "COD_SIT", "CST_ICMS", "CFOP", "ALIQ_ICMS",
    "VL_OPR",
    "VL_BC_ICMS", "VL_ICMS",
    "VL_BC_ICMS_ST", "VL_ICMS_ST",
    "VL_RED_BC", "VL_IPI"
]

# Dicionário de colunas para o DataFrame
colunas = {campo: [] for campo in COLUNAS}

# Buscando todos os registros C100 de notas fiscais de saída
# Dica: A pesquisa de registros específicos pode ser feita diretamente na escrituração ou no bloco
# Mesmo assim é recomendado especificar o bloco para melhorar a clareza e velocidade da pesquisa
# escrituracao["C"].buscar("C100") <=> escrituracao.buscar("C100")
registros_c100_saida = escrituracao["C"].buscar("C100", campos={"IND_OPER": "1"})

# Loop por todos os registros C100->C190 para adicionar-los no relatório
for registro_c100 in registros_c100_saida.como(RegistroC100):
    cod_sit = registro_c100.COD_SIT.valor

    # A função 'como' está disponível nos resultados de busca (ListaRegistro)
    # ou em registros individuais e permite alterar a tipagem dos registros
    # genéricos em editores de texto que suportem tipagens da linguagem Python
    # Funciona do mesmo modo que a função 'cast' da biblioteca padrão 'typing'
    for registro_c190 in registro_c100.buscar("C190").como(RegistroC190):
        # A função 'valores' pode ser usada para alterar os valores dos
        # campos de um registros, mas também pode ser usada para retornar
        # um dicionário com os nomes e valores desses mesmos campos
        # Exemplo de alteração: registro_c190.valores({"CST_ICMS": 60})
        linha = registro_c190.valores()

        # COD_SIT é a única coluna cujo o valor depende do registro C100
        linha["COD_SIT"] = cod_sit

        # Adicionando cada item de cada linha no dicionário de colunas
        for nome in COLUNAS:
            colunas[nome].append(linha[nome])

# Cria o DataFrame, soma e agrupa os valores de todas as colunas,
# exceto as quatro primeiras: COD_SIT, CST_ICMS, CFOP e ALIQ_ICMS
# que são os mesmos do relatório no visualizador do SPED Fiscal
relatorio = (
    pd.DataFrame(colunas)
    .groupby(COLUNAS[:4], as_index=False)
    .sum()
    .set_index(COLUNAS[:4])
)

# Exibindo o DataFrame (exemplo fictício abaixo)
print(relatorio)

#                                  VL_OPR  VL_BC_ICMS  VL_ICMS  VL_BC_ICMS_ST  VL_ICMS_ST  VL_RED_BC  VL_IPI
# COD_SIT CST_ICMS CFOP ALIQ_ICMS                                                                           
# 00      000      5102 7           101.0         0.0      0.0            0.0         0.0        0.0     0.0
#                       18          115.0         0.0      0.0            0.0         0.0        0.0     0.0
#                       25           99.0         0.0      0.0            0.0         0.0        0.0     0.0
#         060      5405 0           114.0         0.0      0.0            0.0         0.0        0.0     0.0
#         200      5102 7           105.0         0.0      0.0            0.0         0.0        0.0     0.0
#         200      5102 12          116.0         0.0      0.0            0.0         0.0        0.0     0.0
#         200      5102 18          117.0         0.0      0.0            0.0         0.0        0.0     0.0
#         260      5405 0           114.0         0.0      0.0            0.0         0.0        0.0     0.0
# 08      000      5929 18           97.0         0.0      0.0            0.0         0.0        0.0     0.0
#         020      5929 12          100.0         0.0      0.0            0.0         0.0        0.0     0.0
#         040      5929 0           111.0         0.0      0.0            0.0         0.0        0.0     0.0
#         060      5929 0           114.0         0.0      0.0            0.0         0.0        0.0     0.0
```

## Criando, Adicionando e Removendo Registros

Novos registros são criados usando o texto da linha final, de maneira idêntica ao arquivo de escrituração, ou usando um dicionário contendo apenas os campos considerados relevantes.

As funções `registro.adicionar()` e `registro.remover()` são usadas para modificar a lista de filhos diretos de um registro específico. Também é possível usar uma lista de registros em ambas para modificar múltiplos filhos de uma vez. Ao remover também há a alternativa de usar filtros para encontrar quais registros a serem removidos.

No exemplo abaixo será recriado o arquivo de exemplo [`efd_contribuicoes_3.txt`](exemplos/efd_contribuicoes_2.txt) iniciando-se de uma escrituração vazia:

```python
# Uma conve# Uma convenção opcional é renomear as classes do módulo a ser usado simplesmente como Escrituracao e Registro
# Assim independente de qual módulo estiver em uso o nomes das classes usadas são sempre os mesmos
from escriturador_sped import EscrituracaoEfdContribuicoes as Escrituracao, RegistroEfdContribuicoes as Registro
from escriturador_sped.modulos.efd_contribuicoes.l006.m1_35.registros import *

# Ao criar uma escrituração sem parâmetros o resultado é uma escrituração "vazia" em que os únicos registros
# presentes são os de abertura e fechamento da escrituração e blocos além dos registros de totalização do bloco 9
escrituracao = Escrituracao()

# Com a escrituração vazia todos os campos (exceto REG) são inicializados vazios e precisam ser preenchidos
# Uma observação interessante é que para valores compostos apenas de números (como datas) não faz diferença se
# os valores estão em formato numérico ou de texto, internalmente ambos são convertidos para o formato apropriado
escrituracao.abertura.valores({
    "REG": "0000",
    "COD_VER": 2,
    "TIPO_ESCRIT": 0,
    "DT_INI": "01042011",
    "DT_FIN": "30042011",
    "NOME": "EMPRESA XXX",
    "CNPJ": "99999999000191",
    "UF": "MG",
    "COD_MUN": 3106200,
    "IND_NAT_PJ": 0,
    "IND_ATIV": 0
})

# Os atributos 'abertura' e 'fechamento' estão disponíveis para a escrituração e os blocos
# Na escrituração representam os registros 0000 e 9999
# No bloco qualquer X representam os registros X001 e X990
registro_0001 = escrituracao["0"].abertura
registro_m001 = escrituracao["M"].abertura

# A função de adicionar registros filhos aceitam um único registro ou uma lista de registros
# Se algum dos filhos a serem adicionados não for descendente direto a função gera uma exceção
registro_m001.adicionar([
    # Método 1: Criar um registro usando o mesmo formato de linha dos arquivos de escrituração
    Registro("|M200|0|0|0|0|0|0|0|0|0|0|0|0|"),
    Registro("|M600|0|0|0|0|0|0|0|0|0|0|0|0|")
])

# Método 2: Criando um registro a partir de um dicionário onde cada chave é um nome de um campo
# Nesse caso casos não especificados são tratados como vazios e o campo REG é obrigatório
registro_0001.adicionar(Registro({
    "REG": "0140",
    "COD_EST": 1,
    "NOME": "EMPRESA XXX",
    "CNPJ": "99999999000191",
    "UF": "MG",
    "COD_MUN": 3106200
}))

# O segundo parâmetro permite definir um registro 'pai' ao registro que está prestes a ser criado
# Internamente isso executará 'pai.adicionar(self)', que inclui a mesma verificação de parentesco
Registro("|0111|1|0|0|0|1|",
    Registro("|0110|1|2|1|1|", pai=registro_0001)
)

# Totalizando a escrituração com ordenação opcional dos registros bloco 9
escrituracao.totalizar(ordenar_9900=True)

# A função 'texto' está disponível para todos os componentes da escrituração
# e retorna o formato textual final para escrituração para aquele componente
print(escrituracao.texto())

# Converte a escrituração para texto e a salva no arquivo especificado
escrituracao.salvar("exemplos/efd_contribuicoes_2.txt")
```
