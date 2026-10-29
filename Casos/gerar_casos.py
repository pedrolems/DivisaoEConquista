"""Gera os arquivos .in/.out de Casos/etapa1 e Casos/etapa2.

A saída esperada é calculada com a força bruta, que serve de referência
por ser a implementação mais simples (os casos pequenos também foram
conferidos à mão, ver Casos/README.md).
"""

import math
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ.parent / "EtapaUm"))
sys.path.insert(0, str(RAIZ.parent / "EtapaDois"))

import Par_Pontos_Prox as e2  # noqa: E402
import Sub_Soma_Max as e1  # noqa: E402

gerador = random.Random(28102026)

CASOS_ETAPA1 = {
    "01_apenas_negativos": [-8, -2, -5],
    "02_apenas_negativos_max_no_fim": [-9, -7, -3],
    "03_tamanho_um_positivo": [7],
    "04_tamanho_um_negativo": [-4],
    "05_empate_inicio_mais_cedo": [3, -3, 3],
    "06_empate_entre_metades": [5, -10, 1, 4],
    "07_empate_mesmo_inicio": [2, 0, -1],
    "08_apenas_zeros": [0, 0, 0],
    "09_zero_entre_negativos": [-1, 0, -2],
    "10_apenas_positivos": [1, 2, 3, 4],
    "11_exemplo_classico": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
    "12_maximo_no_inicio": [10, -20, 1, 2],
    "13_maximo_no_fim": [1, -20, 3, 9],
    "14_cruza_o_meio": [-5, -5, 4, 4, -5, -5],
    "15_valores_grandes": [2_000_000_000, 2_000_000_000, -1],
    "16_aleatorio_n1000": [gerador.randint(-100, 100) for _ in range(1000)],
    "17_aleatorio_muitos_empates_n1000": [gerador.randint(-2, 2) for _ in range(1000)],
}

CASOS_ETAPA2 = {
    "01_dois_pontos": [(0, 0), (3, 4)],
    "02_tres_pontos": [(0, 0), (10, 10), (11, 10)],
    "03_par_cruza_a_linha": [(0, 0), (0, 10), (4, 5), (5, 5), (9, 0), (9, 10)],
    "04_pontos_repetidos": [(1, 1), (5, 5), (9, 9), (5, 5)],
    "05_mesmo_x": [(2, y) for y in (0, 7, 15, 16, 30, 50)],
    "06_mesmo_y": [(x, 4) for x in (0, 9, 20, 22, 40)],
    "07_coordenadas_negativas": [(-5, -5), (-1, -2), (3, 3), (10, -7)],
    "08_coordenadas_reais": [(0.5, 0.5), (0.6, 0.5), (3.0, 3.0)],
    "09_empate_grade": [(x, y) for x in range(3) for y in range(3)],
    "10_faixa_cheia": [(0, 2 * k) for k in range(20)] + [(1, 2 * k + 1) for k in range(20)],
    "11_coordenadas_grandes": [(10**9, 10**9), (-10**9, -10**9), (10**9, 10**9 - 3)],
    "12_aleatorio_n1000": [(gerador.randint(-10**6, 10**6), gerador.randint(-10**6, 10**6))
                           for _ in range(1000)],
    "13_aleatorio_denso_n1000": [(gerador.randint(0, 40), gerador.randint(0, 40))
                                 for _ in range(1000)],
}


def escrever(pasta: Path, nome: str, entrada: str, saida: str) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / f"{nome}.in").write_text(entrada)
    (pasta / f"{nome}.out").write_text(saida)


def main() -> None:
    for nome, valores in CASOS_ETAPA1.items():
        soma, inicio, fim = e1.forca_bruta(valores)
        entrada = f"{len(valores)}\n{' '.join(map(str, valores))}\n"
        escrever(RAIZ / "etapa1", nome, entrada, f"{soma} {inicio + 1} {fim + 1}\n")

    for nome, pontos in CASOS_ETAPA2.items():
        d2, i, j = e2.forca_bruta(pontos)
        entrada = f"{len(pontos)}\n" + "".join(f"{x} {y}\n" for x, y in pontos)
        escrever(RAIZ / "etapa2", nome, entrada, f"{math.sqrt(d2):.6f} {i + 1} {j + 1}\n")

    print(f"{len(CASOS_ETAPA1)} casos da etapa 1 e {len(CASOS_ETAPA2)} da etapa 2 gerados.")


if __name__ == "__main__":
    main()
