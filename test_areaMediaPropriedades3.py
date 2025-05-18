import pandas as pd
import sys
sys.path.append('src')
import sys
sys.path.append('dados')

from areaMediaPropriedades3 import calcular_area_media

def test_calcular_area_media_valido():
    df = pd.DataFrame({
        'Shape_Area': [100, 200, 300],
        'Freguesia': ['Arco da Calheta'] * 3,
        'Municipio': ['Calheta'] * 3,
        'Ilha': ['Madeira'] * 3
    })
    resultado = calcular_area_media(df, 'Freguesia', 'Arco da Calheta')
    assert resultado == 200.0

def test_calcular_area_media_nivel_invalido():
    df = pd.DataFrame({
        'Shape_Area': [150],
        'Freguesia': ['Funchal'],
        'Municipio': ['Funchal'],
        'Ilha': ['Madeira']
    })
    try:
        calcular_area_media(df, 'Distrito', 'Funchal')
    except ValueError as e:
        assert str(e) == "Nível inválido. Escolha entre 'Freguesia', 'Municipio' ou 'Ilha'."

def test_calcular_area_media_sem_resultados(capsys):
    df = pd.DataFrame({
        'Shape_Area': [150],
        'Freguesia': ['Funchal'],
        'Municipio': ['Funchal'],
        'Ilha': ['Madeira']
    })
    resultado = calcular_area_media(df, 'Freguesia', 'Porto Moniz')
    captured = capsys.readouterr()
    assert "Nenhuma correspondência encontrada para Freguesia = 'Porto Moniz'" in captured.out
    assert resultado is None
