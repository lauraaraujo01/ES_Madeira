from shapely.wkt import loads as load_wkt
from shapely.ops import unary_union
from collections import defaultdict
import csv
import sys
sys.path.append('dados')

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
                    "area": geometria.area
                })
            except Exception as e:
                print(f"Erro ao ler linha: {linha}\n{e}")
    return propriedades

def sugerir_trocas(propriedades, freguesia_escolhida):
    props = [p for p in propriedades if p["Freguesia"] == freguesia_escolhida]
    sugestoes = []

    for i in range(len(props)):
        for j in range(i + 1, len(props)):
            p1, p2 = props[i], props[j]
            if p1["OWNER"] == p2["OWNER"]:
                continue

            # Troca virtual
            propriedades_trocadas = props.copy()
            propriedades_trocadas[i] = {**p1, "OWNER": p2["OWNER"]}
            propriedades_trocadas[j] = {**p2, "OWNER": p1["OWNER"]}

            area_antes = calcular_area_media(props, freguesia_escolhida)
            area_depois = calcular_area_media(propriedades_trocadas, freguesia_escolhida)
            ganho = area_depois - area_antes
            diferenca = abs(p1["area"] - p2["area"])
            potencial = ganho / (diferenca + 1e-5)

            sugestoes.append({
                "de": p1["OWNER"],
                "para": p2["OWNER"],
                "parcela_1": p1["PAR_ID"],
                "parcela_2": p2["PAR_ID"],
                "ganho_area_media": ganho,
                "diferenca_areas": diferenca,
                "potencial": potencial
            })

    sugestoes.sort(key=lambda x: x["potencial"], reverse=True)
    return sugestoes[:5]  # top 5 sugestões

# Uso
if __name__ == "__main__":
    propriedades = ler_csv_propriedades("Madeira-Moodle-1.3.csv")
    sugestoes = sugerir_trocas(propriedades, "Arco da Calheta")
    for s in sugestoes:
        print(s)
