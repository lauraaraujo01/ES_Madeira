from shapely import wkt
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon

# Carregar os dados
df = pd.read_csv("Madeira-Moodle-1.1.csv", sep=";")
print(df.head())  # Verifique o conteúdo dos dados carregados

# Função para verificar adjacência com critério de distância
def adjacente(row1, row2, limite_distancia=0.1):
    try:
        # Convertendo WKT para objetos geométricos
        geom1 = wkt.loads(row1['geometry'])
        geom2 = wkt.loads(row2['geometry'])
        
        # Verificar se as geometrias estão suficientemente próximas
        return geom1.distance(geom2) < limite_distancia  # Verifica se a distância entre as geometrias é menor que o limite
    except Exception as e:
        print(f"Erro ao converter geometria: {e}")
        return False

# Criar o grafo
G = nx.Graph()

# Adicionar nós (propriedades) ao grafo
for index, row in df.iterrows():
    G.add_node(row['PAR_ID'], area=row['Shape_Area'], freguesia=row['Freguesia'])

# Adicionar arestas ponderadas (propriedades adjacentes)
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i != j and adjacente(row1, row2):
            weight = abs(row1['Shape_Area'] - row2['Shape_Area'])  # Exemplo de ponderação
            G.add_edge(row1['PAR_ID'], row2['PAR_ID'], weight=weight)

# Verificar o grafo
print(f"Nós no grafo: {G.nodes()}")
print(f"Arestas no grafo: {G.edges()}")

# Se o grafo tiver arestas, ele será visualizado
if G.number_of_edges() > 0:
    nx.draw(G, with_labels=True, node_size=500, font_size=8)
    plt.show()
else:
    print("O grafo não tem arestas. Verifique as geometrias ou os critérios de adjacência.")

# **Visualizar as geometrias para depuração**:
# Visualize algumas geometrias para garantir que estão sendo lidas corretamente

for index, row in df.iterrows():
    geom = wkt.loads(row['geometry'])
    plt.figure()
    
    if isinstance(geom, MultiPolygon):
        for polygon in geom:
            x, y = polygon.exterior.xy
            plt.fill(x, y, alpha=0.5, fc='r', edgecolor='black')
    else:
        x, y = geom.exterior.xy
        plt.fill(x, y, alpha=0.5, fc='r', edgecolor='black')

    plt.title(f"Propriedade {row['PAR_ID']}")
    plt.show()