# Tabelas

O propósito do arquivo [conversor_tabelas.py] é converter as tabelas em formato csv para o arquivo [efd_info.json] em estrutura específica para utilização nesse projeto.

Os arquivos csv foram gerados a partir da ferramenta [sped-extractor], utilizando os seguintes documentos:

- [Guia Prático EFD-ICMS/IPI – Versão 3.1.6](http://sped.rfb.gov.br/arquivo/download/7291) (*09/11/2023*)
- [Guia Prático da EFD Contribuições – Versão 1.35](http://sped.rfb.gov.br/arquivo/download/5836) (*18/06/2021*)

Para verificar as versões mais recentes possíveis, visite o site do [SPED].

Futuramente é possível implementar uma integração direta com o [sped-extractor] para automatizar o processo, mas devido à velocidade de atualização dos manuais do SPED isso não é prioridade.

[conversor_tabelas.py]: conversor_tabelas.py
[efd_info.json]: efd_info.json
[sped-extractor]: https://github.com/akretion/sped-extractor
[SPED]: http://sped.rfb.gov.br/
