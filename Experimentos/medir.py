"""Mede o tempo de execução de todos os algoritmos e grava os CSVs brutos.

Uso: python Experimentos/medir.py

Arquivos gerados (uma linha por execução, sem médias):
    medicoes.csv  tamanhos 100, 200, ..., 6400 para todos os algoritmos
    limiar.csv    divisão e conquista da etapa 2 com limiares diferentes
    pequenos.csv  tamanhos pequenos, para achar onde a força bruta deixa de vencer
    maquina.txt   configuração da máquina usada
"""

import csv
import platform
import random
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ.parent / "EtapaUm"))
sys.path.insert(0, str(RAIZ.parent / "EtapaDois"))

import Par_Pontos_Prox as e2  # noqa: E402
import Sub_Soma_Max as e1  # noqa: E402

TAMANHOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICOES = 5
SEMENTE = 2026

ALGORITMOS = [
    ("etapa1", "forca_bruta", e1.forca_bruta),
    ("etapa1", "divisao_e_conquista", e1.divisao_e_conquista),
    ("etapa1", "kadane", e1.kadane),
    ("etapa2", "forca_bruta", e2.forca_bruta),
    ("etapa2", "divisao_e_conquista", e2.divisao_e_conquista),
]


def vetor(gerador: random.Random, n: int) -> list:
    return [gerador.randint(-1000, 1000) for _ in range(n)]


def pontos(gerador: random.Random, n: int) -> list:
    return [(gerador.randint(0, 10**6), gerador.randint(0, 10**6)) for _ in range(n)]


def cronometrar(funcao, *args) -> float:
    inicio = time.perf_counter()
    funcao(*args)
    return time.perf_counter() - inicio


def medir_principal() -> None:
    with open(RAIZ / "medicoes.csv", "w", newline="") as arquivo:
        saida = csv.writer(arquivo)
        saida.writerow(["etapa", "algoritmo", "n", "repeticao", "tempo_s"])
        for n in TAMANHOS:
            for rep in range(1, REPETICOES + 1):
                # A mesma entrada é usada por todos os algoritmos da etapa.
                gerador = random.Random(SEMENTE * 100_000 + n * 10 + rep)
                entradas = {"etapa1": vetor(gerador, n), "etapa2": pontos(gerador, n)}
                for etapa, nome, funcao in ALGORITMOS:
                    t = cronometrar(funcao, entradas[etapa])
                    saida.writerow([etapa, nome, n, rep, f"{t:.9f}"])
                arquivo.flush()
            print(f"  n = {n} concluído", flush=True)


def medir_limiar() -> None:
    limiares = [1, 2, 4, 8, 12, 16, 24, 32, 64, 128]
    with open(RAIZ / "limiar.csv", "w", newline="") as arquivo:
        saida = csv.writer(arquivo)
        saida.writerow(["n", "limiar", "repeticao", "tempo_s"])
        for n in (1600, 6400):
            for rep in range(1, REPETICOES + 1):
                entrada = pontos(random.Random(SEMENTE + n + rep), n)
                for limiar in limiares:
                    t = cronometrar(e2.divisao_e_conquista, entrada, limiar)
                    saida.writerow([n, limiar, rep, f"{t:.9f}"])


def medir_pequenos() -> None:
    """Para n pequeno uma execução dura microssegundos, então cada medição
    é o tempo médio de um lote de execuções sobre a mesma entrada."""
    lote = 200
    casos = [
        ("etapa1", "forca_bruta", e1.forca_bruta, vetor, {}),
        ("etapa1", "divisao_e_conquista", e1.divisao_e_conquista, vetor, {}),
        ("etapa2", "forca_bruta", e2.forca_bruta, pontos, {}),
        ("etapa2", "dc_sem_limiar", e2.divisao_e_conquista, pontos, {"limiar": 1}),
    ]
    with open(RAIZ / "pequenos.csv", "w", newline="") as arquivo:
        saida = csv.writer(arquivo)
        saida.writerow(["etapa", "algoritmo", "n", "repeticao", "tempo_s"])
        for n in (2, 4, 8, 16, 32, 64, 128, 256):
            for rep in range(1, REPETICOES + 1):
                gerador = random.Random(SEMENTE + 7 * n + rep)
                entradas = {"etapa1": vetor(gerador, n), "etapa2": pontos(gerador, n)}
                for etapa, nome, funcao, _, extra in casos:
                    inicio = time.perf_counter()
                    for _ in range(lote):
                        funcao(entradas[etapa], **extra)
                    t = (time.perf_counter() - inicio) / lote
                    saida.writerow([etapa, nome, n, rep, f"{t:.9f}"])


def registrar_maquina() -> None:
    linhas = [
        f"Sistema: {platform.platform()}",
        f"Python: {platform.python_implementation()} {platform.python_version()}",
    ]
    try:
        info = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
        for linha in info.splitlines():
            if linha.split(":")[0].strip() in ("Model name", "CPU(s)", "L2 cache", "L3 cache"):
                linhas.append(" ".join(linha.split()))
        memoria = open("/proc/meminfo").readline().split()[1]
        linhas.append(f"Memória: {int(memoria) / 1024**2:.1f} GiB")
    except (OSError, IndexError):
        linhas.append(f"Processador: {platform.processor()}")
    (RAIZ / "maquina.txt").write_text("\n".join(linhas) + "\n")


def main() -> None:
    registrar_maquina()
    print("Medindo tamanhos 100 a 6400...", flush=True)
    medir_principal()
    print("Medindo limiares...", flush=True)
    medir_limiar()
    print("Medindo tamanhos pequenos...", flush=True)
    medir_pequenos()
    print("Pronto.")


if __name__ == "__main__":
    main()
