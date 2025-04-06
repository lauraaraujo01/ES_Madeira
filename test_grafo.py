import unittest
from test_one import Grafo

class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.g = Grafo(5)
        self.g.adicionar_aresta(0, 1)
        self.g.adicionar_aresta(0, 2)
        self.g.adicionar_aresta(1, 2)
        self.g.adicionar_aresta(1, 3)
        self.g.adicionar_aresta(2, 4)

    def test_numero_de_vertices(self):
        self.assertEqual(self.g.vertices, 5)

    def test_adicionar_aresta(self):
        # Verifica se as arestas foram corretamente adicionadas
        self.assertIn(1, self.g.grafo[0])
        self.assertIn(2, self.g.grafo[0])
        self.assertIn(0, self.g.grafo[1])
        self.assertIn(3, self.g.grafo[1])
        self.assertIn(4, self.g.grafo[2])

    def test_grafo_bidirecional(self):
        # Verifica se o grafo é bidirecional
        self.assertIn(0, self.g.grafo[1])
        self.assertIn(1, self.g.grafo[2])
        self.assertIn(2, self.g.grafo[4])

if __name__ == '__main__':
    unittest.main()