import pytest
from grafoPropriedades import construir_grafo_propriedades

def test_grafo_simples():
    dados = [
        {"PAR_ID": "1", "OWNER": "João", "Freguesia": "A"},
        {"PAR_ID": "2", "OWNER": "Maria", "Freguesia": "A"},
        {"PAR_ID": "3", "OWNER": "Carlos", "Freguesia": "B"},
        {"PAR_ID": "4", "OWNER": "Ana", "Freguesia": "B"},
        {"PAR_ID": "5", "OWNER": "Rui", "Freguesia": "C"},
    ]

    grafo = construir_grafo_propriedades(dados)

    assert grafo["1"] == {"2"}
    assert grafo["2"] == {"1"}
    assert grafo["3"] == {"4"}
    assert grafo["4"] == {"3"}
    assert "5" not in grafo or grafo["5"] == set()

def test_propriedade_sozinha():
    dados = [
        {"PAR_ID": "10", "OWNER": "Sofia", "Freguesia": "X"}
    ]

    grafo = construir_grafo_propriedades(dados)

    assert "10" not in grafo  # Sem vizinhos

def test_propriedades_multiplas_na_mesma_freguesia():
    dados = [
        {"PAR_ID": "a", "OWNER": "Dono1", "Freguesia": "F"},
        {"PAR_ID": "b", "OWNER": "Dono2", "Freguesia": "F"},
        {"PAR_ID": "c", "OWNER": "Dono3", "Freguesia": "F"},
    ]

    grafo = construir_grafo_propriedades(dados)

    assert grafo["a"] == {"b", "c"}
    assert grafo["b"] == {"a", "c"}
    assert grafo["c"] == {"a", "b"}