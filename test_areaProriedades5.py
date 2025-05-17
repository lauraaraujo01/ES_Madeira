
import tempfile
import os
import csv
from shapely.wkt import dumps as dump_wkt, loads as load_wkt
from areaMediaPropriedades5 import ler_csv_propriedades, calcular_area_media 

def test_area_media_proprietarios_mesma_freguesia():
    propriedades = [
        {
            "PAR_ID": "1",
            "OWNER": "Joana",
            "Freguesia": "Calheta",
            "geometry": load_wkt("POLYGON((0 0, 0 2, 2 2, 2 0, 0 0))")
        },
        {
            "PAR_ID": "2",
            "OWNER": "Joana",
            "Freguesia": "Calheta",
            "geometry": load_wkt("POLYGON((2 0, 2 2, 4 2, 4 0, 2 0))")
        },
        {
            "PAR_ID": "3",
            "OWNER": "Carlos",
            "Freguesia": "Calheta",
            "geometry": load_wkt("POLYGON((10 0, 10 2, 12 2, 12 0, 10 0))")
        },
        {
            "PAR_ID": "4",
            "OWNER": "Carlos",
            "Freguesia": "Calheta",
            "geometry": load_wkt("POLYGON((12 0, 12 2, 14 2, 14 0, 12 0))")
        }
    ]

    # Joana: dois polígonos juntos (4x2 = 8)
    # Carlos: dois polígonos juntos (4x2 = 8)
    # Média = (8 + 8) / 2 = 8.0
    resultado = calcular_area_media(propriedades, "Calheta")
    assert round(resultado, 2) == 8.0

def test_ler_csv_propriedades():
    # Criar WKT válido
    wkt1 = dump_wkt(load_wkt("POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"))
    wkt2 = dump_wkt(load_wkt("POLYGON((1 0, 1 1, 2 1, 2 0, 1 0))"))

    # Criar ficheiro CSV temporário
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        caminho = f.name
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(["PAR_ID", "OWNER", "Freguesia", "geometry"])
        escritor.writerow(["1", "Ana", "Funchal", wkt1])
        escritor.writerow(["2", "Carlos", "Funchal", wkt2])

    # Chamar a função a testar
    propriedades = ler_csv_propriedades(caminho)

    # Apagar ficheiro temporário
    os.unlink(caminho)

    # Verificações
    assert len(propriedades) == 2
    assert propriedades[0]["OWNER"] == "Ana"
    assert propriedades[1]["Freguesia"] == "Funchal"
    assert propriedades[0]["geometry"].area == 1.0
    assert propriedades[1]["geometry"].area == 1.0

def test_ler_csv_propriedades_com_erro():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        caminho = f.name
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(["PAR_ID", "OWNER", "Freguesia", "geometry"])
        escritor.writerow(["1", "Erro", "Funchal", "INVALID_WKT"])  # geometria inválida

    propriedades = ler_csv_propriedades(caminho)
    os.unlink(caminho)

    # Deve ignorar a linha com erro e retornar lista vazia
    assert propriedades == []
