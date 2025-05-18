import pytest


from grafoProprietarios import construir_grafo_proprietarios, desenhar_grafo, ler_csv
import tempfile
import os

def test_grafo_proprietarios_simples():
    dados = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "X"},
        {"PAR_ID": "2", "OWNER": "Bruno", "Freguesia": "X"},
        {"PAR_ID": "3", "OWNER": "Ana", "Freguesia": "Y"},
        {"PAR_ID": "4", "OWNER": "Carlos", "Freguesia": "Y"},
        {"PAR_ID": "5", "OWNER": "Carlos", "Freguesia": "X"},
    ]

    grafo = construir_grafo_proprietarios(dados)

    assert "Bruno" in grafo["Ana"]
    assert "Carlos" in grafo["Ana"]
    assert "Carlos" in grafo["Bruno"]

def test_dono_sem_vizinhos():
    dados = [{"PAR_ID": "10", "OWNER": "Sofia", "Freguesia": "Z"}]
    grafo = construir_grafo_proprietarios(dados)
    assert "Sofia" not in grafo or grafo["Sofia"] == set()

def test_ignora_donos_iguais_na_mesma_freguesia():
    dados = [
        {"PAR_ID": "1", "OWNER": "Ana", "Freguesia": "X"},
        {"PAR_ID": "2", "OWNER": "Ana", "Freguesia": "X"}
    ]
    grafo = construir_grafo_proprietarios(dados)
    assert "Ana" not in grafo or grafo["Ana"] == set()

def test_ler_csv_funciona_com_ficheiro_temporario():
    conteudo = "PAR_ID;OWNER;Freguesia\n1;João;X\n2;Maria;Y\n"
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        f.write(conteudo)
        f.seek(0)
        dados = ler_csv(f.name)
    os.unlink(f.name)  # apagar ficheiro
    assert len(dados) == 2
    assert dados[0]["OWNER"] == "João"
    assert dados[1]["Freguesia"] == "Y"

def test_desenhar_grafo_sem_mostrar():
    grafo = {"A": {"B"}, "B": {"A"}}
    desenhar_grafo(grafo, mostrar=False)
