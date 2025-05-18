"""
Módulo GrafoProprietarios

Este módulo constrói e desenha um grafo que representa as relações de vizinhança entre proprietários
de terrenos rústicos, com base nos dados de cadastro fornecidos em formato CSV.

Funções:
- ler_csv(caminho): Lê os dados do ficheiro CSV.
- construir_grafo_proprietarios(dados_csv): Constrói o grafo de vizinhança entre proprietários.
- desenhar_grafo(grafo, mostrar): Desenha o grafo utilizando o matplotlib e networkx.
"""

import csv
from collections import defaultdict
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.path.append('dados')



def construir_grafo_proprietarios(dados_csv):
    """
    Constrói um grafo de vizinhança entre proprietários a partir dos dados do cadastro.

    Cada proprietário é um nó. Existe uma aresta entre dois proprietários se possuírem
    propriedades na mesma freguesia.

    :param dados_csv: Lista de dicionários com os dados lidos do ficheiro CSV.
    :return: Dicionário com os proprietários como chaves e conjuntos de vizinhos como valores.
    """
    propriedade_para_dono = {}
    freguesia_para_propriedades = defaultdict(list)

    for linha in dados_csv:
        par_id = linha['PAR_ID']
        dono = linha['OWNER']
        freguesia = linha['Freguesia']

        propriedade_para_dono[par_id] = dono
        freguesia_para_propriedades[freguesia].append(par_id)

    grafo_proprietarios = defaultdict(set)

    for propriedades in freguesia_para_propriedades.values():
        for prop1, prop2 in combinations(propriedades, 2):
            dono1 = propriedade_para_dono[prop1]
            dono2 = propriedade_para_dono[prop2]
            if dono1 != dono2:
                grafo_proprietarios[dono1].add(dono2)
                grafo_proprietarios[dono2].add(dono1)

    return grafo_proprietarios

def ler_csv(caminho):
    """
    Lê um ficheiro CSV com delimitador ';' e retorna uma lista de dicionários.

    :param caminho: Caminho para o ficheiro CSV.
    :return: Lista de dicionários representando cada linha.
    """
    with open(caminho, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=';'))

def desenhar_grafo(grafo, mostrar=True):
    """
    Desenha o grafo de vizinhança entre proprietários.

    :param grafo: Dicionário onde as chaves são IDs de proprietários e os valores são conjuntos de vizinhos.
    :param mostrar: Booleano. Se True, mostra o grafo na tela. Se False, apenas prepara a figura.
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.Graph()
    for dono, vizinhos in grafo.items():
        for vizinho in vizinhos:
            G.add_edge(dono, vizinho)

    pos = nx.spring_layout(G, seed=42, k=0.5)  # k controla o afastamento dos nós

    fig, ax = plt.subplots(figsize=(20, 12))  # aumenta o tamanho da figura

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color='skyblue',
        edgecolors='black',
        node_size=1000,
        linewidths=1.5
    )

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color='gray',
        alpha=0.3,
        width=1
    )

    nx.draw_networkx_labels(
        G,
        pos,
        ax=ax,
        font_size=8,
        font_color='black',
        font_weight='bold'
    )

    ax.set_title("Grafo de Vizinhança entre Proprietários", fontsize=16)
    ax.set_axis_off()
    plt.tight_layout()
    if mostrar:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    dados = ler_csv("Madeira-Moodle-1.2.csv")
    grafo = construir_grafo_proprietarios(dados)

  #  for dono, vizinhos in grafo.items():
   #     print(f"{dono}: {', '.join(vizinhos)}")

    desenhar_grafo(grafo)

