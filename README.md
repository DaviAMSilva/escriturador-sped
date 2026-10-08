<!-- markdownlint-disable first-line-h1 no-inline-html -->

[![PyPI](https://img.shields.io/pypi/v/escriturador-sped)](https://pypi.org/project/escriturador-sped/)
[![Python](https://img.shields.io/pypi/pyversions/escriturador-sped)](https://pypi.org/project/escriturador-sped/)
[![Licença](https://img.shields.io/github/license/DaviAMSilva/escriturador-sped)](https://github.com/DaviAMSilva/escriturador-sped/blob/main/LICENSE)

[![pytest](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pytest.yml)
[![pylint](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/pylint.yml)
[![markdownlint](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/markdownlint.yml/badge.svg?branch=main)](https://github.com/DaviAMSilva/escriturador-sped/actions/workflows/markdownlint.yml)

# Escriturador SPED

<div align="center">
<img src="https://raw.githubusercontent.com/DaviAMSilva/escriturador-sped/main/docs/imagens/logo-transparente.webp" alt="Logo" width="40%" />
</div>

A biblioteca **Escriturador SPED** tem como objetivo fornecer uma API de acesso, criação e manipulação de arquivos de escrituração pertencentes ao projeto [SPED](https://www.gov.br/sped/pt-br) do governo brasileiro. A biblioteca escrita em [Python](https://www.python.org/) é destinada a programadores, ou usuários avançados, que trabalham com módulos do projeto SPED que envolvam a criação ou edição de escriturações.

Especificamente esse projeto permite que o desenvolvedor abra, busque, altere e salve a estrutura de uma escrituração. Essa biblioteca não realiza a validação individual ou total dos valores dos campos, apenas a formatação desses campos é garantida. A única maneira oficial de validar uma escrituração é usando os [programas disponibilizados](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/download/sped) pelo governo.

**Para mais informações consulte a [documentação](https://escriturador-sped.daviamsilva.dev).**

## Início Rápido

Instale a biblioteca com:

```bash
pip install escriturador-sped
```

Exemplo básico de uso:

```python
from escriturador_sped import EscrituracaoEfdIcmsIpi, RegistroEfdIcmsIpi

# Abrindo o arquivo de escrituração
escrituracao = EscrituracaoEfdIcmsIpi.abrir("original.txt")

# Adicionando um novo produto na escrituração (registro 0200 do bloco 0)
escrituracao["0"].abertura.adicionar(
    RegistroEfdIcmsIpi("|0200|100|PRODUTO|||UN|00|00000000||||||")
)

# Encontrando a nota de entrada com número 123
nota_123 = escrituracao.primeiro("C100", { "IND_OPER": "0", "NUM_DOC": 123 })

# Alterando a data de entrada da nota
nota_123.DT_E_S.valor = "07091822"

# Mostrando todos os registros associados a essa nota
print(nota_123.texto())

# Totalizando os registros do bloco 9
# Necessário apenas quando há adição ou remoção de registros
escrituracao.totalizar(ordenar_9900=True)

# Salvando a escrituração alterada para outro arquivo
escrituracao.salvar("alterada.txt")
```

## Módulos Suportados

<table>
    <thead>
        <tr>
            <th>Nome</th>
            <th>Identificador Interno</th>
            <th>Versão do Leiaute</th>
            <th>Versão do Manual</th>
            <th>Caminho de Importação</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd">ECD</a></td>
            <td>ecd</td>
            <td>009</td>
            <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd/manuais-e-documentos-tecnicos/manual_de_orientacao_da_ecd_leiaute_9_janeiro_2026.pdf/@@display-file/file">2026.01</a><br />(Cofis nº 01/2026)</td>
            <td><code>ecd.l009.v2026_01</code></td>
        </tr>
        <tr>
            <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf">ECF</a></td>
            <td>ecf</td>
            <td>012</td>
            <td><a href="https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf/manuais-e-documentos-tecnicos/manual_ecf_leiaute_12_20_05_2026_ac_2025_sit_esp_2026.pdf/@@display-file/file">2026.02</a><br />(Cofis nº 02/2026)</td>
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
    </tbody>
</table>

> ⚠️ **Atenção:**  
> Todos os módulos acima são funcionais, entretanto apenas os módulos `efd_contribuicoes` e `efd_icms_ipi` foram testados extensivamente.  
> Problemas encontrados em algum dos módulos podem ser reportados na página de [issues](https://github.com/DaviAMSilva/escriturador-sped/issues).
