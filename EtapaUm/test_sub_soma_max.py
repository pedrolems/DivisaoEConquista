"""Testes da Etapa 1. Executar com: python -m unittest -v (dentro de EtapaUm)."""

import random
import unittest

from Sub_Soma_Max import divisao_e_conquista, forca_bruta, kadane, ler_entrada

ALGORITMOS = (forca_bruta, divisao_e_conquista, kadane)


class TestSubarranjoSomaMaxima(unittest.TestCase):
    def verificar(self, dados, esperado):
        for algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=algoritmo.__name__):
                self.assertEqual(algoritmo(dados), esperado)

    # --- casos de borda pedidos no enunciado ---------------------------------

    def test_apenas_negativos(self):
        """Não existe intervalo com soma positiva: a resposta é o maior
        elemento isolado, nunca 0 ou um intervalo vazio."""
        self.verificar([-8, -2, -5], (-2, 1, 1))

    def test_apenas_negativos_maximo_no_fim(self):
        """Mesmo caso, mas com o maior negativo na última posição, para
        pegar erros de inicialização que só olham o começo do vetor."""
        self.verificar([-9, -7, -3], (-3, 2, 2))

    def test_tamanho_um(self):
        """Caso base da recursão: esquerda == direita."""
        self.verificar([7], (7, 0, 0))

    def test_tamanho_um_negativo(self):
        """Tamanho 1 com valor negativo: a soma pode ser negativa."""
        self.verificar([-4], (-4, 0, 0))

    def test_empate_escolhe_inicio_mais_cedo(self):
        """[3], [3,-3,3] e [3] (no fim) somam 3. Fica o que começa antes
        e, entre os que começam no índice 0, o mais curto."""
        self.verificar([3, -3, 3], (3, 0, 0))

    def test_empate_entre_metades(self):
        """Os intervalos empatados ficam um em cada metade do vetor, então
        a escolha acontece na combinação da divisão e conquista."""
        self.verificar([5, -10, 1, 4], (5, 0, 0))

    def test_empate_mesmo_inicio_escolhe_mais_curto(self):
        """[2] e [2, 0] somam 2 e começam no mesmo dia."""
        self.verificar([2, 0, -1], (2, 0, 0))

    # --- outros casos ----------------------------------------------------------

    def test_apenas_zeros(self):
        """Todos os intervalos empatam em 0; fica o primeiro elemento."""
        self.verificar([0, 0, 0], (0, 0, 0))

    def test_zero_entre_negativos(self):
        """O zero é melhor que qualquer negativo."""
        self.verificar([-1, 0, -2], (0, 1, 1))

    def test_apenas_positivos(self):
        """A resposta é o vetor inteiro."""
        self.verificar([1, 2, 3, 4], (10, 0, 3))

    def test_exemplo_classico(self):
        """Exemplo do CLRS: resposta no meio, cruzando a divisão."""
        self.verificar([-2, 1, -3, 4, -1, 2, 1, -5, 4], (6, 3, 6))

    def test_maximo_no_inicio(self):
        self.verificar([10, -20, 1, 2], (10, 0, 0))

    def test_maximo_no_fim(self):
        self.verificar([1, -20, 3, 9], (12, 2, 3))

    def test_cruza_exatamente_o_meio(self):
        """O melhor intervalo é [meio, meio+1] e nenhum dos lados sozinho."""
        self.verificar([-5, -5, 4, 4, -5, -5], (8, 2, 3))

    def test_tamanho_dois(self):
        self.verificar([-1, 2], (2, 1, 1))
        self.verificar([2, -1], (2, 0, 0))

    def test_valores_grandes(self):
        """Somas acima de 32 bits (Python não estoura, mas fica registrado)."""
        self.verificar([2_000_000_000, 2_000_000_000, -1], (4_000_000_000, 0, 1))

    def test_rejeita_vetor_vazio(self):
        for algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=algoritmo.__name__):
                with self.assertRaises(ValueError):
                    algoritmo([])

    # --- entrada ---------------------------------------------------------------

    def test_ler_entrada_com_quebras_de_linha(self):
        self.assertEqual(ler_entrada("3\n1\n-2\n3\n"), [1, -2, 3])

    def test_ler_entrada_n_incompativel(self):
        with self.assertRaises(ValueError):
            ler_entrada("3 1 2")
        with self.assertRaises(ValueError):
            ler_entrada("0")

    # --- comparação aleatória ----------------------------------------------------

    def test_aleatorio_contra_forca_bruta(self):
        """3000 vetores pequenos com valores em [-5, 5]. A faixa pequena gera
        muitos empates, que é onde as versões costumam divergir."""
        gerador = random.Random(2026)
        for _ in range(3000):
            n = gerador.randint(1, 25)
            dados = [gerador.randint(-5, 5) for _ in range(n)]
            esperado = forca_bruta(dados)
            self.assertEqual(divisao_e_conquista(dados), esperado, dados)
            self.assertEqual(kadane(dados), esperado, dados)


if __name__ == "__main__":
    unittest.main()
