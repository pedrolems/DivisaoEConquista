"""Subarranjo de soma máxima por força bruta, divisão e conquista e Kadane.

Uso:
    python Sub_Soma_Max.py [fb|dc|kadane] < entrada.txt

Entrada: n seguido de n inteiros (separados por espaço ou quebra de linha).
Saída:   uma linha "soma inicio fim", com índices começando em 1.

Regra de desempate (igual nas três versões): maior soma; em empate,
o intervalo que começa primeiro; persistindo o empate, o mais curto.
"""

import sys
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
    """Resolve recursivamente o problema em O(n log n).

    T(n) = 2T(n/2) + Θ(n)  =>  T(n) = Θ(n log n)
    """
    if not valores:
        raise ValueError("A sequência deve conter pelo menos um valor.")

    def resolver(esquerda: int, direita: int) -> Resultado:
        if esquerda == direita:
            return (valores[esquerda], esquerda, direita)

        meio = (esquerda + direita) // 2
        melhor_esquerda = resolver(esquerda, meio)
        melhor_direita = resolver(meio + 1, direita)
        melhor_cruzando = _cruzando(valores, esquerda, meio, direita)
        return _melhor(_melhor(melhor_esquerda, melhor_direita), melhor_cruzando)

    return resolver(0, len(valores) - 1)


def kadane(valores: Sequence[int]) -> Resultado:
    """Versão O(n) (questão desafio).

    Mantém a melhor soma de um intervalo que termina na posição atual.
    Só reinicia quando a soma acumulada fica estritamente negativa; com
    soma zero o intervalo é estendido, o que preserva o início mais cedo
    exigido pela regra de desempate.
    """
    if not valores:
        raise ValueError("A sequência deve conter pelo menos um valor.")

    atual, inicio = 0, 0
    melhor = (valores[0], 0, 0)
    for i, x in enumerate(valores):
        if atual < 0:
            atual, inicio = 0, i
        atual += x
        melhor = _melhor(melhor, (atual, inicio, i))
    return melhor


ALGORITMOS = {
    "fb": forca_bruta,
    "dc": divisao_e_conquista,
    "kadane": kadane,
}


def ler_entrada(texto: str) -> list:
    """Converte o texto de entrada na lista de valores, validando n."""
    dados = list(map(int, texto.split()))
    if not dados:
        raise ValueError("Entrada esperada: n seguido de n inteiros.")
    n, *valores = dados
    if n < 1 or len(valores) != n:
        raise ValueError(f"Informe n >= 1 e exatamente {n} valores.")
    return valores


def main() -> None:
    nome = sys.argv[1] if len(sys.argv) > 1 else "dc"
    if nome not in ALGORITMOS:
        raise SystemExit(f"Algoritmo inválido: {nome}. Use: {', '.join(ALGORITMOS)}")
    try:
        valores = ler_entrada(sys.stdin.read())
    except ValueError as erro:
        raise SystemExit(str(erro))

    soma, inicio, fim = ALGORITMOS[nome](valores)
    print(soma, inicio + 1, fim + 1)


if __name__ == "__main__":
    main()
