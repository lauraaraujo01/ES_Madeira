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
