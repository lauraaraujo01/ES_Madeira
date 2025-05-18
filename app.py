import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from shapely.wkt import loads as load_wkt
import io

from grafoPropriedades import construir_grafo_propriedades, desenhar_grafo_propriedades
from grafoProprietarios import construir_grafo_proprietarios, desenhar_grafo_proprietarios
from areaMediaPropriedades5 import calcular_area_media
from areaMediaPropriedades3 import calcular_area_media_simples
from sugestoesTroca import sugerir_trocas

# Inicializar variáveis persistentes
if "grafo_propriedades_fig" not in st.session_state:
    st.session_state.grafo_propriedades_fig = None

if "grafo_proprietarios_fig" not in st.session_state:
    st.session_state.grafo_proprietarios_fig = None

if "ultima_media_calculada" not in st.session_state:
    st.session_state.ultima_media_calculada = None

if "ultima_media_calculada_simples" not in st.session_state:
    st.session_state.ultima_media_calculada_simples = None    

# Resetar se for trocar de ficheiro
if "trocar_ficheiro" in st.session_state and st.session_state.trocar_ficheiro:
    st.session_state.grafo_propriedades_fig = None
    st.session_state.grafo_proprietarios_fig = None
    st.session_state.ultima_media_calculada = None

st.set_page_config(page_title="Gestão do Território", layout="wide")
st.title(" Sistema de Apoio à Decisão - Gestão do Território")

st.sidebar.title(" Navegação")
opcao = st.sidebar.radio("Ir para:", [
    "📂 Carregar Dados",
    "📈 Grafo de Propriedades",
    "👥 Grafo de Proprietários",
    "📏 Cálculo da Área Média por Nível Administrativo",
    "📏 Cálculo da Área Média por Nível Administrativo com Áreas Adjacentes",
    "🔄 Sugestões de Troca"
])

if "propriedades" not in st.session_state:
    st.session_state.propriedades = []

if opcao == "📂 Carregar Dados":
    st.header("📂 Carregar Ficheiro CSV com Geometria")

    if "csv_buffer" not in st.session_state:
        st.session_state.csv_buffer = None

    if "trocar_ficheiro" not in st.session_state:
        st.session_state.trocar_ficheiro = False

    if st.session_state.csv_buffer and not st.session_state.trocar_ficheiro:
        st.success("✅ Ficheiro já carregado anteriormente.")
        if st.button(" Carregar novo ficheiro"):
            st.session_state.trocar_ficheiro = True
    else:
        ficheiro = st.file_uploader("Escolha um ficheiro CSV com geometria:", type="csv")
        if ficheiro:
            try:
                conteudo = ficheiro.read().decode("utf-8")
                st.session_state.csv_buffer = conteudo
                st.session_state.trocar_ficheiro = False

                df = pd.read_csv(io.StringIO(conteudo), delimiter=';')

                propriedades = []
                for _, linha in df.iterrows():
                    try:
                        geom = load_wkt(linha["geometry"])
                        propriedades.append({
                            "PAR_ID": linha["PAR_ID"],
                            "OWNER": linha["OWNER"],
                            "Freguesia": linha["Freguesia"],
                            "Municipio": linha["Municipio"],
                            "Ilha": linha["Ilha"],
                            "geometry": geom,
                            "area": geom.area,
                            "perimetro": geom.length
                        })
                    except:
                        continue

                st.session_state.propriedades = propriedades
                st.success(f"✅ {len(propriedades)} propriedades carregadas com sucesso.")

            except Exception as e:
                st.error(f"Erro ao carregar ficheiro: {e}")

elif opcao == "📈 Grafo de Propriedades":
    st.header("📈 Grafo de Adjacência das Propriedades")
    if st.session_state.propriedades:
        grafo = construir_grafo_propriedades(st.session_state.propriedades)
        fig = desenhar_grafo_propriedades(grafo)
        st.session_state.grafo_propriedades_fig = fig
        st.pyplot(fig)
    elif st.session_state.grafo_propriedades_fig:
        st.pyplot(st.session_state.grafo_propriedades_fig)
    else:
        st.warning("Carregue primeiro os dados no menu 'Carregar Dados'.")


