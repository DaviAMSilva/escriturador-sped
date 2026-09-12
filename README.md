<!-- markdownlint-disable first-line-h1 no-inline-html -->

[![pytest](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml)
[![pylint](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml)

# Escriturador SPED

<div align="center">
<img src="logo.webp" alt="Logo and title of the project" width="30%" />
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

No exemplo abaixo abre uma escrituração que já existe, encontra todas as notas avulsas de entrada e defini a situação do documento como 08

```python
from escriturador_sped import EscrituracaoEfdIcmsIpi

# Abrindo uma escrituração de um arquivo já existente
escrituracao = EscrituracaoEfdIcmsIpi.abrir("escrituracao.txt")

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
    situacao = registro_C100.COD_SIT.valor_n
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
