# Conceitos Básicos

!!! warning "Aviso"

    Essa documentação supõe que o leitor já contêm conhecimento prévio do ambiente [SPED](https://www.gov.br/sped/pt-br) e suas escriturações, além de conhecimentos básicos de programação em [Python](https://www.python.org/).

- **[Componente](./classes/componente.md): A classe base da qual as classes Escrituração, Bloco e Registro abaixo são derivadas.**

    Contém métodos e atributos comuns a todas essas classes.

- **[Escrituração](./classes/escrituracao.md): A classe que armazena as informações de uma escrituração.**

    Escriturações contêm exatamente dois registros filhos, um de abertura e um de fechamento.  
    Contêm uma quantidade limitada de blocos, dependente no tipo do módulo em questão, alguns obrigatórios e o resto opcional.

- **[Bloco](./classes/bloco.md): A classe que armazena as informações de um bloco.**

    Blocos contêm exatamente dois registros filhos, um de abertura e um de fechamento.

- **[Registro](./classes/registro.md): A classe que armazena as informações de um registro.**

    Registros podem conter qualquer quantidade de registros filhos, incluindo nenhum filho.  
    Registros contêm um referência ao registro pai, exceto os registros `0000` e `9999` de abertura e fechamento de um escrituração.  
    Registros contêm uma quantidade variável de campos, dependente do tipo do registro informado durante a sua criação.

- **[Campo](./campos.md): A classe que armazena as informações de um registro.**

    Campos contém informações sobre as propriedade que o campo representado tem e os valores atuais dele.  
    Campos têm as suas propriedades definidas durante a criação de um registro.

- **[ListaRegistro](./estruturas-de-dados/lista-registro.md): Uma estrutura de dados especial para armazenar uma lista de registros.**

    Contém funcionalidades próprias para a manipulação de vários registros, especialmente ao realizar [buscas](./buscas.md).

- **[TuplaCampo](./estruturas-de-dados/tupla-campo.md): Uma estrutura de dados especial para armazenar uma tupla de campos.**

    Contém funcionalidades próprias para o acesso dos campos de um registro.
