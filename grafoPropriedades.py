import csv
from collections import defaultdict
from itertools import combinations

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


if __name__ == "__main__":
    # Apenas executa isto se correr o ficheiro diretamente (não quando fizer import nos testes)
    dados_csv = ler_csv("Madeira-Moodle-1.1.csv")
    grafo = construir_grafo_propriedades(dados_csv)

    for propriedade, vizinhas in grafo.items():
        print(f"Propriedade {propriedade} tem as vizinhas: {', '.join(vizinhas)}")
