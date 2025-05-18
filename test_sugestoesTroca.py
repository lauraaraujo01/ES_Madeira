from shapely.geometry import Polygon
from sugestoesTroca import sugerir_trocas

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
        {
            "PAR_ID": "1",
            "OWNER": "João",
            "Freguesia": "X",
            "geometry": Polygon([(0,0), (0,1), (1,1), (1,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
        {
            "PAR_ID": "2",
            "OWNER": "Maria",
            "Freguesia": "X",
            "geometry": Polygon([(1,0), (1,1), (2,1), (2,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
        {
            "PAR_ID": "3",
            "OWNER": "João",
            "Freguesia": "X",
            "geometry": Polygon([(2,0), (2,1), (3,1), (3,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
        {
            "PAR_ID": "4",
            "OWNER": "Maria",
            "Freguesia": "X",
            "geometry": Polygon([(3,0), (3,1), (4,1), (4,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
    ]

    sugestoes = sugerir_trocas(propriedades, "Freguesia", "X")
    assert isinstance(sugestoes, list)
    assert len(sugestoes) > 0, "Esperava-se pelo menos uma sugestão de troca"
    print("✅ test_troca_com_mais_de_um_dono passou")


def test_sem_trocas_possiveis_mesmo_dono():
    propriedades = [
        {
            "PAR_ID": "1",
            "OWNER": "José",
            "Freguesia": "Y",
            "geometry": Polygon([(0,0), (0,1), (1,1), (1,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
        {
            "PAR_ID": "2",
            "OWNER": "José",
            "Freguesia": "Y",
            "geometry": Polygon([(1,0), (1,1), (2,1), (2,0)]),
            "area": 1.0,
            "perimetro": 4.0
        },
    ]

    sugestoes = sugerir_trocas(propriedades, "Freguesia", "Y")
    assert len(sugestoes) == 0, "Não deve haver trocas com apenas um dono"
    print("✅ test_sem_trocas_possiveis_mesmo_dono passou")


def test_freguesia_inexistente():
    propriedades = [
        {
            "PAR_ID": "1",
            "OWNER": "Ana",
            "Freguesia": "Z",
            "geometry": Polygon([(0,0), (0,1), (1,1), (1,0)]),
            "area": 1.0,
            "perimetro": 4.0
        }
    ]

    sugestoes = sugerir_trocas(propriedades, "Freguesia", "Freguesia Inexistente")
    assert len(sugestoes) == 0, "Não deve haver trocas para freguesia não existente"
    print("✅ test_freguesia_inexistente passou")
