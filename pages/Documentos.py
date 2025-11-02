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

st.header("Base Legal e Documentos de Referência")
st.write("As análises e indicadores apresentados neste painel são fundamentados em um conjunto de documentos legais e normativos que regem o tema no Brasil. Abaixo estão listadas as principais fontes consultadas.")

st.divider()

    # --- 1. Legislação Federal ---
st.subheader("Legislação Federal")
st.markdown(f"""
    * **[Constituição da República Federativa do Brasil de 1988](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)**
    
    * **[Consolidação das Leis do Trabalho (CLT) - Decreto-Lei nº 5.452/43](https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)**
    """)

    # --- 2. Normas Regulamentadoras (NRs) ---
st.subheader("Normas Regulamentadoras (NRs)")
st.markdown("""
    As Normas Regulamentadoras, emitidas pelo Ministério do Trabalho e Emprego (MTE), 
    são disposições complementares ao Capítulo V da CLT, estabelecendo requisitos técnicos 
    e medidas de proteção para garantir a segurança e a saúde dos trabalhadores.
    
    * **[Normas Regulamentadoras - NR](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/ctpp-nrs/normas-regulamentadoras-nrs)**
    """)

    # Usar "expander" é ótimo aqui, pois as NRs são muitas
with st.expander("Ver Normas Regulamentadoras (NRs) mais utilizadas em nosso trabalho"):
        st.markdown("""
        * **[NR 01](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1)** - Disposições Gerais e Gerenciamento de Riscos Ocupacionais (GRO / PGR)
        * **[NR 05](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-5-nr-5)** - Comissão Interna de Prevenção de Acidentes (CIPA)
        * **[NR 06](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-6-nr-6)** - Equipamento de Proteção Individual (EPI)
        * **[NR 07](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-7-nr-7)** - Programa de Controle Médico de Saúde Ocupacional (PCMSO)
        * **[NR 09](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-9-nr-9)** - Avaliação e Controle das Exposições Ocupacionais a Agentes Físicos, Químicos e Biológicos
        * **[NR 15](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-15-nr-15)** - Atividades e Operações Insalubres
        * **[NR 17](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-17-nr-17)** - Ergonomia
        """)

    # --- 3. Outras Publicações ---
st.subheader("Manuais e Publicações de Apoio")
st.markdown("""
    * **[Cartilha Esquematizada sobre Acidentes do Trabalho](https://www.oabsp.org.br/upload/674049386.pdf)**
        * *Fonte: (Comissão Especial de Acidentes do Trabalho da OAB/SP)*
        * *Ano: (2024)* 
    """)