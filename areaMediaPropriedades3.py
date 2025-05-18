import pandas as pd


# Carrega o ficheiro CSV
df = pd.read_csv('Madeira-Moodle-1.2.csv', sep=';')

# Função para calcular a área média com base no nível geográfico e nome da área
def calcular_area_media(df, nivel, nome):
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