elif opcao == "👥 Grafo de Proprietários":
    st.header("👥 Grafo de Relações entre Proprietários")
    if st.session_state.propriedades:
        grafo = construir_grafo_proprietarios(st.session_state.propriedades)
        fig = desenhar_grafo_proprietarios(grafo)
        st.session_state.grafo_proprietarios_fig = fig
        st.pyplot(fig)
    elif st.session_state.grafo_proprietarios_fig:
        st.pyplot(st.session_state.grafo_proprietarios_fig)
    else:
        st.warning("Carregue primeiro os dados no menu 'Carregar Dados'.")

elif opcao == "📏 Cálculo da Área Média por Nível Administrativo com Áreas Adjacentes":
    st.header("📏 Cálculo da Área Média por Nível Administrativo com Áreas Adjacentes")

    if st.session_state.propriedades:
      
        df = pd.DataFrame(st.session_state.propriedades)

        nivel = st.selectbox("Escolha o nível geográfico:", ["Freguesia", "Municipio", "Ilha"])

        opcoes_nomes = df[nivel].dropna().unique()
        nome_escolhido = st.selectbox(f"Escolha o nome da {nivel.lower()}:", sorted(opcoes_nomes))

        if st.button("Calcular área média"):
                media = calcular_area_media(st.session_state.propriedades, nivel, nome_escolhido)
                st.session_state.ultima_media_calculada = (nome_escolhido, nivel, media)
                st.metric(f"Área média em {nome_escolhido} ({nivel})", f"{media:.2f} m²")
        elif st.session_state.ultima_media_calculada:
                nome_escolhido, nivel, media = st.session_state.ultima_media_calculada
                st.metric(f"Área média em {nome_escolhido} ({nivel})", f"{media:.2f} m²")

    else:
        st.warning("Carregue primeiro os dados no menu 'Carregar Dados'.")

elif opcao == "📏 Cálculo da Área Média por Nível Administrativo":
    st.header("📏 Cálculo da Área Média por Nível Administrativo")

    if st.session_state.propriedades:
       
        df = pd.DataFrame(st.session_state.propriedades)

        niveis = ["Freguesia", "Municipio", "Ilha"]
        nivel = st.selectbox("Escolha o nível geográfico:", niveis)

        if nivel:
            opcoes_nomes = df[nivel].dropna().unique()
            nome_escolhido = st.selectbox(f"Escolha a {nivel.lower()}:", sorted(opcoes_nomes))

            if st.button("Calcular área média"):
                media = calcular_area_media_simples(st.session_state.propriedades, nivel, nome_escolhido)
                st.session_state.ultima_media_calculada_simples = (nome_escolhido, nivel, media)
                st.metric(f"Área média em {nome_escolhido} ({nivel})", f"{media:.2f} m²")
            elif st.session_state.ultima_media_calculada_simples:
                nome_escolhido, nivel, media = st.session_state.ultima_media_calculada_simples
                st.metric(f"Área média em {nome_escolhido} ({nivel})", f"{media:.2f} m²")
    else:
                    st.warning("Carregue primeiro os dados no menu 'Carregar Dados'.")

elif opcao == "🔄 Sugestões de Troca":
    st.header("🔄 Sugestões de Troca entre Propriedades")

    if st.session_state.propriedades:
        df = pd.DataFrame(st.session_state.propriedades)

        nivel = st.selectbox("Escolha o nível geográfico:", ["Freguesia", "Municipio", "Ilha"])
        opcoes_nomes = df[nivel].dropna().unique()
        nome_escolhido = st.selectbox(f"Escolha a {nivel.lower()}:", sorted(opcoes_nomes))

        if st.button("Gerar Sugestões"):
            trocas = sugerir_trocas(st.session_state.propriedades, nivel, nome_escolhido)
            if trocas:
                for t in trocas:
                    st.success(f"Troca entre {t['de']} (prop. {t['parcela_1']}) e {t['para']} (prop. {t['parcela_2']}) | ganho: {t['ganho_area_media']:.2f} | potencial: {t['potencial']:.2f}")
            else:
                st.info("Nenhuma sugestão encontrada para esta região.")
    else:
        st.warning("Carregue primeiro os dados no menu 'Carregar Dados'.")
