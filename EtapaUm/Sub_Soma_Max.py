"""Subarranjo de soma máxima por força bruta e divisão e conquista."""

from typing import Sequence, Tuple

Resultado = Tuple[int, int, int]  # (soma, inicio, fim), índices internos 0-based


def _melhor(a: Resultado, b: Resultado) -> Resultado:
    """Escolhe maior soma; em empate, menor início e depois menor fim."""
    if a[0] != b[0]:
        return a if a[0] > b[0] else b
    if a[1] != b[1]:
        return a if a[1] < b[1] else b
    return a if a[2] <= b[2] else b


def forca_bruta(valores: Sequence[int]) -> Resultado:
    """Testa todos os intervalos não vazios em O(n²)."""
    if not valores:
        raise ValueError("A sequência deve conter pelo menos um valor.")

    melhor = (valores[0], 0, 0)
    for inicio in range(len(valores)):
        soma = 0
        for fim in range(inicio, len(valores)):
            soma += valores[fim]
            melhor = _melhor(melhor, (soma, inicio, fim))
    return melhor


def _cruzando(valores: Sequence[int], esquerda: int, meio: int, direita: int) -> Resultado:
    """Calcula em O(n) o melhor intervalo que inclui meio e meio+1."""
    soma = 0
    melhor_esquerda = (float("-inf"), esquerda, meio)
    for i in range(meio, esquerda - 1, -1):
        soma += valores[i]
        melhor_esquerda = _melhor(melhor_esquerda, (soma, i, meio))

    soma = 0
    melhor_direita = (float("-inf"), meio + 1, direita)
    for i in range(meio + 1, direita + 1):
        soma += valores[i]
        melhor_direita = _melhor(melhor_direita, (soma, meio + 1, i))

    return (
        melhor_esquerda[0] + melhor_direita[0],
        melhor_esquerda[1],
        melhor_direita[2],
    )


def divisao_e_conquista(valores: Sequence[int]) -> Resultado:
       """O(n). Em empate, estende o intervalo atual (início mais cedo)."""
       if not valores:
           raise ValueError("A sequência deve conter pelo menos um valor.")
       atual, inicio = 0, 0
       melhor = (valores[0], 0, 0)
       for i, x in enumerate(valores):
           if atual < 0:          # só reinicia se for estritamente negativo
               atual, inicio = 0, i
           atual += x
           melhor = _melhor(melhor, (atual, inicio, i))
       return melhor




def main() -> None:
    """Lê n e os n inteiros da entrada padrão e mostra os dois resultados."""
    import sys

    dados = list(map(int, sys.stdin.read().split()))
    if not dados:
        raise SystemExit("Entrada esperada: n seguido de n inteiros.")
    n, *valores = dados
    if n < 1 or len(valores) != n:
        raise SystemExit(f"Informe n >= 1 e exatamente {n} valores.")

    for nome, algoritmo in (
        ("Força bruta", forca_bruta),
        ("Divisão e conquista", divisao_e_conquista),
    ):
        soma, inicio, fim = algoritmo(valores)
        print(f"{nome}: soma máxima = {soma}; início = {inicio + 1}; fim = {fim + 1}")


if __name__ == "__main__":
    main()