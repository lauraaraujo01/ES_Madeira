import csv
from collections import defaultdict
from itertools import combinations

# Armazenamento
propriedade_para_dono = {}
freguesia_para_propriedades = defaultdict(list)

# Leitura do ficheiro CSV
with open("Madeira-Moodle-1.1.csv", newline='', encoding="utf-8") as csvfile:
    leitor = csv.DictReader(csvfile, delimiter=';')
    for linha in leitor:
        par_id = linha['PAR_ID']
        dono = linha['OWNER']
        freguesia = linha['Freguesia']

        propriedade_para_dono[par_id] = dono
# Agrupar propriedades por freguesia
        freguesia_para_propriedades[freguesia].append(par_id)

# Simulação de vizinhança: propriedades da mesma freguesia são vizinhas
grafo_propriedades = defaultdict(set)

for propriedades in freguesia_para_propriedades.values():
    # Para cada par de propriedades na mesma freguesia
    for prop1, prop2 in combinations(propriedades, 2):
        # Se as propriedades são diferentes, adicionamos uma aresta entre elas
        grafo_propriedades[prop1].add(prop2)
        grafo_propriedades[prop2].add(prop1)

# Exemplo de saída: Exibe as relações de adjacência entre as propriedades
for propriedade, vizinhas in grafo_propriedades.items():
    print(f"Propriedade {propriedade} tem as vizinhas: {', '.join(vizinhas)}")
