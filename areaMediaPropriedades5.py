from shapely.geometry import shape
from shapely.ops import unary_union
from collections import defaultdict
from shapely.wkt import loads as load_wkt
import csv
import sys
sys.path.append('dados')


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
                    "geometry": geometria
                })
            except Exception as e:
                print(f"Erro ao ler linha: {linha}\n{e}")
    return propriedades

def calcular_area_media(propriedades, freguesia_escolhida):
    # Filtra propriedades da freguesia escolhida
    propriedades_filtradas = [p for p in propriedades if p["Freguesia"] == freguesia_escolhida]

    # Agrupa por dono
    grupos_por_dono = defaultdict(list)
    for prop in propriedades_filtradas:
        grupos_por_dono[prop["OWNER"]].append(prop)

    propriedades_agrupadas = []

    for dono, lista in grupos_por_dono.items():
        visitadas = set()

        for i, prop in enumerate(lista):
            if i in visitadas:
                continue

            grupo = [prop["geometry"]]
            stack = [i]
            visitadas.add(i)

            while stack:
                atual = stack.pop()
                for j, outra_prop in enumerate(lista):
                    if j not in visitadas and lista[atual]["geometry"].intersects(outra_prop["geometry"]):
                        grupo.append(outra_prop["geometry"])
                        stack.append(j)
                        visitadas.add(j)

            propriedades_agrupadas.append(unary_union(grupo))

    if not propriedades_agrupadas:
        return 0

    soma_areas = sum(geom.area for geom in propriedades_agrupadas)
    area_media = soma_areas / len(propriedades_agrupadas)
    return area_media

# Exemplo de uso
if __name__ == "__main__":
    propriedades = ler_csv_propriedades("Madeira-Moodle-1.2.csv")
    media = calcular_area_media(propriedades, "Arco da Calheta")
    print(f"\n✅ Área média em 'Arco da Calheta': {media:.2f} m2")
