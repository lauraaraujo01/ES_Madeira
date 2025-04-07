import csv
from collections import defaultdict
from itertools import combinations

# Armazenamento
propriedade_para_dono = {}
freguesia_para_propriedades = defaultdict(list)

# Leitura do ficheiro CSV
with open("propriedades.csv", newline='', encoding="utf-8") as csvfile:
    leitor = csv.DictReader(csvfile, delimiter=';')
    for linha in leitor:
        par_id = linha['PAR_ID']
        dono = linha['OWNER']
        freguesia = linha['Freguesia']

        propriedade_para_dono[par_id] = dono
        freguesia_para_propriedades[freguesia].append(par_id)