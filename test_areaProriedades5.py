import tempfile
import os
import csv
from shapely.wkt import dumps as dump_wkt, loads as load_wkt
from areaMediaPropriedades5 import calcular_area_media, ler_csv_propriedades

def test_area_media_proprietarios_mesma_freguesia():
    propriedades = [
        {
            "PAR_ID": "1",
            "OWNER": "Joana",
            "Freguesia": "Calheta",
            "Municipio": "XYZ",
            "Ilha": "Madeira",
            "geometry": load_wkt("POLYGON((0 0, 0 2, 2 2, 2 0, 0 0))")
        },
        {
            "PAR_ID": "2",
            "OWNER": "Joana",
            "Freguesia": "Calheta",
            "Municipio": "XYZ",
            "Ilha": "Madeira",
            "geometry": load_wkt("POLYGON((2 0, 2 2, 4 2, 4 0, 2 0))")
        },
        {
            "PAR_ID": "3",
            "OWNER": "Carlos",
            "Freguesia": "Calheta",
            "Municipio": "XYZ",
            "Ilha": "Madeira",
            "geometry": load_wkt("POLYGON((10 0, 10 2, 12 2, 12 0, 10 0))")
        },
        {
            "PAR_ID": "4",
            "OWNER": "Carlos",
            "Freguesia": "Calheta",
            "Municipio": "XYZ",
            "Ilha": "Madeira",
            "geometry": load_wkt("POLYGON((12 0, 12 2, 14 2, 14 0, 12 0))")
        }
    ]
    resultado = calcular_area_media(propriedades, "Freguesia", "Calheta")
    assert round(resultado, 2) == 8.0

def test_ler_csv_propriedades():
    wkt1 = dump_wkt(load_wkt("POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"))
    wkt2 = dump_wkt(load_wkt("POLYGON((1 0, 1 1, 2 1, 2 0, 1 0))"))
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        caminho = f.name
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(["PAR_ID", "OWNER", "Freguesia", "Municipio", "Ilha", "geometry"])
        escritor.writerow(["1", "Ana", "Funchal", "A", "X", wkt1])
        escritor.writerow(["2", "Carlos", "Funchal", "A", "X", wkt2])

    propriedades = ler_csv_propriedades(caminho)
    os.unlink(caminho)

    assert len(propriedades) == 2
    assert propriedades[0]["OWNER"] == "Ana"
    assert propriedades[1]["Freguesia"] == "Funchal"
    assert round(propriedades[0]["geometry"].area, 2) == 1.0
    assert round(propriedades[1]["geometry"].area, 2) == 1.0

def test_ler_csv_propriedades_com_erro():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        caminho = f.name
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(["PAR_ID", "OWNER", "Freguesia", "Municipio", "Ilha", "geometry"])
        escritor.writerow(["1", "Erro", "Funchal", "A", "X", "INVALID_WKT"])

    propriedades = ler_csv_propriedades(caminho)
    os.unlink(caminho)

    assert propriedades == []
