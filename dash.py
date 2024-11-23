#importação de bibliotecas

import streamlit as st
import pandas as pd
from datetime import *
import numpy as np
import plotly.express as px
import json

df2 = pd.read_csv('dataset_limpo2.csv')
df2.drop(['Unnamed: 0'], axis=1, inplace= True)
df2['CNAE2.0 Empregador.1'].replace('Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - hipermercados e supermercados', 'Comércio varejista de mercadorias (produtos alimentícios)', inplace = True)
#criar funções de carregamento de dados

st.set_page_config(layout='wide')

st.image('logo-fat.png', width= 500 )

st.title('Observatório de Engenharia do Trabalho e Sustentabilidade')
st.subheader('Análise exploratória de dados relacionados a segurança do trabalho na Região das Agulhas Negras')
st.text('texto breve')


st.subheader('Base de dados:')
st.dataframe(df2)

#gráfico da região
dfci = json.load(open('geojs-33-mun.json', 'r'))

df_semacento = df2["Município Empregador"].value_counts().reset_index()
df_semacento['Município Empregador'].replace('Piraí', 'Pirai', inplace=True)
df_semacento['Município Empregador'].replace('Barra do Piraí', 'Barra do Pirai', inplace=True)
df_semacento['Município Empregador'].replace('Valença', 'Valenca', inplace=True)


fig = px.choropleth_mapbox(data_frame = df_semacento,
                        geojson=dfci,
                        color = "count",
                        color_continuous_scale="greens",
                        locations="Município Empregador",
                        featureidkey="properties.name",
                        center={"lat": -22.5, "lon": -44.1},                       
                        mapbox_style="carto-positron",
                        zoom=8.2,
                        opacity=1,
                        hover_name = 'Município Empregador')
fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(title="Coloração do Mapa da Região do Médio Paraíba Conforme o Nº de Acidentes",
                  width = 850,
                  height = 530)

st.plotly_chart(fig)

#gráfico de barras por município
df_munic = df2["Município Empregador"].value_counts().reset_index()
st.subheader('Distribuição de Acidentes por Município: ')
select = st.selectbox(label = 'Escolha o tipo de gráfico',
                      options=["Gráfico de Barras", "Gráfico de Pizza"])

#colunas
col1, col2 =  st.columns([2, 7])

col1.write("A distribuição do número de acidentes na Região do Médio Vale Paraíba mostra como os incidentes se concentram nas cidades de Volta Redonda, Barra Mansa e Resende.")

def grafic(select):
    fig1 = px.bar(df_munic, 
             y='count', 
             x='Município Empregador',
             color= 'Município Empregador',)
    fig1.update_layout(title="Distribuição do Nº de Acidentes na Região")


    ############----

    fig2 = px.pie(df_munic, 
             values='count', 
             names='Município Empregador',
             color= 'Município Empregador',)
    fig2.update_layout(title="Distribuição do Nº de Acidentes na Região")

    if select == 'Gráfico de Barras':
        return fig1
    else:
        return fig2


col2.plotly_chart(grafic(select))

st.subheader('Distribuição de Colunas com Poucas Variáveis: ')
att = st.selectbox(label = 'Escolha o gráfico',
                   options=["Gráfico por Gênero", "Gráfico por Óbito", "Gráfico por Tipo de Acidente"])

def attpizza(att):
    #gráfico de pizza por gênero
    
    df_genero = df2["Sexo"].value_counts().reset_index()
    fig1 = px.pie(df_genero, 
                values='count', 
                names='Sexo',
                color= 'Sexo',
                color_discrete_map={"Masculino":"red",
                                    "Feminino":"blue", 
                                    "Não Informado": "green"})
    
    #gráfico de pizza por tipo de acidente
    df_tipoacidente = df2["Tipo do Acidente"].value_counts().reset_index()
    fig2 = px.pie(df_tipoacidente, 
                values='count', 
                names='Tipo do Acidente',
                color= 'Tipo do Acidente')
    

    #gráfico de pizza por indica óbito
    df_indica = df2['Indica Óbito Acidente'].value_counts().reset_index()
    fig3 = px.pie(df_indica, 
                values='count', 
                names='Indica Óbito Acidente',
                color= 'Indica Óbito Acidente')
    
    if att == 'Gráfico por Gênero':
        return fig1
    elif att == 'Gráfico por Tipo de Acidente':
        return fig2
    else:
        return fig3

st.plotly_chart(attpizza(att))

#gráfico de barras por município

st.subheader('Distribuição de Acidentes por Município: ')

def grafico_atualizado(n):
    df_cbo = df2["CBO - Função"].value_counts().reset_index().head(n)
    fig = px.bar(df_cbo, 
             y='count', 
             x='CBO - Função',
             color= 'CBO - Função',
             log_y= True)
    
    return fig

escolha = st.slider(label = 'Selecione a quantidade de informações',
          min_value= 1,
          max_value= 200,
          value = 5)

st.plotly_chart(grafico_atualizado(escolha))


#gráfico cnae
st.subheader('Distribuição de CNAE: ')
def grafico_atualizado2(n):
    df_cnae = df2['CNAE2.0 Empregador.1'].value_counts().reset_index().head(n)
    fig = px.bar(df_cnae, 
             y='count', 
             x='CNAE2.0 Empregador.1',
             color= 'CNAE2.0 Empregador.1',
             log_y= True)
    
    return fig

escolha2 = st.slider(label = 'Selecione a quantidade de informações',
                     min_value=1,
                     max_value=100,
                     value = 5)

st.plotly_chart(grafico_atualizado2(escolha2))


#gráfico cid
st.subheader('Distribuição de Ferimentos: ')

def grafico_atualizado3(n):
    df_cid = df2['CID - Ferimento'].value_counts().reset_index().head(n)
    fig = px.bar(df_cid, 
             y='count', 
             x='CID - Ferimento',
             color= 'CID - Ferimento',
             log_y= True)
    
    return fig

escolha3 = st.slider(label = 'Selecione a quantidade de informações',
                     value=5)
st.plotly_chart(grafico_atualizado3(escolha3))


##correlação
