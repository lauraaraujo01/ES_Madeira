"""
Módulo de testes para a função test_areaMediaPropriedades3

Este módulo testa a função test_areaMediaPropriedades3 do ficheiro areaMediaPropriedades3.py.
São verificadas:
- Cálculo correto em caso de dados válidos
- Erro quando o nível geográfico é inválido
- Retorno adequado e mensagem quando não há correspondência
"""
import pandas as pd
import sys
sys.path.append('src')
import sys
sys.path.append('dados')

from areaMediaPropriedades3 import calcular_area_media

def test_calcular_area_media_valido():
    """
    Testa o cálculo da área média quando os dados são válidos.

    Deve retornar 200.0 quando as áreas são 100, 200 e 300
    na freguesia 'Arco da Calheta'.
    """
    df = pd.DataFrame({
        'Shape_Area': [100, 200, 300],
        'Freguesia': ['Arco da Calheta'] * 3,
        'Municipio': ['Calheta'] * 3,
        'Ilha': ['Madeira'] * 3
    })
    resultado = calcular_area_media(df, 'Freguesia', 'Arco da Calheta')
    assert resultado == 200.0

def test_calcular_area_media_nivel_invalido():
    """
    Testa o comportamento quando um nível geográfico inválido é fornecido.

    Deve levantar um ValueError com uma mensagem específica.
    """
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
    """
    Testa o caso em que não há correspondência para a área geográfica indicada.

    Deve imprimir uma mensagem de aviso e retornar None.
    """
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
