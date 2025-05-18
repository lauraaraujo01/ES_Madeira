from shapely.wkt import loads as load_wkt
from shapely.ops import unary_union
from collections import defaultdict, Counter
from copy import deepcopy
import csv
from grafoPropriedades import construir_grafo_propriedades
from areaMediaPropriedades5 import calcular_area_media


def ler_csv_propriedades(caminho_csv):
    propriedades = []
    with open(caminho_csv, newline='', encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=';')
        for linha in leitor:
            try:
                geometria = load_wkt(linha["geometry"])
                propriedades.append({
                    "PAR_ID": linha["PAR_ID"],
                    "OWNER": linha["OWNER"],
                    "Freguesia": linha["Freguesia"],
                    "geometry": geometria,
                    "area": geometria.area,
                    "perimetro": geometria.length
                })
            except Exception as e:
                print(f"Erro ao ler linha: {linha}\n{e}")
    return propriedades


def sugerir_trocas(propriedades, nivel_geografico, nome_escolhido):
    props = [
        p for p in propriedades
        if isinstance(p.get(nivel_geografico), str)
        and p[nivel_geografico].strip().lower() == nome_escolhido.strip().lower()
    ]

    # Remover donos com só uma propriedade (troca inútil)
    contagem = Counter(p["OWNER"] for p in props)
    props = [p for p in props if contagem[p["OWNER"]] > 1]

    sugestoes = []

    # Adicionar número de vizinhos (grafo de adjacência)
    grafo = construir_grafo_propriedades(props)
    for p in props:
        p["n_vizinhos"] = len(grafo.get(p["PAR_ID"], []))

    # Limita a análise a 100 propriedades
    props = sorted(props, key=lambda x: x["area"], reverse=True)[:40]
    for i in range(len(props)):
        for j in range(i + 1, len(props)):
            p1, p2 = props[i], props[j]
            if p1["OWNER"] == p2["OWNER"]:
                continue

            propriedades_trocadas = deepcopy(props)
            propriedades_trocadas[i] = {**p1, "OWNER": p2["OWNER"]}
            propriedades_trocadas[j] = {**p2, "OWNER": p1["OWNER"]}

            area_antes = calcular_area_media(props, nivel_geografico, nome_escolhido)
            area_depois = calcular_area_media(propriedades_trocadas, nivel_geografico, nome_escolhido)
            ganho = area_depois - area_antes

            # Ignorar trocas com ganho irrelevante
            if abs(ganho) < 1e-3:
                continue

            diferenca = abs(p1["area"] - p2["area"])
            potencial = ganho / (diferenca + 1e-5)

            media_vizinhos = (p1["n_vizinhos"] + p2["n_vizinhos"]) / 2
            media_perimetro = (p1["perimetro"] + p2["perimetro"]) / 2

            score = potencial + 0.1 * media_vizinhos - 0.01 * media_perimetro

            sugestoes.append({
                "de": p1["OWNER"],
                "para": p2["OWNER"],
                "parcela_1": p1["PAR_ID"],
                "parcela_2": p2["PAR_ID"],
                "ganho_area_media": ganho,
                "potencial": potencial,
                "score": score
            })

    sugestoes.sort(key=lambda x: x["score"], reverse=True)
    return sugestoes[:5]


if __name__ == "__main__":
    propriedades = ler_csv_propriedades("Madeira-Moodle-1.3.csv")
    sugestoes = sugerir_trocas(propriedades, "Freguesia", "Arco da Calheta")
    for s in sugestoes:
        print(s)
