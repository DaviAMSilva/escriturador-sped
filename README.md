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

# Crie o ambiente virtual (opcioinal)
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
