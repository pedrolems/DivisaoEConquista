# Trabalho Prático — Divisão e Conquista

Implementação, testes e análise experimental de dois problemas resolvidos por
divisão e conquista, cada um comparado com uma solução de força bruta.

Linguagem: Python 3 (testado com 3.13). Os algoritmos usam apenas a biblioteca
padrão; os gráficos usam `matplotlib`.

## Estrutura

```
EtapaUm/      Subarranjo de soma máxima (força bruta, D&C e Kadane) + testes
EtapaDois/    Par de pontos mais próximos (força bruta e D&C) + testes
Casos/        Arquivos .in/.out com os casos de teste e o script que os executa
Experimentos/ Scripts de medição e análise, CSVs brutos, gráficos e tabelas
Relatorio/    Fonte LaTeX e PDF do relatório
```

## Como executar

### Etapa 1 — subarranjo de soma máxima

```
python EtapaUm/Sub_Soma_Max.py [fb|dc|kadane] < entrada.txt
```

- Entrada: `n` seguido de `n` inteiros.
- Saída: `soma inicio fim` (índices começando em 1).
- Sem argumento, usa a divisão e conquista (`dc`).
- Desempate: maior soma; depois o intervalo que começa primeiro; depois o mais curto.

Exemplo:

```
$ echo "9  -2 1 -3 4 -1 2 1 -5 4" | python EtapaUm/Sub_Soma_Max.py dc
6 4 7
```

### Etapa 2 — par de pontos mais próximos

```
python EtapaDois/Par_Pontos_Prox.py [fb|dc] [limiar] < entrada.txt
```

- Entrada: `n` seguido de `n` pares `x y`.
- Saída: `distancia i j` (6 casas decimais; índices começando em 1, `i < j`).
- `limiar` é opcional (padrão 16): subproblemas com até esse número de pontos
  são resolvidos por força bruta.

Exemplo:

```
$ printf "3\n0 0\n10 10\n11 10\n" | python EtapaDois/Par_Pontos_Prox.py dc
1.000000 2 3
```

## Testes

```
cd EtapaUm   && python -m unittest -v && cd ..
cd EtapaDois && python -m unittest -v && cd ..
python Casos/rodar_casos.py
```

Os testes unitários cobrem os casos de borda (com a justificativa de cada um
na docstring) e comparam as versões com a força bruta em milhares de entradas
aleatórias. Os casos em arquivo estão descritos em [Casos/README.md](Casos/README.md).

## Experimentos

```
pip install matplotlib
python Experimentos/medir.py      # demora alguns minutos por causa da força bruta
python Experimentos/analisar.py
```

- `Experimentos/medicoes.csv`: uma linha por execução (5 por tamanho, n de 100 a 6400).
- `Experimentos/limiar.csv`: D&C da etapa 2 com limiares de 1 a 128.
- `Experimentos/pequenos.csv`: tamanhos de 2 a 256, para ver quando a força bruta ganha.
- `Experimentos/maquina.txt`: configuração da máquina das medições.
- `Experimentos/tabelas.md` e `Experimentos/graficos/`: médias e gráficos.

## Relatório

`Relatorio/relatorio.pdf` (fonte em `Relatorio/relatorio.tex`).
