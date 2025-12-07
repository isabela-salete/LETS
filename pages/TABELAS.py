import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
from unidecode import unidecode
import re
import base64
import os

# Função para converter a imagem em Base64
def get_base64_of_bin_file(bin_file):
    """Carrega o arquivo binário da imagem, codifica em Base64 e retorna uma string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return "" 

img_file = 'logo-fat.png'
img_base64 = ""

if os.path.exists(img_file):
    img_base64 = get_base64_of_bin_file(img_file)
else:
    st.error(f"Erro: O arquivo de imagem '{img_file}' não foi encontrado na pasta do script. Verifique o nome e o caminho.")

st.markdown(
    """
    <style>
    /* Oculta a barra de navegação de páginas nativa */
    section[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Estilo para a nossa barra fixa principal */
    .fixed-header {
        position: fixed;
        top: 60px;
        left: 0px;
        width: 107.5%;
        background-color: #f0f4f6; 
        padding: 10px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        z-index: 999;
        display: flex;
        align-items: center;
        transition: left 0.3s, width 0.3s;
        justify-content: center;
    }
    
    .header-image {
        height: 80px;
        margin-right: 40px;
    }
    .header-title {
        font-size: 22px;
        font-weight: bold;
        color: #000;
        margin: 0;
    }

    /* Ajuste para a sidebar quando ela está aberta. */
    .sidebar-open .fixed-header {
        left: 250px;
        width: calc(100% - 250px);
    }
    
    .stApp {
        padding-top: 80px; 
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="fixed-header">
        <img class="header-image" src="data:image/png;base64,{img_base64}" alt="Logo">
        <h1 class="header-title">Observatório de Engenharia do Trabalho e Sustentabilidade</h1>
    </div>
    """,
    unsafe_allow_html=True
)


st.subheader(" ")

#Tabelas - CBO
st.header('Tabelas de Referência: CBO')

df_cbo1 = pd.read_csv('tabelas/CBO2002-Ocupacao.csv')
df_cbo2 = pd.read_csv('tabelas/CBO2002-SubGrupo.csv')
df_cbo3 = pd.read_csv('tabelas/CBO2002-SubGrupoPrincipal.csv')
df_cbo4 = pd.read_csv('tabelas/CBO2002-Familia.csv')

st.subheader("Tabela de Ocupações CBO 2002")
st.dataframe(df_cbo1)

st.subheader("Tabela de Sub Grupo CBO 2002")
st.dataframe(df_cbo2)

st.subheader("Tabela de Sub Grupo Principal CBO 2002")
st.dataframe(df_cbo3)

st.subheader("Tabela de Familia CBO 2002")
st.dataframe(df_cbo4)

st.divider()

#Tabelas - CID
st.header('Tabelas de Referência: CID')

df_cid1 = pd.read_csv('tabelas/CID-CAPITULOS.csv')
df_cid2 = pd.read_csv('tabelas/CID-GRUPO.csv')
df_cid3 = pd.read_csv('tabelas/CID-CATEGORIAS.csv')
df_cid4 = pd.read_csv('tabelas/CID-SUBCATEGORIAS.csv')


st.subheader("Tabela de Capítulos CID 10")
st.dataframe(df_cid1)

st.subheader("Tabela de Grupo CID 10")
st.dataframe(df_cid2)

st.subheader("Tabela de Categorias CID 10")
st.dataframe(df_cid3)

st.subheader("Tabela de Sub Categorias CID 10")
st.dataframe(df_cid4)

st.divider()

#Tabelas - CNAE
st.header('Tabelas de Referência: CNAE')

df_cnae = pd.read_csv('tabelas/CNAE-Tabela.csv')

st.subheader("Tabela Geral CNAE")
st.dataframe(df_cnae)

st.divider()

#Tabelas - DEMAIS
st.header('Tabelas de Referência: Demais associadas')

st.subheader("Tabela Agente Causador do Acidente")
df_agente= pd.read_csv('tabelas/AGENTE.csv')
st.dataframe(df_agente)
st.divider()

st.subheader("Tabela Natureza da Lesão")
df_natureza= pd.read_csv('tabelas/NATUREZA.csv')
st.dataframe(df_natureza)
st.divider()

st.subheader("Tabela Parte do Corpo Atingida")
df_parte= pd.read_csv('tabelas/PARTE-ATINGIDA.csv')
st.dataframe(df_parte)
st.divider()
