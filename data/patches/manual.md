# MANUAL

## EFD_ICMS_IPI - accurate_fields.csv - Adicionar

```text
"B035","53","01","REG","Texto fixo contendo “B035”","C","004*","-","","Não informar","O"
"B035","53","02","VL_CONT_P","Parcela correspondente ao “Valor Contábil” referente à combinação da alíquota e item da lista","N","-","02","","Não informar","O"
"B035","53","03","VL_BC_ISS_P","Parcela correspondente ao “Valor da base de cálculo do ISS” referente à combinação da alíquota e item da lista","N","-","02","","Não informar","O"
"B035","53","04","ALIQ_ISS","Alíquota do ISS","N","-","02","","Não informar","O"
"B035","53","05","VL_ISS_P","Parcela correspondente ao “Valor do ISS” referente à combinação da alíquota e item da lista","N","-","02","","Não informar","O"
"B035","53","06","VL_ISNT_ISS_P","Parcela correspondente ao “Valor das operações isentas ou não-tributadas pelo ISS” referente à combinação da alíquota e item da lista","N","-","02","","Não informar","O"
"B035","53","07","COD_SERV","Item da lista de serviços, conforme Tabela 4.6.3.","C","004*","-","","Não informar","O"
```

```text
"C181","97","13","VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA","Valor médio unitário do ICMS OP, das mercadorias em estoque, correspondente ao valor do campo VL_UNIT_ICMS_OP_ESTOQUE_CONV, preenchido na ocasião da saída","N","-","06","","OC",""
"C181","97","14","VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA","Valor médio unitário do ICMS ST, incluindo FCP ST, das mercadorias em estoque, correspondente ao valor do campo VL_UNIT_ICMS_ST_ESTOQUE_CONV, preenchido na ocasião da saída","N","-","06","","OC",""
"C181","97","15","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV_SAIDA","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, correspondente ao valor do campo VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV, preenchido na ocasião da saída","N","-","06","","OC",""
"C181","97","16","VL_UNIT_ICMS_NA_OPERACAO_CONV_SAIDA","Valor unitário para o ICMS na operação, correspondente ao valor do campo VL_UNIT_ICMS_NA_OPERACAO_CONV, preenchido na ocasião da saída","N","-","06","","OC",""
"C181","97","17","VL_UNIT_ICMS_OP_CONV_SAIDA","Valor unitário do ICMS correspondente ao valor do campo VL_UNIT_ICMS_OP_CONV, preenchido na ocasião da saída","N","-","06","","OC",""
"C181","97","18","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, correspondente ao estorno do complemento apurado na operação de saída.","N","-","06","","OC",""
"C181","97","19","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","OC",""
"C181","97","20","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do estorno do ressarcimento/restituição, incluindo FCP ST, apurado na operação de saída.","N","-","06","","OC",""
"C181","97","21","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","OC",""
```

```text
"C185","101","14","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP agregado ao ICMS das mercadorias em estoque, considerando a unidade utilizada para informar o campo “QUANT_CONV”","N","-","06","","","OC"
"C185","101","15","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C185","101","16","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C185","101","17","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C185","101","18","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
```

```text
"C186","104","17","VL_UNIT_BC_ICMS_ST_CONV_ENTRADA","Valor unitário da base de cálculo do imposto pago ou retido anteriormente por substituição, correspondente ao valor do campo VL_UNIT_BC_ICMS_ST_CONV, preenchido na ocasião da entrada","N","-","06","","","OC"
"C186","104","18","VL_UNIT_ICMS_ST_CONV_ENTRADA","Valor unitário do imposto pago ou retido anteriormente por substituição, inclusive FCP se devido, correspondente ao valor do campo VL_UNIT_ICMS_ST_CONV, preenchido na ocasião da entrada","N","-","06","","","OC"
"C186","104","19","VL_UNIT_FCP_ST_CONV_ENTRADA","Valor unitário do FCP_ST, correspondente ao valor do campo VL_UNIT_FCP_ST_CONV, preenchido na ocasião da entrada","N","-","06","","","OC"
```

