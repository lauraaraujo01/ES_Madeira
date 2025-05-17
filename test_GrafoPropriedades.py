import pytest
from grafoPropriedades import construir_grafo_propriedades, desenhar_grafo

def test_grafo_intersecta_sobreposicao():
    dados = [
        {
            "PAR_ID": "A",
            "OWNER": "X",
            "Freguesia": "F1",
            "geometry": "MULTIPOLYGON (((0 0, 2 0, 2 2, 0 2, 0 0)))"
        },
        {
            "PAR_ID": "B",
            "OWNER": "Y",
            "Freguesia": "F1",
            "geometry": "MULTIPOLYGON (((0.5 0.5, 1.5 0.5, 1.5 1.5, 0.5 1.5, 0.5 0.5)))"
        },
        {
            "PAR_ID": "C",
            "OWNER": "Z",
            "Freguesia": "F1",
            "geometry": "MULTIPOLYGON (((5 5, 6 5, 6 6, 5 6, 5 5)))"
        }
    ]

    grafo = construir_grafo_propriedades(dados)

    # A e B sobrepõem-se, devem estar ligados
    assert "B" in grafo["A"]
    assert "A" in grafo["B"]

    # C está longe, não deve ter vizinhos
    assert grafo["C"] == set()

def test_geometria_invalida():
    dados = [
        {
            "PAR_ID": "X",
            "geometry": "INVALID WKT DATA"
        }
    ]
    grafo = construir_grafo_propriedades(dados)
    assert grafo == {}  # Não deve gerar nenhum nó

def test_sobreposicao_total():
    dados = [
        {
            "PAR_ID": "A",
            "geometry": "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))"
        },
        {
            "PAR_ID": "B",
            "geometry": "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))"
        }
    ]
    grafo = construir_grafo_propriedades(dados)
    assert "B" in grafo["A"]

def test_varias_conexoes():
    dados = [
        {
            "PAR_ID": "A",
            "geometry": "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))"
        },
        {
            "PAR_ID": "B",
            "geometry": "MULTIPOLYGON (((1 0, 2 0, 2 1, 1 1, 1 0)))"
        },
        {
            "PAR_ID": "C",
            "geometry": "MULTIPOLYGON (((0 -1, 1 -1, 1 0, 0 0, 0 -1)))"
        }
    ]
    grafo = construir_grafo_propriedades(dados)
    assert "B" in grafo["A"]
    assert "C" in grafo["A"]

def test_ler_csv(tmp_path):
    # Cria ficheiro CSV temporário
    ficheiro = tmp_path / "teste.csv"
    ficheiro.write_text("PAR_ID;geometry\n1;MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))")

    from grafoPropriedades import ler_csv
    resultado = ler_csv(str(ficheiro))
    assert len(resultado) == 1
    assert resultado[0]["PAR_ID"] == "1"

def test_desenhar_grafo_sem_mostrar():
    grafo = {"A": {"B"}, "B": {"A"}}
    desenhar_grafo(grafo, mostrar=False)  # Não abre janela