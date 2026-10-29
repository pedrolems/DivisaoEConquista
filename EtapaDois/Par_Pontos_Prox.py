"""Par de pontos mais próximos por força bruta e divisão e conquista.

Uso:
    python Par_Pontos_Prox.py [fb|dc] [limiar] < entrada.txt

Entrada: n seguido de n pares "x y" (inteiros ou reais).
Saída:   uma linha "distancia i j", com a distância em 6 casas decimais
         e os índices (começando em 1) das duas estações, com i < j.

Se houver mais de um par com a mesma distância mínima, qualquer um deles
é uma resposta válida; a distância é sempre a mesma.

As distâncias são comparadas ao quadrado, sem raiz, para que coordenadas
inteiras sejam comparadas de forma exata.
"""

import math
import sys
from typing import List, Sequence, Tuple

Ponto = Tuple[float, float]
Resultado = Tuple[float, int, int]  # (distância ao quadrado, i, j), índices 0-based

INFINITO = float("inf")

# Abaixo deste tamanho a recursão passa para a força bruta.
# Valor escolhido a partir de Experimentos/limiar.csv (ver relatório).
LIMIAR_PADRAO = 16


def _dist2(p: Ponto, q: Ponto) -> float:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def _ordenar_par(d2: float, i: int, j: int) -> Resultado:
    return (d2, i, j) if i < j else (d2, j, i)


def forca_bruta(pontos: Sequence[Ponto]) -> Resultado:
    """Compara todos os pares em O(n²)."""
    if len(pontos) < 2:
        raise ValueError("São necessários pelo menos dois pontos.")
    return _forca_bruta_indices(pontos, range(len(pontos)))


def _forca_bruta_indices(pontos: Sequence[Ponto], indices: Sequence[int]) -> Resultado:
    melhor = (INFINITO, -1, -1)
    for a in range(len(indices)):
        p = pontos[indices[a]]
        for b in range(a + 1, len(indices)):
            d2 = _dist2(p, pontos[indices[b]])
            if d2 < melhor[0]:
                melhor = _ordenar_par(d2, indices[a], indices[b])
    return melhor


def divisao_e_conquista(pontos: Sequence[Ponto], limiar: int = LIMIAR_PADRAO) -> Resultado:
    """Resolve em O(n log n).

    T(n) = 2T(n/2) + Θ(n)  =>  T(n) = Θ(n log n)
    (as duas ordenações iniciais custam O(n log n) e são feitas uma vez).
    """
    if len(pontos) < 2:
        raise ValueError("São necessários pelo menos dois pontos.")
    if limiar < 1:
        raise ValueError("O limiar deve ser pelo menos 1.")

    n = len(pontos)
    px = sorted(range(n), key=lambda i: (pontos[i][0], pontos[i][1]))
    py = sorted(range(n), key=lambda i: (pontos[i][1], pontos[i][0]))
    na_esquerda = bytearray(n)

    def resolver(px: List[int], py: List[int]) -> Resultado:
        tamanho = len(px)
        if tamanho <= limiar:
            return _forca_bruta_indices(pontos, px)

        meio = tamanho // 2
        x_linha = pontos[px[meio]][0]

        # Separa py em esquerda e direita mantendo a ordem por y, em O(n).
        for i in px[:meio]:
            na_esquerda[i] = 1
        py_esq = [i for i in py if na_esquerda[i]]
        py_dir = [i for i in py if not na_esquerda[i]]
        for i in px[:meio]:
            na_esquerda[i] = 0

        melhor = min(resolver(px[:meio], py_esq), resolver(px[meio:], py_dir))
        delta2 = melhor[0]

        # Faixa de largura 2δ em torno da linha, já ordenada por y.
        faixa = [i for i in py if (pontos[i][0] - x_linha) ** 2 < delta2]

        for a in range(len(faixa)):
            p = pontos[faixa[a]]
            # No máximo 7 vizinhos seguintes (justificativa no relatório).
            for b in range(a + 1, min(a + 8, len(faixa))):
                q = pontos[faixa[b]]
                if (q[1] - p[1]) ** 2 >= delta2:
                    break
                d2 = _dist2(p, q)
                if d2 < delta2:
                    melhor = _ordenar_par(d2, faixa[a], faixa[b])
                    delta2 = d2
        return melhor

    return resolver(px, py)


def ler_entrada(texto: str) -> List[Ponto]:
    """Converte o texto de entrada na lista de pontos, validando n."""
    partes = texto.split()
    if not partes:
        raise ValueError("Entrada esperada: n seguido de n pares x y.")
    n = int(partes[0])
    numeros = [float(v) if any(c in v for c in ".eE") else int(v) for v in partes[1:]]
    if n < 2 or len(numeros) != 2 * n:
        raise ValueError(f"Informe n >= 2 e exatamente {n} pares de coordenadas.")
    return [(numeros[2 * k], numeros[2 * k + 1]) for k in range(n)]


def main() -> None:
    nome = sys.argv[1] if len(sys.argv) > 1 else "dc"
    if nome not in ("fb", "dc"):
        raise SystemExit(f"Algoritmo inválido: {nome}. Use: fb, dc")
    try:
        pontos = ler_entrada(sys.stdin.read())
    except ValueError as erro:
        raise SystemExit(str(erro))

    if nome == "fb":
        d2, i, j = forca_bruta(pontos)
    else:
        limiar = int(sys.argv[2]) if len(sys.argv) > 2 else LIMIAR_PADRAO
        d2, i, j = divisao_e_conquista(pontos, limiar)
    print(f"{math.sqrt(d2):.6f} {i + 1} {j + 1}")


if __name__ == "__main__":
    main()
