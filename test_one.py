class Grafo:
    def __init__(self, propiedades,):
        self.vertices = propiedades
        self.grafo = [[] for i in range(self.vertices)]

    def load_dataset(self, dataset):
        # Implementar a lógica para carregar o dataset
        pass


    def adicionar_aresta(self, u, v,):
        self.grafo[u].append((v))
        self.grafo[v].append((u))

    def show_list(self):
        for i in range(self.vertices):
            print(f'{i}: {self.grafo[i]}')


if __name__ == '__main__':
    grafo = Grafo(5)
    grafo.adicionar_aresta(0, 1)
    grafo.adicionar_aresta(0, 2)
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(2, 4)
    grafo.show_list()