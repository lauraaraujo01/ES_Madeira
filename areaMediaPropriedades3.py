"""
Módulo areaMediaPropriedades

Este módulo permite calcular a área média das propriedades rústicas em diferentes níveis geográficos
(freguesia, município ou ilha), a partir de um ficheiro CSV com os dados de cadastro.

Funções:
- calcular_area_media(df, nivel, nome): Calcula a área média das propriedades para a área geográfica indicada.
"""
import pandas as pd
import csv 
from shapely.geometry import shape
from shapely.ops import unary_union
from collections import defaultdict
from shapely.wkt import loads as load_wkt


def ler_csv_propriedades(caminho_csv):
    propriedades = []
    with open(caminho_csv, newline='', encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=';')
        for linha in leitor:
            try:
                geometria = load_wkt(linha["geometry"])
                propriedades.append({
                    "PAR_ID": linha["PAR_ID"],
                    "OWNER": linha["OWNER"],
                    "Freguesia": linha["Freguesia"],
                    "Municipio": linha["Municipio"],
                    "Ilha": linha["Ilha"],
                    "geometry": geometria
                })
            except Exception as e:
                print(f"Erro ao ler linha: {linha}\n{e}")
    return propriedades

# Função para calcular a área média com base no nível geográfico e nome da área
def calcular_area_media_simples(propriedades, nivel, nome):

    """
    Calcula a área média das propriedades para um nível geográfico e nome específicos.

    :param df: DataFrame com os dados das propriedades.
    :param nivel: Nível geográfico a considerar ('Freguesia', 'Municipio' ou 'Ilha').
    :param nome: Nome da área geográfica (ex: 'Arco da Calheta').
    :return: Área média das propriedades na área indicada, ou None se não for encontrada.
    :raises ValueError: Se o nível indicado não for válido.
    """
    if nivel not in ['Freguesia', 'Municipio', 'Ilha']:
        raise ValueError("Nível inválido. Escolha entre 'Freguesia', 'Municipio' ou 'Ilha'.")

    # Adiciona a área ao dicionário de propriedades
    for prop in propriedades:
        prop['area'] = prop['geometry'].area

    df = pd.DataFrame(propriedades)

    filtrado = df[df[nivel].str.lower() == nome.lower()]

    if filtrado.empty:
        print(f"Nenhuma correspondência encontrada para {nivel} = '{nome}'.")
        return None

    media_area = filtrado['area'].mean()
    return media_area
