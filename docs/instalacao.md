# Instalação

## Instalação Básica

Futuramente estará disponível em [PyPI](https://pypi.org/), mas por enquanto pode ser instalado diretamente do GitHub:

```bash
pip install git+https://github.com/DaviAMSilva/escriturador-sped
```

Use o comando abaixo para visualizar a lista de módulos presentes na instalação:

```bash
$ python -m escriturador_sped
Módulos disponíveis no Escriturador SPED (v1.4.2):
* = Manual carregado por padrão

[ecd]
* Leiaute: 009 - Manual: 2026.01

[ecf]
* Leiaute: 012 - Manual: 2026.02

[efd_contribuicoes]
* Leiaute: 006 - Manual: 1.35

[efd_icms_ipi]
  Leiaute: 020 - Manual: 3.2.3
* Leiaute: 020 - Manual: 3.2.4
  Leiaute: 021 - Manual: 3.2.4
```

## Instalação para Desenvolvimento

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

## Comandos `invoke`

A ferramenta [invoke](https://www.pyinvoke.org/) para python é essencialmente equivalente aos comandos do tipo `npm run <comando>` ao usar Node, mas precisa ser instalada separadamente (já presente no extra `DEV`).

- **``venv [--python ('python')] [--pasta ('venv')]``:**

    Cria um ambiente virtual python. Opcionalmente, usando a versão do python e a pasta do ambiente informadas. Mostra instruções sobre como ativar o ambiente virtual.

- **``install [--dev]``:**

    Instala a biblioteca, opcionalmente com as bibliotecas de desenvolvimento.

- **``conversor [--formatado]``:**

    Converte os arquivos de módulos presentes nas pastas `modulos/[modulo]/[leiaute]/[manual]/` para os arquivos `src/escriturador_sped/modulos/[modulo]/[leiaute]/[manual]/modulo.json`. Opcionalmente formate o arquivo gerado para ficar fácil de ler.

- **``tipagem [--lint]:``:** <small>(Requer `invoke conversor`)</small>

    Gera os arquivos de tipagem de registros em `src/escriturador_sped/modulos/[modulo]/[leiaute]/[manual]/registros.py`.

- **``mkdocs-serve``:**

    Roda o servidor de testes de [mkdocs](https://www.mkdocs.org/).

- **``build-docs [--formatado]``:** <small>(Requer `invoke conversor`)</small>

    Cria o arquivo `docs/modulos/modulos.js` necessário para o Visualizador de Módulos SPED. Opcionalmente formate o arquivo gerado para ficar fácil de ler.

- **``build [--sdist] [--wheel]``:**

    Cria os arquivos do pacote python. Opcionalmente os tipos de arquivos a serem gerados.

- **``lint``:**

    Analisa todos os arquivos python, procurando erros e inconsistências de estilo.

- **``markdownlint``:**

    Analisa todos os arquivos markdown, procurando erros e inconsistências de estilo.

- **``test [--coverage] [--profile] [--profile-svg]``:**

    Rodas os testes unitários da biblioteca. Opcionalmente:

    - `--coverage`: Permite encontrar seções de código que não estão sendo testadas;
    - `--profile`: Identificar as seções de código que mais e menos gastam tempo de processamento.
    - `--profile-svg`: O mesmo que a opção acima, mas gera uma imagem SVG útil para o mesmo propósito.

- **``snakeviz [--arquivo ('.prof/combined.prof')]``:** <small>(Requer `invoke test --profile`)</small>

    Usa a ferramenta [snakeviz](https://jiffyclub.github.io/snakeviz/) para visualizar os arquivos de *profiling* do comando anterior.
