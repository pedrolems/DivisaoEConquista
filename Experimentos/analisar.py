"""Lê os CSVs brutos, calcula médias e gera tabelas e gráficos.

Uso: python Experimentos/analisar.py   (depois de medir.py)

Gera em Experimentos/graficos/ as figuras usadas no relatório e em
Experimentos/tabelas.md as tabelas de médias.
"""

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parent
GRAFICOS = RAIZ / "graficos"

NOMES = {
    "forca_bruta": "Força bruta",
    "divisao_e_conquista": "Divisão e conquista",
    "kadane": "Kadane",
    "dc_sem_limiar": "D&C sem limiar",
}
CORES = {
    "forca_bruta": "#c0392b",
    "divisao_e_conquista": "#2471a3",
    "kadane": "#1e8449",
    "dc_sem_limiar": "#2471a3",
}
PREVISTO = {
    "forca_bruta": ("n²", lambda n: n * n),
    "divisao_e_conquista": ("n log n", lambda n: n * math.log2(n)),
    "kadane": ("n", lambda n: n),
}


def ler(nome: str) -> list:
    with open(RAIZ / nome, newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def agrupar(linhas: list, *chaves: str) -> dict:
    grupos = defaultdict(list)
    for linha in linhas:
        grupos[tuple(linha[c] for c in chaves)].append(float(linha["tempo_s"]))
    return grupos


def expoente(ns: list, tempos: list) -> float:
    """Inclinação da reta de mínimos quadrados em escala log-log."""
    xs = [math.log(n) for n in ns]
    ys = [math.log(t) for t in tempos]
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def formatar_ms(t: float) -> str:
    return f"{t * 1000:.3f}"


def main() -> None:
    GRAFICOS.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size": 10, "figure.dpi": 150})
    texto = []

    # --- medições principais ----------------------------------------------------
    medicoes = agrupar(ler("medicoes.csv"), "etapa", "algoritmo", "n")
    series = defaultdict(dict)
    for (etapa, algoritmo, n), tempos in medicoes.items():
        series[(etapa, algoritmo)][int(n)] = tempos

    for etapa, titulo in (("etapa1", "Etapa 1 — subarranjo de soma máxima"),
                          ("etapa2", "Etapa 2 — par de pontos mais próximos")):
        ordem = list(PREVISTO)
        algoritmos = sorted({a for (e, a) in series if e == etapa}, key=ordem.index)
        ns = sorted(series[(etapa, algoritmos[0])])

        texto.append(f"## {titulo}\n")
        cabecalho = "| n | " + " | ".join(f"{NOMES[a]} (ms)" for a in algoritmos) + " |"
        texto.append(cabecalho)
        texto.append("|" + "---|" * (len(algoritmos) + 1))
        for n in ns:
            celulas = []
            for a in algoritmos:
                tempos = series[(etapa, a)][n]
                celulas.append(f"{formatar_ms(statistics.fmean(tempos))} "
                               f"± {formatar_ms(statistics.stdev(tempos))}")
            texto.append(f"| {n} | " + " | ".join(celulas) + " |")
        texto.append("")
        for a in algoritmos:
            medias = [statistics.fmean(series[(etapa, a)][n]) for n in ns]
            texto.append(f"- Expoente ajustado ({NOMES[a]}): {expoente(ns, medias):.2f}")
        for a in algoritmos:
            if a == "forca_bruta":
                continue
            fb = statistics.fmean(series[(etapa, "forca_bruta")][ns[-1]])
            outro = statistics.fmean(series[(etapa, a)][ns[-1]])
            texto.append(f"- Aceleração em n = {ns[-1]} ({NOMES[a]} sobre força bruta): "
                         f"{fb / outro:.0f}x")
        texto.append("")

        # Tempo x n em escala log-log.
        fig, eixo = plt.subplots(figsize=(6, 3.8))
        for a in algoritmos:
            medias = [statistics.fmean(series[(etapa, a)][n]) for n in ns]
            desvios = [statistics.stdev(series[(etapa, a)][n]) for n in ns]
            eixo.errorbar(ns, medias, yerr=desvios, marker="o", ms=4, capsize=3,
                          color=CORES[a], label=NOMES[a])
        eixo.set_xscale("log", base=2)
        eixo.set_yscale("log")
        eixo.set_xlabel("n")
        eixo.set_ylabel("tempo médio (s)")
        eixo.set_title(titulo)
        eixo.grid(True, which="both", alpha=0.3)
        eixo.legend()
        fig.tight_layout()
        fig.savefig(GRAFICOS / f"{etapa}_tempos.png")
        plt.close(fig)

        # Tempo dividido pela complexidade prevista: deve ficar quase constante.
        fig, eixo = plt.subplots(figsize=(6, 3.4))
        for a in algoritmos:
            rotulo, f = PREVISTO[a]
            razoes = [statistics.fmean(series[(etapa, a)][n]) / f(n) for n in ns]
            base = razoes[-1]
            eixo.plot(ns, [r / base for r in razoes], marker="o", ms=4,
                      color=CORES[a], label=f"{NOMES[a]}: t / {rotulo}")
        eixo.axhline(1, color="gray", lw=0.8, ls="--")
        eixo.set_xscale("log", base=2)
        eixo.set_ylim(0, 2.5)
        eixo.set_xlabel("n")
        eixo.set_ylabel("razão normalizada (n = 6400 → 1)")
        eixo.set_title(f"{titulo.split(' —')[0]}: tempo / complexidade prevista")
        eixo.grid(True, alpha=0.3)
        eixo.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(GRAFICOS / f"{etapa}_razao.png")
        plt.close(fig)

    # --- limiar ------------------------------------------------------------------
    limiar = agrupar(ler("limiar.csv"), "n", "limiar")
    texto.append("## Limiar da etapa 2\n")
    texto.append("| limiar | n = 1600 (ms) | n = 6400 (ms) |")
    texto.append("|---|---|---|")
    limiares = sorted({int(l) for (_, l) in limiar})
    for l in limiares:
        celulas = [formatar_ms(statistics.fmean(limiar[(str(n), str(l))])) for n in (1600, 6400)]
        texto.append(f"| {l} | " + " | ".join(celulas) + " |")
    texto.append("")
    fig, eixo = plt.subplots(figsize=(6, 3.4))
    for n, cor in ((1600, "#7d3c98"), (6400, "#2471a3")):
        medias = [statistics.fmean(limiar[(str(n), str(l))]) for l in limiares]
        melhor = min(medias)
        eixo.plot(limiares, [m / melhor for m in medias], marker="o", ms=4,
                  color=cor, label=f"n = {n}")
    eixo.set_xscale("log", base=2)
    eixo.set_xlabel("limiar (tamanho abaixo do qual usa força bruta)")
    eixo.set_ylabel("tempo / menor tempo")
    eixo.set_title("Etapa 2: efeito do limiar na divisão e conquista")
    eixo.grid(True, which="both", alpha=0.3)
    eixo.legend()
    fig.tight_layout()
    fig.savefig(GRAFICOS / "etapa2_limiar.png")
    plt.close(fig)

    # --- tamanhos pequenos -------------------------------------------------------------
    pequenos = agrupar(ler("pequenos.csv"), "etapa", "algoritmo", "n")
    fig, eixos = plt.subplots(1, 2, figsize=(7, 3.2))
    texto.append("## Tamanhos pequenos (µs por execução)\n")
    for eixo, etapa, titulo in ((eixos[0], "etapa1", "Etapa 1"), (eixos[1], "etapa2", "Etapa 2")):
        algoritmos = sorted({a for (e, a, _) in pequenos if e == etapa})
        ns = sorted({int(n) for (e, _, n) in pequenos if e == etapa})
        texto.append(f"### {titulo}\n")
        texto.append("| n | " + " | ".join(NOMES[a] for a in algoritmos) + " |")
        texto.append("|" + "---|" * (len(algoritmos) + 1))
        for n in ns:
            texto.append(f"| {n} | " + " | ".join(
                f"{statistics.fmean(pequenos[(etapa, a, str(n))]) * 1e6:.1f}"
                for a in algoritmos) + " |")
        texto.append("")
        for a in algoritmos:
            medias = [statistics.fmean(pequenos[(etapa, a, str(n))]) * 1e6 for n in ns]
            eixo.plot(ns, medias, marker="o", ms=4, color=CORES[a], label=NOMES[a])
        eixo.set_xscale("log", base=2)
        eixo.set_yscale("log")
        eixo.set_xlabel("n")
        eixo.set_ylabel("tempo médio (µs)")
        eixo.set_title(titulo)
        eixo.grid(True, which="both", alpha=0.3)
        eixo.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "pequenos.png")
    plt.close(fig)

    (RAIZ / "tabelas.md").write_text("# Médias das medições\n\n" + "\n".join(texto) + "\n")
    print("\n".join(texto))


if __name__ == "__main__":
    main()
