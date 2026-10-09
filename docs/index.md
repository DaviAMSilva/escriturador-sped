---
description: Biblioteca Python para auxiliar a criação e edição de arquivos de escrituração do SPED brasileiro.
hide: toc
---

<!-- markdownlint-disable no-inline-html -->

# Escriturador SPED

<style>
.md-content .md-button {
    width: 100%;
    text-align: center;
}

img#logo {
    width: 20%;
    min-width: 200px;
    max-width: 100%;
}

.intro {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.intro img#logo {
    flex: 0 0 220px;
    width: 220px;
    max-width: 100%;
    height: auto;
}

.intro > div {
    flex: 1;
    min-width: 0;
}

/* mobile: stack, image on top and centered */
@media (max-width: 768px) {
    .intro {
        flex-direction: column;
        text-align: left;
    }

    .intro img#logo {
        flex: none;
        width: 160px;
        margin: 0 auto;
    }
}
</style>

<div class="intro" markdown="1">

<img id="logo" src="imagens/logo-transparente.webp" alt="Logo and title of the project" />

<div markdown="1">

A biblioteca **Escriturador SPED** tem como objetivo fornecer uma API de acesso, criação e manipulação de arquivos de escrituração pertencentes ao projeto [SPED](https://www.gov.br/sped/pt-br) do governo brasileiro. A biblioteca escrita em [Python](http://www.python.org/) é destinada a programadores, ou usuários avançados, que trabalham com módulos do projeto SPED que envolvam a criação ou edição de escriturações.

Especificamente esse projeto permite que o desenvolvedor abra, busque, altere e salve a estrutura de uma escrituração. Essa biblioteca não realiza a validação individual ou total dos valores dos campos, apenas a formatação desses campos é garantida. A única maneira oficial de validar uma escrituração é usando os [programas disponibilizados](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/download/sped) pelo governo.

</div>

</div>

<div class="grid cards" markdown>

[Instalação](./instalacao.md){ .md-button .md-button--primary .card }

[Conceitos Básicos](./conceitos-basicos.md){ .md-button .md-button--primary .card }

[Exemplos Práticos](./exemplos-praticos.md){ .md-button .md-button--primary .card }

[Realizando Buscas](./realizando-buscas.md){ .md-button .md-button--primary .card }

<br />

<br />

[Módulos Suportados](./modulos-suportados.md){ .md-button .card }

[Visualizador de Módulos SPED](/modulos){ .md-button .card }

</div>
