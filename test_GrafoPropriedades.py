import pytest

import tempfile
import csv
import os
from shapely.wkt import dumps as dump_wkt, loads as load_wkt
from grafoPropriedades import construir_grafo_propriedades, desenhar_grafo_propriedades

def criar_csv_temp(geometrias):
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        caminho = f.name
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["PAR_ID", "OWNER", "Freguesia", "Municipio", "Ilha", "geometry"])
        for i, wkt in enumerate(geometrias, start=1):
            writer.writerow([str(i), f"Dono{i}", "F", "M", "I", wkt])
    return caminho

def test_grafo_adjacencia():
    # A e B tocam-se, C está longe
    wkt_A = dump_wkt(load_wkt("POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"))
    wkt_B = dump_wkt(load_wkt("POLYGON((1 0, 1 1, 2 1, 2 0, 1 0))"))  # toca em A
    wkt_C = dump_wkt(load_wkt("POLYGON((10 10, 10 11, 11 11, 11 10, 10 10))"))

    caminho = criar_csv_temp([wkt_A, wkt_B, wkt_C])

    from grafoPropriedades import ler_csv  # garantir leitura correta
    linhas = []
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            row["geometry"] = load_wkt(row["geometry"])
            linhas.append(row)

    grafo = construir_grafo_propriedades(linhas)

    assert "1" in grafo and "2" in grafo["1"], "Propriedades 1 e 2 deviam ser vizinhas"
    assert "3" not in grafo["1"], "Propriedade 3 está longe e não devia ser adjacente"
    assert "3" not in grafo["2"], "Propriedade 3 está longe e não devia ser adjacente"

    os.unlink(caminho)

if __name__ == "__main__":
    test_grafo_adjacencia()
    print("✅ Todos os testes passaram.")
