#importação de bibliotecas
import streamlit as st
import pandas as pd
from datetime import *
import numpy as np
import plotly.express as px
import json
import plotly.graph_objects as go
import math

#criar funções de carregamento de dados
df2 = pd.read_csv('dataset_limpo2.csv')
df2.drop(['Unnamed: 0'], axis=1, inplace= True)
df2['CNAE2.0 Empregador.1'].replace('Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - hipermercados e supermercados', 'Comércio varejista de mercadorias (produtos alimentícios)', inplace = True)
populacoes = {'Barra Mansa': 12000,'Barra do Piraí': 18000,'Itatiaia': 15000,
              'Pinheiral': 1200,'Piraí': 1800,'Porto Real': 15000,
              'Quatis': 12020,'Resende': 18800,'Rio Claro': 15000,
              'Valença': 12100}


#configurações iniciais da página
st.set_page_config(layout='wide')

st.image('logo-fat.png', width= 500 )

st.title('Observatório de Engenharia do Trabalho e Sustentabilidade')
st.subheader('Análise exploratória de dados relacionados a segurança do trabalho na Região das Agulhas Negras')
st.text('texto breve')

#amostra da base de dados
st.subheader('Base de dados:')
st.dataframe(df2)

st.divider()

# Lista de municípios (com "Geral" primeiro)
municipios = ['Geral'] + sorted(df2['Município Empregador'].unique().tolist())
tipos_grafico = ['Geral', 'Distribuição de CNAE', 'Distribuição de Ferimentos', 'Distribuição dos Acidentes por Idade', 'Funções mais atingidas', 'Tipos de Ferimentos', 'Distribuição de Acidentes no Tempo']

# Sidebar: seleção do tipo de gráfico
st.sidebar.title("Painel de Controle")
grafico_selecionado = st.sidebar.radio("Escolha o gráfico:", tipos_grafico)

abas = st.tabs(municipios)

# === Função de plotagem ===
def plotar_grafico(df, grafico, municipio):
    if grafico == 'Distribuição de CNAE':
        st.subheader("Distribuição de CNAE")

        def grafico_atualizado2(n):
            df_cnae = df['CNAE2.0 Empregador.1'].value_counts().reset_index().head(n)
            fig = px.bar(df_cnae, 
                         y='count', 
                         x='CNAE2.0 Empregador.1',
                         color='CNAE2.0 Empregador.1',
                         log_y=True)
            return fig

        escolha2 = st.slider(label='Selecione a quantidade de informações',
                             min_value=1,
                             max_value=100,
                             value=5,
                             key=f"slider_{municipio}")

        st.plotly_chart(grafico_atualizado2(escolha2), use_container_width=True)


    elif grafico == 'Distribuição de Ferimentos':
        st.subheader("Distribuição de Ferimentos (CID)")
        df_cid = df['CID - Ferimento'].value_counts().reset_index()
        fig23331 = px.bar(df_cid, 
             y='count', 
             x='CID - Ferimento',
             color= 'CID - Ferimento',
             log_y= True)
        st.plotly_chart(fig23331, use_container_width=True)

    elif grafico == 'Distribuição dos Acidentes por Idade':
        #acidentes por genero e faixa de idade
        st.subheader('Distribuição dos Acidentes por Idade')

        df['Data Nascimento'] = pd.to_datetime(df['Data Nascimento'])
        df['Data Acidente'] = pd.to_datetime(df['Data Acidente'])
        df['Idade'] = df['Data Acidente'] - df['Data Nascimento']
        df['Idade2'] =  df['Data Nascimento'] - df['Data Acidente']
        df['Idade'] = df['Idade'].dt.days
        df['Idade'] = df['Idade'] / 365.25
        df['Idade'] = df['Idade'].fillna(0)
        df['Idade'] = df['Idade'].astype(int)

        df_acidentes_limpo = df[
            (df['Idade'] != 0) &
            (df['Sexo'] != 'Não Informado')].copy()

        bins = [0, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, np.inf]
        labels = [
            '0-14 anos', '15-19 anos', '20-24 anos', '25-29 anos', '30-34 anos',
            '35-39 anos', '40-44 anos', '45-49 anos', '50-54 anos', '55-59 anos',
            '60-64 anos', '65-69 anos', '70-74 anos', '75-79 anos', '80+ anos']

        df_acidentes_limpo['Faixa Etária'] = pd.cut(
            df_acidentes_limpo['Idade'],
            bins=bins,
            labels=labels,
            right=False)

        contagem_acidentes_df = df_acidentes_limpo.groupby(['Faixa Etária', 'Sexo']).size().reset_index(name='Quantidade de Acidentes')

        fig33 = px.bar(
            contagem_acidentes_df,
            y='Faixa Etária',              
            x='Quantidade de Acidentes',   
            color='Sexo',                  
            orientation='h',               
            title='Quantidade de Acidentes por Faixa Etária e Sexo',
            labels={
                'Faixa Etária': 'Faixa Etária (anos)',
                'Quantidade de Acidentes': 'Número de Acidentes'
            },
            barmode='group',               
            category_orders={"Faixa Etária": labels},
            color_discrete_map={
            'Masculino': 'blue',
            'Feminino': 'purple'
        } 
        )

        fig33.update_layout(
            xaxis_title='Número de Acidentes',
            yaxis_title='Faixa Etária',
            legend_title='Sexo',
            height = 700
        )

        fig33.update_traces(texttemplate='%{x}', textposition='inside')

        st.plotly_chart(fig33)

    elif grafico == 'Funções mais atingidas':
        st.subheader('Funções mais atingidas')

        def grafico_atualizado(n):
            df_cbo = df["CBO - Função"].value_counts().reset_index().head(n)
            fig = px.bar(df_cbo, 
                    y='count', 
                    x='CBO - Função',
                    color= 'CBO - Função',
                    log_y= True)
            
            return fig

        escolha = st.slider(label = 'Selecione a quantidade de informações',
                min_value= 1,
                max_value= 200,
                value = 5,
                key=f"slider_{municipio}")

        st.plotly_chart(grafico_atualizado(escolha))

    elif grafico == 'Tipos de Ferimentos':
        st.subheader('Tipos de Ferimentos')

        def grafico_atualizado3(n):
            df_cid = df['CID - Ferimento'].value_counts().reset_index().head(n)
            fig = px.bar(df_cid, 
                    y='count', 
                    x='CID - Ferimento',
                    color= 'CID - Ferimento',
                    log_y= True)
            
            return fig

        escolha3 = st.slider(label = 'Selecione a quantidade de informações',
                            value=5, key=f"slider_{municipio}")
        st.plotly_chart(grafico_atualizado3(escolha3))

    elif grafico == 'Distribuição de Acidentes no Tempo':
        st.subheader('Distribuição de Acidentes no Tempo')
        ##dados
        df['data'] = pd.to_datetime(df['Data Acidente'])
        df['mes'] = df['data'].dt.month
        df['ano'] = df['data'].dt.year

        df_contagem = df['ano'].value_counts().reset_index()
        df_contagem.columns = ['Ano', 'Contagem']

        ##caixa de seleçao
        anos = sorted(df['ano'].unique())
        opcoes = ['Geral'] + [str(ano) for ano in anos]
        escolha = st.selectbox("Selecione o ano", opcoes)

        if escolha == 'Geral':
            dados_ano = df['ano'].value_counts().sort_index()
            fig = px.bar(x=dados_ano.index, y=dados_ano.values, labels={'x': 'Ano', 'y': 'Contagem'}, title='Distribuição por Ano')
        else:
            ano_escolhido = int(escolha)
            df_filtrado = df[df['ano'] == ano_escolhido]
            dados_mes = df_filtrado['mes'].value_counts().sort_index()
            fig = px.bar(x=dados_mes.index, y=dados_mes.values, labels={'x': 'Mês', 'y': 'Contagem'}, title=f'Distribuição por Mês em {ano_escolhido}')
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']))

        fig.update_traces(texttemplate='%{y}', textposition='inside')

        st.plotly_chart(fig)

    elif grafico == 'Geral':
        st.subheader("Distribuição Consolidada por Município")
        dados = []
        for mun in sorted(df['Município Empregador'].unique()):
            pop = populacoes.get(mun, 0)
            cnaes = df[df['Município Empregador'] == mun]['CNAE2.0 Empregador.1'].nunique()
            dados.append({'Município Empregador': mun, 'População': 22, 'Setores Econômicos': cnaes})
        df_resumo = pd.DataFrame(dados)

