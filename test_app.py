from shapely.wkt import loads as load_wkt

# Função mock de leitura de propriedades
def ler_csv_propriedades_mock():
    linhas = [
        {
            "PAR_ID": "1",
            "OWNER": "João",
            "Freguesia": "X",
            "Municipio": "Y",
            "Ilha": "Z",
            "geometry": "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
        },
        {
            "PAR_ID": "2",
            "OWNER": "Maria",
            "Freguesia": "X",
            "Municipio": "Y",
            "Ilha": "Z",
            "geometry": "POLYGON((2 2, 3 2, 3 3, 2 3, 2 2))"
        }
    ]

    propriedades = []
    for linha in linhas:
        geom = load_wkt(linha["geometry"])
        propriedades.append({
            "PAR_ID": linha["PAR_ID"],
            "OWNER": linha["OWNER"],
            "Freguesia": linha["Freguesia"],
            "Municipio": linha["Municipio"],
            "Ilha": linha["Ilha"],
            "geometry": geom,
            "area": geom.area,
            "perimetro": geom.length
        })

    return propriedades

# Teste da função mock
def test_ler_csv_propriedades_mock():
    propriedades = ler_csv_propriedades_mock()

    assert len(propriedades) == 2

    for prop in propriedades:
        assert "PAR_ID" in prop
        assert "OWNER" in prop
        assert "geometry" in prop
        assert "area" in prop
        assert "perimetro" in prop

    assert propriedades[0]["area"] == 1.0
    assert round(propriedades[0]["perimetro"], 2) == 4.0
