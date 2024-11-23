import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df2 = pd.read_csv('pinheiral.csv')
df2.drop(['Unnamed: 0'], axis=1, inplace= True)

st.title('Análise no município de Pinheiral')
st.dataframe(df2)

#gráfico de pizza por gênero
st.subheader('Distribuição de Acidentes por Gênero: ')
df_genero = df2["Sexo"].value_counts().reset_index()
fig = px.pie(df_genero, 
             values='count', 
             names='Sexo',
             color= 'Sexo',
             color_discrete_map={"Masculino":"blue",
                                 "Feminino":"red", 
                                 "Não Informado": "green"})
st.plotly_chart(fig, use_container_width=True)

#gráfico cbo
st.subheader('Distribuição de Profissiões: ')
df_cbo = df2["CBO - Função"].value_counts().reset_index()
fig = px.bar(df_cbo, 
             y='count', 
             x='CBO - Função',
             color= 'CBO - Função',
             log_y= True)
st.plotly_chart(fig, use_container_width=True)


#gráfico cnae
st.subheader('Distribuição de CNAE: ')
df_cnae = df2['CNAE2.0 Empregador.1'].value_counts().reset_index()
fig = px.bar(df_cnae, 
             y='count', 
             x='CNAE2.0 Empregador.1',
             color= 'CNAE2.0 Empregador.1',
             log_y= True)
st.plotly_chart(fig, use_container_width=True)

#gráfico cid
st.subheader('Distribuição de Ferimentos: ')
df_cid = df2['CID - Ferimento'].value_counts().reset_index()
fig = px.bar(df_cid, 
             y='count', 
             x='CID - Ferimento',
             color= 'CID - Ferimento',
             log_y= True)
st.plotly_chart(fig, use_container_width=True)