import csv
from collections import defaultdict
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

def construir_grafo_propriedades(dados_csv):
    propriedade_para_dono = {}
    freguesia_para_propriedades = defaultdict(list)

    # Agrupar os dados
    for linha in dados_csv:
        par_id = linha["PAR_ID"]
        freguesia = linha["Freguesia"]
        propriedade_para_dono[par_id] = linha["OWNER"]
        freguesia_para_propriedades[freguesia].append(par_id)

    grafo_propriedades = defaultdict(set)

    for propriedades in freguesia_para_propriedades.values():
        for prop1, prop2 in combinations(propriedades, 2):
            grafo_propriedades[prop1].add(prop2)
            grafo_propriedades[prop2].add(prop1)

    return grafo_propriedades

def ler_csv(caminho_ficheiro):
    with open(caminho_ficheiro, newline='', encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        return list(leitor)

def desenhar_grafo(grafo):
    G = nx.Graph()
    for prop, vizinhas in grafo.items():
        for vizinha in vizinhas:
            G.add_edge(prop, vizinha)

    pos = nx.spring_layout(G, seed=42, k=0.5)

    fig, ax = plt.subplots(figsize=(20, 12))
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color='lightgreen',
        edgecolors='black',
        node_size=700,
        linewidths=1.2
    )
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color='gray',
        width=1,
        alpha=0.4
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        font_size=8,
        font_color='black'
    )

    ax.set_title("Grafo de Adjacência entre Propriedades", fontsize=16)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    dados_csv = ler_csv("Madeira-Moodle-1.2.csv")
    grafo = construir_grafo_propriedades(dados_csv)

    for propriedade, vizinhas in grafo.items():
        print(f"Propriedade {propriedade} tem as vizinhas: {', '.join(vizinhas)}")

    desenhar_grafo(grafo)
