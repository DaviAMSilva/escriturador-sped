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

function Modulo(modulo, leiaute, versao, registros) {
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
                    ${Object.entries(registros).map(([nome, registro]) => {
                        return html`<tr>
                            <td>
                                <a id=${nome} href="#${nome}" class="registro">${nome}</a>
                            </td>
                            <td>
                                <span>
                                    ${registro.campos.map((campo, i) => {
                                        const numeroFormatado = String(campo.numero).padStart(2, "0");
                                        return html`
                                            <span class="pipe">|</span>
                                            <span class="wj">⁠</span>
                                            <span id="${nome}-${numeroFormatado}" class="campo">
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
    function formatar(item) {
        return `Módulo: ${item.modulo.toUpperCase()} — Leiaute: ${item.leiaute.padStart(3, "0")} — Versão: ${item.versao}`;
    }

    function chave(item) {
        return `${item.modulo}-${item.leiaute.padStart(3, "0")}-${item.versao}`;
    }

    const tabelas = Object.entries(MODULOS).flatMap(([modulo, leiautes]) => {
        return Object.entries(leiautes).flatMap(([leiaute, versoes]) => {
            return Object.entries(versoes).map(([versao, dados]) => {
                return { modulo, leiaute, versao, blocos: dados.blocos, registros: dados.registros };
            });
        });
    });

    const [tabelaChave, setTabelaChave] = useState(() => {
        const tabelaChaveSalva = localStorage.getItem("tabelaChave");
        return tabelas.some((tabela) => chave(tabela) === tabelaChaveSalva) ? tabelaChaveSalva : chave(tabelas[0]);
    });
    const tabelaAtual = tabelas.find((m) => chave(m) === tabelaChave);

    useEffect(() => {
        localStorage.setItem("tabelaChave", tabelaChave);
    }, [tabelaChave]);

    return html`
        <span>Escolha a tabela a ser visualizada: </span>
        <select value=${tabelaChave} onChange=${(e) => setTabelaChave(e.target.value)}>
            ${tabelas.map((m) => {
                const c = chave(m);
                return html`<option key="${c}" value="${c}">${formatar(m)}</option>`;
            })}
        </select>
        ${tabelaAtual && Modulo(tabelaAtual.modulo, tabelaAtual.leiaute, tabelaAtual.versao, tabelaAtual.registros)}
    `;
}

render(html`<${App} />`, document.getElementById("app"));
