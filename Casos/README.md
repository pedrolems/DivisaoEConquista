# Casos de teste

Cada caso tem um arquivo `.in` (entrada no formato do enunciado) e um `.out`
(saída esperada). Para gerar de novo: `python Casos/gerar_casos.py`.
Para executar todos contra todas as versões: `python Casos/rodar_casos.py`.

Além destes arquivos, os testes unitários (`EtapaUm/test_sub_soma_max.py` e
`EtapaDois/test_par_pontos_prox.py`) comparam as versões com a força bruta em
milhares de entradas aleatórias.

## Etapa 1 — formato

- Entrada: `n` e depois `n` inteiros.
- Saída: `soma inicio fim`, com índices começando em 1.
- Desempate: maior soma; depois o intervalo que começa primeiro; depois o mais curto.

| Caso | Por que existe |
|---|---|
| 01_apenas_negativos | Borda pedida. A resposta é o maior elemento sozinho (-2), não 0 nem intervalo vazio. |
| 02_apenas_negativos_max_no_fim | Igual ao anterior, mas o maior está na última posição. Pega inicializações que só olham o começo do vetor. |
| 03_tamanho_um_positivo | Borda pedida. É o caso base da recursão. |
| 04_tamanho_um_negativo | Tamanho 1 com soma negativa. |
| 05_empate_inicio_mais_cedo | Borda pedida. `[3]`, `[3,-3,3]` e o `[3]` final somam 3; fica `1 1`. |
| 06_empate_entre_metades | Os intervalos empatados estão em metades diferentes, então o desempate acontece na combinação. |
| 07_empate_mesmo_inicio | `[2]` e `[2,0]` começam juntos; fica o mais curto. |
| 08_apenas_zeros | Todos os intervalos empatam em 0. |
| 09_zero_entre_negativos | O zero vence os negativos. |
| 10_apenas_positivos | A resposta é o vetor inteiro. |
| 11_exemplo_classico | Exemplo do livro (CLRS); resposta no meio do vetor. |
| 12_maximo_no_inicio | Resposta na primeira posição. |
| 13_maximo_no_fim | Resposta nas duas últimas posições. |
| 14_cruza_o_meio | A resposta só aparece no subarranjo que cruza o meio; nenhuma metade sozinha a contém. |
| 15_valores_grandes | Soma acima de 32 bits. |
| 16_aleatorio_n1000 | Entrada grande aleatória. |
| 17_aleatorio_muitos_empates_n1000 | Valores em [-2, 2]: muitos empates em uma entrada grande. |

## Etapa 2 — formato

- Entrada: `n` e depois `n` linhas `x y`.
- Saída: `distancia i j`, distância com 6 casas e índices (a partir de 1) com `i < j`.
- Em empates qualquer par com a distância mínima é aceito; o `rodar_casos.py`
  confere a distância e se o par devolvido realmente tem essa distância.

| Caso | Por que existe |
|---|---|
| 01_dois_pontos | Menor entrada válida. |
| 02_tres_pontos | Tamanho ímpar; metades de tamanhos diferentes. |
| 03_par_cruza_a_linha | Cada metade isolada tem distância 10, mas o par mais próximo tem um ponto de cada lado. Só a faixa encontra. |
| 04_pontos_repetidos | Duas estações na mesma posição (distância 0). |
| 05_mesmo_x | Todos na mesma vertical: a divisão pela mediana de x não pode depender de x distintos. |
| 06_mesmo_y | Todos na mesma horizontal. |
| 07_coordenadas_negativas | Coordenadas negativas. |
| 08_coordenadas_reais | Coordenadas não inteiras. |
| 09_empate_grade | Grade 3x3: vários pares a distância 1. |
| 10_faixa_cheia | Pontos concentrados perto da linha divisória: a faixa fica com quase todos os pontos. |
| 11_coordenadas_grandes | Coordenadas da ordem de 10⁹ (quadrados da ordem de 10¹⁸). |
| 12_aleatorio_n1000 | Entrada grande aleatória e esparsa. |
| 13_aleatorio_denso_n1000 | 1000 pontos em uma grade 41x41: muitos repetidos e empates. |
