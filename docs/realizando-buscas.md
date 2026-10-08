# Realizando Buscas

As classes [Registro], [Bloco] e [ListaRegistro] suportam a busca de registros dentro de si mesmos. Ambas usam a função `#!python buscar()` para isso, com a mesma sintaxe de comandos e o retorno de outra [ListaRegistro] com os registros encontrados.

A filtragem dos registros a serem encontrados funciona por meio de lista branca, em que que cada registro precisa ser válido em cada parâmetro para estar presente no resultado retornado.

Caso a função seja executado sem nenhum filtro, todos os registros são retornados (mas para essa situação existe a propriedade atalho [`registros`](./classes/componente.md/#escriturador_sped.classes.componente.Componente.registros)). Adicionalmente a função `#!python primeiro()` está presente nas mesmas classes que `#!python buscar()`, e é um atalho equivalente a `#!python buscar(..., primeiro=True)[0]`.

Finalmente os mesmo parâmetros também podem aparecer parcialmente em outras funções que realizam uma ação baseada em um conjunto de filtro especificado. Especificamente a função [`#!python remover()`](./classes/registro.md/#escriturador_sped.classes.registro.Registro.remover) e [`#!python teste()`](./classes/registro.md/#escriturador_sped.classes.registro.Registro.teste).

---

::: escriturador_sped.classes.componente.Componente.buscar
    options:
      show_root_heading: true
      show_root_full_path: false
      heading_level: 3
      parameter_headings: true

[Registro]: ./classes/registro.md
[Bloco]: ./classes/bloco.md
[ListaRegistro]: ./estruturas/lista-registro.md
