import csv
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt



def construir_grafo_propriedades(dados_csv):
    geometria_por_parcela = {}
    grafo = nx.Graph()

    # 1. Converter WKT → objeto geométrico Shapely
    for linha in dados_csv:
        par_id = linha["PAR_ID"]
        try:
            geom = linha["geometry"]
            geometria_por_parcela[par_id] = geom
            grafo.add_node(par_id)
        except Exception as e:
            print(f"Erro ao processar geometria da parcela {par_id}: {e}")

    # 2. Verificar adjacência real entre todas as geometrias
    lista_parcelas = list(geometria_por_parcela.items())
    for i in range(len(lista_parcelas)):
        id1, geom1 = lista_parcelas[i]
        for j in range(i + 1, len(lista_parcelas)):
            id2, geom2 = lista_parcelas[j]
            if geom1.intersects(geom2): 
                grafo.add_edge(id1, id2)

    # 3. Converter para defaultdict(set) para manter compatibilidade com desenhar_grafo
    grafo_dict = defaultdict(set)

    for a, b in grafo.edges:
        grafo_dict[a].add(b)
        grafo_dict[b].add(a)

    return grafo_dict

def ler_csv(caminho_ficheiro):
    with open(caminho_ficheiro, newline='', encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        return list(leitor)

def desenhar_grafo_propriedades(grafo, mostrar=True):
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
    if mostrar:
        plt.show()
    else:
        plt.close()

    return fig

if __name__ == "__main__":
    dados_csv = ler_csv("Madeira-Moodle-1.2.csv")
    grafo = construir_grafo_propriedades(dados_csv)

    #for propriedade, vizinhas in grafo.items():
     #   print(f"Propriedade {propriedade} tem as vizinhas: {', '.join(vizinhas)}")

    desenhar_grafo_propriedades(grafo)
