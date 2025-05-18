"""
Módulo areaMediaPropriedades

Este módulo permite calcular a área média das propriedades rústicas em diferentes níveis geográficos
(freguesia, município ou ilha), a partir de um ficheiro CSV com os dados de cadastro.

Funções:
- calcular_area_media(df, nivel, nome): Calcula a área média das propriedades para a área geográfica indicada.
"""
import pandas as pd
import sys
sys.path.append('dados')

# Carrega o ficheiro CSV
df = pd.read_csv('Madeira-Moodle-1.2.csv', sep=';')

# Função para calcular a área média com base no nível geográfico e nome da área
def calcular_area_media(df, nivel, nome):
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
    
    filtrado = df[df[nivel].str.lower() == nome.lower()]
    
    if filtrado.empty:
        print(f"Nenhuma correspondência encontrada para {nivel} = '{nome}'.")
        return None
    
    media_area = filtrado['Shape_Area'].mean()
    return media_area

# Exemplo de uso:
nivel = 'Freguesia'  # ou 'Municipio', 'Ilha'
nome = 'Arco da Calheta'

media = calcular_area_media(df, nivel, nome)

if media:
    print(f"Área média das propriedades na {nivel} '{nome}': {media:.2f} m²")
