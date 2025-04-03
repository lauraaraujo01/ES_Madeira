class Grafo:
    def __init__(self, propiedades,):
        self.vertices = propiedades
        self.grafo = [[] for i in range(self.vertices)]

    def adicionar_aresta(self, u, v,):
        self.grafo[u].append((v))
        self.grafo[v].append((u))

    def show_list(self):
        for i in range(self.vertices):
            print(f'{i}: {self.grafo[i]}')