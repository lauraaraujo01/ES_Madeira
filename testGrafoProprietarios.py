import pytest
from grafoProprietarios import construir_grafo_proprietarios

def test_grafo_proprietarios_simples():
    dados = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "X"},
        {"PAR_ID": "2", "OWNER": "Bruno", "Freguesia": "X"},
        {"PAR_ID": "3", "OWNER": "Ana", "Freguesia": "Y"},
        {"PAR_ID": "4", "OWNER": "Carlos", "Freguesia": "Y"},
        {"PAR_ID": "5", "OWNER": "Carlos", "Freguesia": "X"},
    ]

    grafo = construir_grafo_proprietarios(dados)

    # Ana e Bruno têm propriedades na mesma freguesia X
    assert "Bruno" in grafo["Ana"]
    assert "Ana" in grafo["Bruno"]

    # Ana e Carlos têm propriedades na mesma freguesia Y
    assert "Carlos" in grafo["Ana"]
    assert "Ana" in grafo["Carlos"]

    # Carlos e Bruno também são vizinhos em X
    assert "Bruno" in grafo["Carlos"]
    assert "Carlos" in grafo["Bruno"]

def test_dono_sem_vizinhos():
    dados = [
        {"PAR_ID": "10", "OWNER": "Sofia", "Freguesia": "Z"}
    ]

    grafo = construir_grafo_proprietarios(dados)
    assert "Sofia" not in grafo or grafo["Sofia"] == set()
