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
        freguesia_para_propriedades[freguesia].append(par_id)


# Simulação de vizinhança: propriedades da mesma freguesia são vizinhas
grafo_proprietarios = defaultdict(set)

for propriedades in freguesia_para_propriedades.values():
    for prop1, prop2 in combinations(propriedades, 2):
        dono1 = propriedade_para_dono[prop1]
        dono2 = propriedade_para_dono[prop2]
        if dono1 != dono2:
            grafo_proprietarios[dono1].add(dono2)
            grafo_proprietarios[dono2].add(dono1)

# Exemplo de saída
for dono, vizinhos in grafo_proprietarios.items():
    print(f"{dono}: {', '.join(vizinhos)}")