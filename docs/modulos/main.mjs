import { h, render } from "https://esm.sh/preact@10";
import { useEffect, useState } from "https://esm.sh/preact@10/hooks";
import htm from "https://esm.sh/htm@3";

const html = htm.bind(h);

if (typeof MODULOS === "undefined") {
    const mensagemAviso = "O arquivo modulos.js não foi encontrado. Tenha certeza que o arquivo foi gerado corretamente.";
    const elementoAviso = document.createElement("div");
    elementoAviso.style.color = "red";
    elementoAviso.textContent = mensagemAviso;
    document.body.innerHTML = "";
    document.body.appendChild(elementoAviso);
    throw new Error("Erro ao carregar o arquivo modulos.js (MODULOS é undefined)");
}

function Tabela(registros) {
    return html`
        <div>
            <table class="tabela">
                <thead>
                    <tr>
                        <th>Registro</th>
                        <th>Campos</th>
                    </tr>
                </thead>
                <tbody>
                    ${registros.map(([nome, registro]) => {
                        const { campos, ...outrosDados } = registro;

                        return html`<tr>
                            <td>
                                <a id=${nome} href="#${nome}" class="registro" data-title="${JSON.stringify(outrosDados, null, 2)}">${nome}</a>
                            </td>
                            <td>
                                <span>
                                    ${registro.campos.map((campo) => {
                                        const numeroFormatado = String(campo.numero).padStart(2, "0");
                                        return html`
                                            <span class="pipe">|</span>
                                            <span class="wj">⁠</span>
                                            <span id="${nome}-${numeroFormatado}" class="campo" data-title="${JSON.stringify(campo, null, 2)}">
                                                ${campo.nome}
                                                <small><a href="#${nome}-${numeroFormatado}">${numeroFormatado}</a></small>
                                            </span>
                                            <wbr />
                                        `;
                                    })}
                                    <span class="pipe">|</span>
                                </span>
                            </td>
                        </tr>`;
                    })}
                </tbody>
            </table>
        </div>
    `;
}

function App() {
    // TODO: Corrigir ordenação dos registros

    function formatar(tabela) {
        return `Módulo: ${tabela.modulo.toUpperCase()} — Leiaute: ${tabela.leiaute.padStart(3, "0")} — Versão: ${tabela.versao}`;
    }

    function chave(tabela) {
        return `${tabela.modulo}-${tabela.leiaute.padStart(3, "0")}-${tabela.versao}`;
    }

    const tabelas = Object.entries(MODULOS).flatMap(([modulo, leiautes]) => {
        return Object.entries(leiautes).flatMap(([leiaute, versoes]) => {
            return Object.entries(versoes).map(([versao, dados]) => {
                const blocosOrdem = Object.fromEntries(dados.blocos.map((k, v) => [k.nome, v]));

                const registros = Object.entries(dados.registros).sort((a, b) => {
                    return blocosOrdem[a[0][0]] - blocosOrdem[b[0][0]];
                });

                return { modulo, leiaute, versao, blocos: dados.blocos, registros: registros };
            });
        });
    });

    const [tabelaChave, setTabelaChave] = useState(() => {
        const tabelaParametro = new URLSearchParams(window.location.search).get("tabela");
        const tabelaLocalStorage = localStorage.getItem("tabelaChave");
        return tabelas.some((tabela) => chave(tabela) === tabelaParametro)
            ? tabelaParametro
            : tabelas.some((tabela) => chave(tabela) === tabelaLocalStorage)
              ? tabelaLocalStorage
              : chave(tabelas[0]);
    });

    const tabelaAtual = tabelas.find((tabela) => chave(tabela) === tabelaChave);

    useEffect(() => {
        localStorage.setItem("tabelaChave", tabelaChave);
        const url = new URL(window.location.href);
        url.searchParams.set("tabela", chave(tabelaAtual));
        url.hash = "";
        window.history.replaceState(null, "", url);
    }, [tabelaChave, tabelaAtual]);

    return html`
        <div class="selecao">
            <span>Escolha a tabela a ser visualizada: </span>
            <select value=${tabelaChave} onChange=${(e) => setTabelaChave(e.target.value)}>
                ${tabelas.map((tabela) => {
                    const c = chave(tabela);
                    return html`<option key="${c}" value="${c}">${formatar(tabela)}</option>`;
                })}
            </select>
            <a href="/"><button type="button" class="voltar">Voltar para documentação</button></a>
        </div>
        ${tabelaAtual && Tabela(tabelaAtual.registros)}
    `;
}

render(html`<${App} />`, document.getElementById("app"));
