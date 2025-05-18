import pytest
from shapely.geometry import Polygon
from areaMediaPropriedades3 import calcular_area_media_simples
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

# --- Teste 1: Cálculo válido com geometrias conhecidas ---
def test_calcular_area_media_valido():
    propriedades = [
        {
            'geometry': Polygon([(0, 0), (0, 10), (10, 10), (10, 0)]),  # Área: 100
            'Freguesia': 'Arco da Calheta',
            'Municipio': 'Calheta',
            'Ilha': 'Madeira'
        },
        {
            'geometry': Polygon([(0, 0), (0, 20), (10, 20), (10, 0)]),  # Área: 200
            'Freguesia': 'Arco da Calheta',
            'Municipio': 'Calheta',
            'Ilha': 'Madeira'
        },
        {
            'geometry': Polygon([(0, 0), (0, 30), (10, 30), (10, 0)]),  # Área: 300
            'Freguesia': 'Arco da Calheta',
            'Municipio': 'Calheta',
            'Ilha': 'Madeira'
        }
    ]
    resultado = calcular_area_media_simples(propriedades, 'Freguesia', 'Arco da Calheta')
    assert resultado == 200.0


# --- Teste 2: Nível geográfico inválido ---
def test_calcular_area_media_nivel_invalido():
    propriedades = [
        {
            'geometry': Polygon([(0, 0), (0, 10), (10, 10), (10, 0)]),
            'Freguesia': 'Funchal',
            'Municipio': 'Funchal',
            'Ilha': 'Madeira'
        }
    ]
    with pytest.raises(ValueError, match="Nível inválido"):
        calcular_area_media_simples(propriedades, 'Distrito', 'Funchal')


# --- Teste 3: Nenhuma correspondência encontrada ---
def test_calcular_area_media_sem_resultados(capsys):
    propriedades = [
        {
            'geometry': Polygon([(0, 0), (0, 10), (10, 10), (10, 0)]),
            'Freguesia': 'Funchal',
            'Municipio': 'Funchal',
            'Ilha': 'Madeira'
        }
    ]
    resultado = calcular_area_media_simples(propriedades, 'Freguesia', 'Porto Moniz')
    captured = capsys.readouterr()
    assert "Nenhuma correspondência encontrada para Freguesia = 'Porto Moniz'" in captured.out
    assert resultado is None


# --- Teste 4: Cálculo por outro nível (ex: Ilha) ---
def test_calcular_area_media_por_ilha():
    propriedades = [
        {
            'geometry': Polygon([(0, 0), (0, 10), (10, 10), (10, 0)]),  # Área: 100
            'Freguesia': 'X',
            'Municipio': 'Y',
            'Ilha': 'Madeira'
        },
        {
            'geometry': Polygon([(0, 0), (0, 30), (10, 30), (10, 0)]),  # Área: 300
            'Freguesia': 'A',
            'Municipio': 'B',
            'Ilha': 'Madeira'
        }
    ]
    resultado = calcular_area_media_simples(propriedades, 'Ilha', 'Madeira')
    assert resultado == 200.0



