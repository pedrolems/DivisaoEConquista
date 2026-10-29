"""Testes da Etapa 2. Executar com: python -m unittest -v (dentro de EtapaDois)."""

import random
import unittest

from Par_Pontos_Prox import _dist2, divisao_e_conquista, forca_bruta, ler_entrada

# Limiares testados: 1 força a recursão até o fim (testa a faixa em todos os
# níveis); 3 e 16 testam o caso base híbrido.
LIMIARES = (1, 3, 16)


class TestParPontosMaisProximos(unittest.TestCase):
    def verificar(self, pontos, d2_esperado, par_esperado=None):
        """Confere a distância em todas as versões. O par só é conferido
        quando ele é único; em empates basta ter a distância mínima."""
        resultados = [("fb", forca_bruta(pontos))]
        resultados += [(f"dc/{l}", divisao_e_conquista(pontos, l)) for l in LIMIARES]
        for nome, (d2, i, j) in resultados:
            with self.subTest(algoritmo=nome):
                self.assertEqual(d2, d2_esperado)
                self.assertLess(i, j)
                self.assertEqual(_dist2(pontos[i], pontos[j]), d2)
                if par_esperado is not None:
                    self.assertEqual((i, j), par_esperado)

    def test_dois_pontos(self):
        """Menor entrada válida."""
        self.verificar([(0, 0), (3, 4)], 25, (0, 1))

    def test_tres_pontos(self):
        """Tamanho ímpar: as metades ficam com 1 e 2 pontos."""
        self.verificar([(0, 0), (10, 10), (11, 10)], 1, (1, 2))

    def test_par_cruza_a_linha_divisoria(self):
        """Cada lado isolado tem distância 10, mas o par mais próximo tem um
        ponto de cada lado. Só a verificação da faixa encontra a resposta."""
        pontos = [(0, 0), (0, 10), (4, 5), (5, 5), (9, 0), (9, 10)]
        self.verificar(pontos, 1, (2, 3))

    def test_pontos_repetidos(self):
        """Duas estações na mesma posição: distância 0."""
        self.verificar([(1, 1), (5, 5), (9, 9), (5, 5)], 0, (1, 3))

    def test_todos_com_mesmo_x(self):
        """Todos os pontos sobre a mesma reta vertical. A divisão pela
        mediana de x precisa funcionar mesmo com x repetido."""
        pontos = [(2, y) for y in (0, 7, 15, 16, 30, 50)]
        self.verificar(pontos, 1, (2, 3))

    def test_todos_com_mesmo_y(self):
        """Pontos na mesma reta horizontal: a faixa por y é degenerada."""
        pontos = [(x, 4) for x in (0, 9, 20, 22, 40)]
        self.verificar(pontos, 4, (2, 3))

    def test_coordenadas_negativas(self):
        self.verificar([(-5, -5), (-1, -2), (3, 3), (10, -7)], 25, (0, 1))

    def test_coordenadas_reais(self):
        pontos = [(0.5, 0.5), (0.6, 0.5), (3.0, 3.0)]
        d2, i, j = divisao_e_conquista(pontos, 1)
        self.assertAlmostEqual(d2, 0.01)
        self.assertEqual((i, j), (0, 1))

    def test_empate_entre_pares(self):
        """Grade 3x3 com espaçamento 1: vários pares a distância 1. Qualquer
        um serve, desde que a distância seja a mínima."""
        pontos = [(x, y) for x in range(3) for y in range(3)]
        self.verificar(pontos, 1)

    def test_pior_caso_da_faixa(self):
        """Pontos concentrados perto da linha divisória, com distâncias
        quase iguais, forçando muitos pontos na faixa."""
        pontos = [(0, 2 * k) for k in range(20)] + [(1, 2 * k + 1) for k in range(20)]
        self.verificar(pontos, 2)

    def test_coordenadas_grandes(self):
        self.verificar([(10**9, 10**9), (-10**9, -10**9), (10**9, 10**9 - 3)], 9, (0, 2))

    def test_rejeita_menos_de_dois_pontos(self):
        for pontos in ([], [(1, 1)]):
            with self.assertRaises(ValueError):
                forca_bruta(pontos)
            with self.assertRaises(ValueError):
                divisao_e_conquista(pontos)

    def test_ler_entrada(self):
        self.assertEqual(ler_entrada("2\n0 0\n1.5 2\n"), [(0, 0), (1.5, 2)])
        with self.assertRaises(ValueError):
            ler_entrada("3 0 0 1 1")

    def test_aleatorio_contra_forca_bruta(self):
        """1500 conjuntos aleatórios. Coordenadas em faixa pequena geram
        muitos pontos repetidos e empates."""
        gerador = random.Random(2026)
        for _ in range(1500):
            n = gerador.randint(2, 60)
            faixa = gerador.choice((5, 50, 1000))
            pontos = [(gerador.randint(-faixa, faixa), gerador.randint(-faixa, faixa))
                      for _ in range(n)]
            esperado = forca_bruta(pontos)[0]
            for limiar in LIMIARES:
                self.assertEqual(divisao_e_conquista(pontos, limiar)[0], esperado, pontos)


if __name__ == "__main__":
    unittest.main()
