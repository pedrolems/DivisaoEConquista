"""Executa os programas sobre cada Casos/etapaX/*.in e compara com o .out.

Uso: python Casos/rodar_casos.py

Na etapa 1 a comparação é exata (soma, início e fim), pois a regra de
desempate é a mesma em todas as versões. Na etapa 2 a distância precisa
ser igual à esperada e o par devolvido precisa ter exatamente essa
distância, já que em empates as versões podem escolher pares diferentes.
"""

import math
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PROGRAMA1 = RAIZ.parent / "EtapaUm" / "Sub_Soma_Max.py"
PROGRAMA2 = RAIZ.parent / "EtapaDois" / "Par_Pontos_Prox.py"


def executar(programa: Path, algoritmo: str, entrada: str) -> str:
    resultado = subprocess.run(
        [sys.executable, str(programa), algoritmo],
        input=entrada, capture_output=True, text=True, check=True,
    )
    return resultado.stdout.strip()


def conferir_etapa2(entrada: str, obtido: str, esperado: str) -> bool:
    d_obt, i, j = obtido.split()
    d_esp = esperado.split()[0]
    if d_obt != d_esp:
        return False
    partes = entrada.split()
    coord = [float(v) for v in partes[1:]]
    i, j = int(i) - 1, int(j) - 1
    if not i < j:
        return False
    d = math.hypot(coord[2 * i] - coord[2 * j], coord[2 * i + 1] - coord[2 * j + 1])
    return f"{d:.6f}" == d_esp


def main() -> int:
    falhas = total = 0
    for etapa, programa, algoritmos in (
        ("etapa1", PROGRAMA1, ("fb", "dc", "kadane")),
        ("etapa2", PROGRAMA2, ("fb", "dc")),
    ):
        for caso in sorted((RAIZ / etapa).glob("*.in")):
            entrada = caso.read_text()
            esperado = caso.with_suffix(".out").read_text().strip()
            for algoritmo in algoritmos:
                total += 1
                obtido = executar(programa, algoritmo, entrada)
                if etapa == "etapa1":
                    ok = obtido == esperado
                else:
                    ok = conferir_etapa2(entrada, obtido, esperado)
                if not ok:
                    falhas += 1
                    print(f"FALHOU {etapa}/{caso.stem} [{algoritmo}]: "
                          f"esperado '{esperado}', obtido '{obtido}'")
    print(f"{total - falhas}/{total} execuções corretas.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