```text
"C330","113","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”","N","-","06","","","OC"
"C330","114","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C330","114","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C330","114","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C330","114","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
```

```text
"C380","118","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C380","118","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C380","118","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C380","118","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C380","118","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C380","118","15","CST_ICMS","Código da Situação Tributária referente ao ICMS","N","003*","-","","","O"
"C380","118","16","CFOP","Código Fiscal de Operação e Prestação","N","004*","-","","","O"
```

```text
"C430","125","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C430","125","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C430","125","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C430","125","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C430","125","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C430","126","15","CST_ICMS","Código da Situação Tributária referente ao ICMS","N","003*","-","","","O"
"C430","126","16","CFOP","Código Fiscal de Operação e Prestação","N","004*","-","","","O"
```

```text
"C480","131","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C480","131","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C480","131","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C480","131","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C480","131","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C480","131","15","CST_ICMS","Código da Situação Tributária referente ao ICMS","N","003*","-","","","O"
"C480","131","16","CFOP","Código Fiscal de Operação e Prestação","N","004*","-","","","O"
```

```text
"C815","158","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C815","158","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C815","158","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C815","158","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
"C815","158","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","06","","","OC"
```

```text
"C880","165","10","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","Valor médio unitário do FCP ST agregado ao ICMS das mercadorias em estoque, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","03","","","OC"
"C880","165","11","VL_UNIT_ICMS_ST_CONV_REST","Valor unitário do total do ICMS ST, incluindo FCP ST, a ser restituído/ressarcido, calculado conforme a legislação de cada UF, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","03","","","OC"
"C880","165","12","VL_UNIT_FCP_ST_CONV_REST","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","03","","","OC"
"C880","165","13","VL_UNIT_ICMS_ST_CONV_COMPL","Valor unitário do complemento do ICMS, incluindo FCP ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”.","N","-","03","","","OC"
"C880","165","14","VL_UNIT_FCP_ST_CONV_COMPL","Valor unitário correspondente à parcela de ICMS FCP ST que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”, considerando unidade utilizada para informar o campo “QUANT_CONV”.","N","-","03","","","OC"
```

```text
"H010","263","11","VL_ITEM_IR","Valor do item para efeitos do Imposto de Renda.","N","-","02","OC","",""
```

```text
"K230","272","06","QTD_ENC","Quantidade de produção acabada","N","-","6","O","",""
```

```text
"K260","275","07","QTD_RET","Quantidade de retorno ao estoque (entrada)","N","-","6","OC","",""
```

```text
"1105","289","07","COD_ITEM","Código do item (campo 02 do Registro 0200)","C","060","-","O","",""
```

```text
"1110","289","04","SER","Série do documento fiscal recebido com fins específicos de exportação.","C","004","-","OC","",""
"1110","289","05","NUM_DOC","Número do documento fiscal recebido com fins específicos de exportação.","N","009","-","O","",""
"1110","289","06","DT_DOC","Data da emissão do documento fiscal recebido com fins específicos de exportação","N","008*","-","O","",""
"1110","289","07","CHV_NFE","Chave da Nota Fiscal Eletrônica","N","044*","-","OC","",""
"1110","289","08","NR_ MEMO","Número do Memorando de Exportação","N","-","-","OC","",""
"1110","289","09","QTD","Quantidade do item efetivamente exportado.","N","-","03","O","",""
"1110","289","10","UNID","Unidade do item  (Campo 02 do registro 0190)","C","006","-","O","",""
```

## EFD_ICMS_IPI - accurate_fields.csv - Remover

```text
"C177","92","03","QT_SELO_IPI","Quantidade de selo de controle do IPI aplicada","N","012","-","","","O"
```

## EFD_ICMS_IPI - registers.csv - Adicionar

```text
"B","B035","","","True","3","1:N","","Não informar","O","Detalhamento por combinação de alíquota e item da lista de serviços da Lei Complementar nº 116/2003"
```

## EFD_PIS_COFINS - accurate_fields.csv - Adicionar

```text
"D505","219","08","COD_CTA","Código da conta analítica contábil debitada/creditada","C","255","-","N"
```
