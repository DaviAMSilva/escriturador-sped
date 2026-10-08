---
hide: toc
---

# Exemplos Práticos

## Alterando Valores de Registros

O exemplo abaixo abre uma escrituração que já existe, encontra todas as notas avulsas de entrada e defini a situação do documento como 08.

```python title="Alterando Valores de Registros"
from escriturador_sped import EscrituracaoEfdIcmsIpi as Registro

# Abrindo uma escrituração de um arquivo já existente
escrituracao = Registro.abrir("escrituracao.txt")

# Conseguindo o bloco C
bloco_c = escrituracao["C"]

# Loop de todos os registros do tipo C100
for registro_C100 in bloco_c.buscar("C100"):
    # Todos os campos contém duas representações do mesmo valor interno e a
    # extração desses valores segue a definição de tipos de campos dos manuais:
    # valor_c: Valor Alfanumérico (str)
    # valor_n: Valor Numérico (int | float | None)
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

## Criando, Adicionando e Removendo Registros

Novos registros são criados usando o texto da linha final, de maneira idêntica ao arquivo de escrituração, ou usando um dicionário contendo apenas os campos considerados relevantes.

As funções `registro.adicionar()` e `registro.remover()` são usadas para modificar a lista de filhos diretos de um registro específico. Também é possível usar uma lista de registros em ambas para modificar múltiplos filhos de uma vez. Ao remover também há a alternativa de usar [filtros](./realizando-buscas.md) para encontrar quais registros a serem removidos.

No exemplo abaixo será recriado o arquivo de exemplo `efd_contribuicoes_3.txt` iniciando-se de uma escrituração vazia:

```python title="Criando, Adicionando e Removendo Registros"
# Uma convenção opcional é renomear as classes do módulo a ser usado simplesmente como Escrituracao e Registro
# Assim independente de qual módulo estiver em uso o nomes das classes usadas são sempre os mesmos
from escriturador_sped import EscrituracaoEfdContribuicoes as Escrituracao, RegistroEfdContribuicoes as Registro

# O caminho 'escriturador_sped.modulos' oferece todas as versões de módulos suportados pela biblioteca
# Cada versão contém todos os registros conforme a versão (Registro0000, RegistroC100, etc.)
# Esses registros podem ser usados como atalhos para criação de novos registros ou com as funções 'como()' abaixo
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
# Aqui as funções 'como()' servem para explicar ao servidor de intellisense da sua IDE qual tipo
# de registro essa variável é e quais os campos estão disponíveis para preenchimento automático
registro_0001 = escrituracao["0"].abertura.como(Registro0001)
registro_m001 = escrituracao["M"].abertura.como(RegistroM001)

# A função de adicionar registros filhos aceitam um único registro ou uma lista de registros
# Se algum dos filhos a serem adicionados não for descendente direto a função gera uma exceção
# Método 1: Criar um registro usando o mesmo formato de linha dos arquivos de escrituração
registro_m001.adicionar([
    Registro("|M200|0|0|0|0|0|0|0|0|0|0|0|0|"),
    Registro("|M600|0|0|0|0|0|0|0|0|0|0|0|0|")
])

# Método 2: Criando um registro a partir de um dicionário onde cada chave é um nome de um campo
# Nesse caso casos não especificados são tratados como vazios e o campo 'REG' é obrigatório
# Caso fosse usada a subclasse 'Registro0140' o campo 'REG' poderia ser omitido
registro_0001.adicionar(Registro({
    "REG": "0140",
    "COD_EST": 1,
    "NOME": "EMPRESA XXX",
    "CNPJ": "99999999000191",
    "UF": "MG",
    "COD_MUN": 3106200
}))

# Existem várias formas de remover um registro, a mais simples sendo informar uma referência direta
# A remoção de registros é limitada a filhos diretos
registro_remover = escrituracao["A"].abertura.adicionar(Registro("|A010|00000000000000|"))
escrituracao["A"].remover(registro_remover)
# Alternativamente:
# escrituracao["A"].remover([registro_remover, ...]) # Múltiplos registros
# escrituracao["A"].remover(nome="A010")             # Usando filtros
# escrituracao["A"].limpar()                         # Removendo todos os registros

# Ao criar um novo registro é possível informar qual será o pai e adicionar filhos ao novo registro
# Os argumentos 'pai' e 'filhos' são do tipo palavra-chave (keyword) e precisam ser nomeados explicitamente
# Internamente isso executará 'pai.adicionar(self)' e 'self.adicionar(filhos)'
Registro(
    "|0110|1|2|1|1|",
    pai=registro_0001,
    filhos=[
        Registro("|0111|1|0|0|0|1|")
    ]
)

# Totalizando a escrituração com ordenação opcional dos registros bloco 9
escrituracao.totalizar(ordenar_9900=True)

# A função 'texto' está disponível para todos os componentes da escrituração
# e retorna o formato textual final para escrituração para aquele componente
print(escrituracao.texto())

# Converte a escrituração para texto e a salva no arquivo especificado
escrituracao.salvar("exemplos/efd_contribuicoes_2.txt")
```
