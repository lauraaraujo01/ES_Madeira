from shapely.wkt import loads 
from shapely.ops import unary_union
from collections import defaultdict
from sugestoesTroca import sugerir_trocas, ler_csv_propriedades  
import tempfile
import os
import csv
from shapely.wkt import dumps
import sys
sys.path.append('dados')

#1

def test_ler_csv_propriedades_funciona():
    # Criar conteúdo CSV temporário com geometria válida
    geometria = "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
    conteudo = "PAR_ID;OWNER;Freguesia;geometry\n" \
               "1;Ana;X;\"" + geometria + "\"\n"

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", encoding="utf-8") as f:
        f.write(conteudo)
        caminho = f.name

    try:
        propriedades = ler_csv_propriedades(caminho)
        assert len(propriedades) == 1
        prop = propriedades[0]
        assert prop["PAR_ID"] == "1"
        assert prop["OWNER"] == "Ana"
        assert prop["Freguesia"] == "X"
        assert prop["geometry"].area == 1.0
        assert abs(prop["area"] - 1.0) < 0.0001
    finally:
        os.remove(caminho)  # apagar ficheiro temporário

def test_sugerir_trocas_retorna_lista():
    propriedades = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "X", "geometry": loads("POLYGON((0 0,1 0,1 1,0 1,0 0))"), "area": 1},
        {"PAR_ID": "2", "OWNER": "Bruno", "Freguesia": "X", "geometry": loads("POLYGON((2 0,3 0,3 1,2 1,2 0))"), "area": 1},
    ]
    sugestoes = sugerir_trocas(propriedades, "X")
    assert isinstance(sugestoes, list)
    assert len(sugestoes) > 0

def test_sugerir_trocas_ignora_mesmo_owner():
    propriedades = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "X", "geometry": loads("POLYGON((0 0,1 0,1 1,0 1,0 0))"), "area": 1},
        {"PAR_ID": "2", "OWNER": "Ana", "Freguesia": "X", "geometry": loads("POLYGON((2 0,3 0,3 1,2 1,2 0))"), "area": 2},
    ]
    sugestoes = sugerir_trocas(propriedades, "X")
    assert all(s["de"] != s["para"] for s in sugestoes)

def test_sugerir_trocas_ordenacao_por_potencial():
    propriedades = [
        {"PAR_ID": "1", "OWNER": "Ana",   "Freguesia": "X", "geometry": loads("POLYGON((0 0,1 0,1 1,0 1,0 0))"), "area": 1},
        {"PAR_ID": "2", "OWNER": "Bruno", "Freguesia": "X", "geometry": loads("POLYGON((2 0,3 0,3 1,2 1,2 0))"), "area": 1.1},
        {"PAR_ID": "3", "OWNER": "Carlos","Freguesia": "X", "geometry": loads("POLYGON((4 0,5 0,5 1,4 1,4 0))"), "area": 10},
    ]
    sugestoes = sugerir_trocas(propriedades, "X")
    potenciais = [s["potencial"] for s in sugestoes]
    assert potenciais == sorted(potenciais, reverse=True)

def test_sugerir_trocas_lida_com_freguesia_errada():
    propriedades = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "Y", "geometry": loads("POLYGON((0 0,1 0,1 1,0 1,0 0))"), "area": 1},
        {"PAR_ID": "2", "OWNER": "Bruno", "Freguesia": "Y", "geometry": loads("POLYGON((2 0,3 0,3 1,2 1,2 0))"), "area": 1},
    ]
    sugestoes = sugerir_trocas(propriedades, "X")
    assert sugestoes == []