# === Gerar gráficos por aba ===
for i, tab in enumerate(abas):
    municipio = municipios[i]
    with tab:
        st.markdown(f"### Município: {municipio}")

        # Aba Geral: descrição genérica
        if municipio == 'Geral':
            df_filtrado = df2.copy()

            if grafico_selecionado == "Geral":
                st.info("Este painel apresenta uma visão consolidada dos municípios com base nos principais indicadores.")

                #gráfico da região
                dfci = json.load(open('geojs-33-mun.json', 'r'))

                df_semacento = df2["Município Empregador"].value_counts().reset_index()
                df_semacento['Município Empregador'].replace('Piraí', 'Pirai', inplace=True)
                df_semacento['Município Empregador'].replace('Barra do Piraí', 'Barra do Pirai', inplace=True)
                df_semacento['Município Empregador'].replace('Valença', 'Valenca', inplace=True)


                mapa = px.choropleth_mapbox(data_frame = df_semacento,
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
                mapa.update_geos(fitbounds="locations", visible=False)

                mapa.update_layout(title="Coloração do Mapa da Região do Médio Paraíba Conforme o Nº de Acidentes",
                                width = 850,
                                height = 530)
                st.plotly_chart(mapa)

            #acidentes tree map
                #colunas
                st.subheader('Quantidade de Acidentes por Município')
                col1, col2 =  st.columns([2, 7])

                col1.write("A distribuição do número de acidentes na Região do Médio Vale Paraíba mostra como os incidentes se concentram nas cidades de Volta Redonda, Barra Mansa e Resende.")

                municipio_counts = df2['Município Empregador'].value_counts().reset_index()
                municipio_counts.columns = ['Município Empregador', 'count']

                #treemap de municipio
                fig2222 = px.treemap(municipio_counts, path=['Município Empregador'], values='count',
                                title=' ')

                fig2222.data[0].textinfo = 'label+value'

                fig2222.update_layout(
                    margin=dict(t=50, l=25, r=25, b=25),
                    title_font_size=28,
                    uniformtext=dict(minsize=14, mode='show'))

                col2.plotly_chart(fig2222)

            plotar_grafico(df_filtrado, grafico_selecionado, municipio)

        else:
            df_filtrado = df2[df2['Município Empregador'] == municipio]

            # Mostra a população do município
            pop = populacoes.get(municipio, "Desconhecida") # transforma 12000 -> "12.000"
            st.metric("População estimada", pop)

        # Chama a função para exibir o gráfico selecionado
            plotar_grafico(df_filtrado, grafico_selecionado, municipio)
