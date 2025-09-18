import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
from unidecode import unidecode
import re

st.set_page_config(layout='wide')

st.image('logo-fat.png', width= 500 )

st.title('Observatório de Engenharia do Trabalho e Sustentabilidade')
st.subheader('Análise exploratória de dados relacionados a segurança do trabalho na Região do Médio Vale Paraíba')


def slugify(text):
    import re
    return re.sub(r'\W+', '_', text.lower())

def load_css(file_name):
    try:
        with open(file_name, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Erro: O arquivo CSS '{file_name}' não foi encontrado. Verifique o caminho.")
    except UnicodeDecodeError as e:
        st.error(f"Erro de decodificação no arquivo CSS '{file_name}': {e}. Tente salvar o arquivo CSS como UTF-8.")
    except Exception as e:
        st.error(f"Um erro inesperado ocorreu ao carregar o CSS: {e}")

load_css("style.css")

# Carregar o segundo dataset
df2 = pd.read_csv('dataset_limpo2.csv')
df2.drop(['Unnamed: 0'], axis=1, inplace=True)
df2['CNAE2.0 Empregador.1'].replace('Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - hipermercados e supermercados',
                                   'Comércio varejista de mercadorias (produtos alimentícios)', inplace=True)

df_info = pd.read_csv("info.csv")
# Carregar dados para mapa
#gráfico da região
dfci = json.load(open('geojs-33-mun.json', 'r'))

df_semacento = df2["Município Empregador"].value_counts().reset_index()
df_semacento['Município Empregador'].replace('Piraí', 'Pirai', inplace=True)
df_semacento['Município Empregador'].replace('Barra do Piraí', 'Barra do Pirai', inplace=True)
df_semacento['Município Empregador'].replace('Valença', 'Valenca', inplace=True)

# Nomes de municípios manualmente
municipios = ["Geral", "Barra do Piraí", "Barra Mansa", "Itatiaia", "Pinheiral", "Piraí", "Porto Real", "Quatis", "Resende", "Rio Claro", 
              "Rio das Flores", "Valença", "Volta Redonda"]
municipios_sem_acento = {m: unidecode(m) for m in municipios}

# Descrições dos municípios
descricoes_municipios = {
    "Geral": "Esta visão geral apresenta informações agregadas sobre todos os municípios da região.",
    "Barra do Piraí":"Barra do Piraí é um município localizado no sul fluminense, cercado por áreas verdes e paisagens serranas. Com forte tradição na agropecuária e pequenos negócios, tem população acolhedora e espírito comunitário. O setor industrial também está presente, com indústrias voltadas para o beneficiamento de alimentos e indústria leve. O município investe em educação e cultura local, promovendo eventos que valorizam artistas e manifestações populares. O turismo ecológico tem crescido, com trilhas e cachoeiras atraindo visitantes. Barreiras ambientais têm sido enfrentadas com projetos de recuperação de matas e qualidade da água.",
    "Barra Mansa": "Barra Mansa, grande polo industrial do sul do estado do Rio, destaca-se pela siderurgia, comércio e forte presença de pequenas e médias empresas. Seu crescimento econômico é complementado por iniciativas na área de educação, com escolas técnicas e cursos profissionalizantes. A cidade está estrategicamente localizada na região do Vale do Paraíba, próxima a importantes rodovias e a Resende. Culturalmente, promove feiras, exposições e festivais que movimentam a comunidade. O setor de serviços segue em expansão, acompanhando o dinamismo demográfico. Projetos de urbanização e recuperação ambiental são prioridades da gestão local.",
    "Itatiaia":"Itatiaia é conhecida por abrigar o Parque Nacional de mesmo nome, atraindo ecoturismo com trilhas, cachoeiras e clima de montanha. A cidade valoriza sua ligação com a natureza e preserva uma forte identidade ambiental. Apesar de seu pequeno porte, possui estrutura de pousadas, restaurantes e turismo de campo em expansão. Há também investimentos em educação e infraestrutura para receber visitantes com conforto. A economia local tem ganho força com o desenvolvimento do turismo interiorano. A comunidade local se mobiliza em projetos de sustentabilidade e preservação.",
    "Pinheiral":"Pinheiral tem papel relevante como município estratégico no Polo Regional do Sul Fluminense. Com população em crescimento, desenvolve projetos educacionais e culturais para jovens e adultos. O comércio local é diversificado, servindo de apoio a municípios vizinhos. O setor industrial cresce lentamente, com pequenas indústrias e serviços. A cidade possui áreas verdes e projetos de urbanização que valorizam a qualidade de vida. A proximidade com Resende e Barra Mansa faz de Pinheiral um local favorável para quem busca acesso a grandes centros, mas com perfil mais tranquilo.",
    "Piraí":"Piraí é uma cidade histórica com paisagens montanhosas, conhecida por suas construções coloniais e rios. A economia local combina agricultura, pecuária e turismo rural. Pequenos comércios e serviços atendem à população de maneira comunitária. Eventos culturais, feiras agrícolas e festas religiosas movimentam a vida local. A educação tem posição de destaque, com unidades de ensino bem avaliadas. Projetos de conservação de mananciais e áreas verdes são importantes para a sustentabilidade. O município é um convite ao turismo de campo e à vivência de tradições.",
    "Porto Real":"Porto Real é pequeno município industrial do sul fluminense, integrando-se à economia regional por meio de metalurgia e produção de componentes automotivos. Localizado estrategicamente, atrai investimentos e tem perfil populacional jovem. O comércio local é centrado em serviços para a população e trabalhadores da indústria. Há interesse em fortalecer programas de educação técnica e empregabilidade. A infraestrutura urbana é bem desenvolvida para o porte do município, com vias pavimentadas e rede de internet. Projetos de qualificação profissional estão em destaque.",
    "Quatis":"Quatis é um município em desenvolvimento, localizado próximo a grandes polos industriais, o que cria boas oportunidades de trabalho. A população jovem valoriza a expansão da educação técnica e programas culturais voltados à música e ao esporte. O comércio de bairro e os serviços destinados às famílias locais estão crescendo. Preserva áreas verdes e investe em práticas sustentáveis nos arredores do município. Projetos de parcerias com cidades vizinhas promovem eventos regionais e desenvolvimento integrado. A qualidade de vida ainda é um atrativo para quem busca um município menor, porém dinâmico.",
    "Resende": "Resende é um dos principais polos industriais do sul do Rio de Janeiro, com forte presença da indústria automotiva e química. A cidade conta com boa infraestrutura de ensino técnico e superior, atraindo estudantes da região. O turismo histórico e cultural também recebe atenção, com museus e patrimônio arquitetônico preservado. O setor de serviços é consolidado, com comércio movimentado e centros comerciais. Eventos esportivos e feiras regionais reforçam a integração metropolitana. Iniciativas ambientais voltam-se à recuperação de margens de rios e parques urbanos.",
    "Rio Claro":"Rio Claro é um município de perfil agrícola, com destaque para plantações e pequenas agroindústrias. A economia local procura equilibrar comércio, serviços e infraestrutura voltada às famílias. A educação municipal está em expansão, com foco em inovação e sustentabilidade. A cidade preserva características rurais e mantém festivais e feiras agropecuárias. A proximidade com centros maiores permite acesso a serviços de saúde e varejo. Projetos de melhoria da rede viária e saneamento têm prioridade na gestão municipal.",
    "Rio das Flores":"Rio das Flores é um município pitoresco, com forte apelo turístico e preservação das tradições históricas, especialmente do ciclo do café. A beleza natural, com rios e matas, atrai visitantes e inspira projetos ecológicos. Pequenos comércios e a rede hoteleira desenvolvem-se de forma sustentável. O setor cultural é ativo, com eventos que exaltam a história local e manifestações populares. A educação pública é valorizada e busca trazer mais oportunidades para a juventude. A administração local investe em políticas voltadas ao turismo rural e em infraestrutura básica.",
    "Valença":"Valença é um município de expressão no centro-sul fluminense, com economia diversificada que envolve comércio, agropecuária e turismo cultural. Com patrimônio arquitetônico preservado, oferece eventos musicais e festivais. A educação técnica e profissionalizante ganha destaque, assim como a formação de mão de obra local. Os serviços atendem bem à população e aos visitantes. Infraestrutura urbana inclui boa mobilidade e saneamento. Projetos de fomento cultural e estímulo à economia criativa estão em curso, buscando atrair investimentos.",
    "Volta Redonda":"Volta Redonda é conhecida como a 'Cidade do Aço', sede de uma das maiores siderúrgicas do país, que impulsiona sua economia. População expressiva e infraestrutura urbana avançada fazem dela um polo de serviços, comércio e cultura. A cidade investe em educação técnica voltada à indústria e programas sociais. O setor esportivo e cultural é forte, com grandes eventos e centros de lazer. O turismo industrial e de negócios permanece em ascensão. A gestão foca em sustentabilidade urbana e revitalização de áreas públicas."
}

# Criando abas manualmente
abas_municipios = st.tabs(municipios)

# Loop pelos municípios
for i, municipio in enumerate(municipios):
    with abas_municipios[i]:
        st.subheader(f"{municipio}")
        #st.write(descricoes_municipios.get(municipio, "Descrição não disponível."))  # Substitua com a descrição real
        #df_municipio_mapa = df_semacento[df_semacento["Município Empregador"] == municipio]

        nome_sem_acento = municipios_sem_acento[municipio]
        df_municipio_mapa = df_semacento[df_semacento["Município Empregador"] == nome_sem_acento]
        

        if municipio == "Geral":
            df_municipio2 = df2.copy()
            df_municipio_mapa = df_semacento.copy()
            st.write('A Região do Vale do Paraíba é uma importante faixa territorial localizada entre os estados do Rio de Janeiro, São Paulo e Minas Gerais, tendo o rio Paraíba do Sul como elemento central que conecta seus diversos municípios. Historicamente marcada pelo ciclo do café no século XIX, a região preserva traços coloniais e um rico patrimônio cultural, além de desenvolver-se fortemente ao longo das principais rotas de circulação do Sudeste brasileiro, como a Via Dutra (BR-116).No aspecto econômico, o Vale do Paraíba se destaca por sua diversidade produtiva, que vai desde a agricultura familiar e o turismo rural até polos industriais de grande porte, com forte presença da indústria automobilística, siderúrgica e de tecnologia. Cidades como Volta Redonda, Resende, São José dos Campos e Taubaté são exemplos de centros urbanos com infraestrutura consolidada e papel estratégico no desenvolvimento regional. A região também é conhecida pela sua paisagem montanhosa, áreas de proteção ambiental e por abrigar unidades de conservação como o Parque Nacional de Itatiaia. O turismo ecológico, religioso e histórico tem crescido como atividade complementar à economia.Socialmente, o Vale do Paraíba apresenta bons índices de escolarização e acesso a serviços urbanos, mas ainda enfrenta desafios relacionados à mobilidade, desigualdade social e crescimento urbano desordenado em algumas áreas. Iniciativas intermunicipais e consórcios regionais vêm sendo desenvolvidos para integrar políticas públicas e impulsionar o desenvolvimento sustentável e equilibrado da região.')
            
            #mapa 
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
                                height = 550)
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

        else:
            nome_sem_acento = municipios_sem_acento[municipio]
            df_municipio2 = df2[df2["Município Empregador"] == nome_sem_acento]
            df_municipio_mapa = df_semacento[df_semacento["Município Empregador"] == nome_sem_acento]
            info = df_info[df_info["Município"] == municipio]

            if not info.empty:
                info = info.iloc[0]

                col1, col2, col3 = st.columns(3)
                col1.metric("População", f"{int(info['População']):,}".replace(",", "."))
                col2.metric("Área (km²)", f"{info['Área']}")
                col3.metric("IDHM", f"{info['IDHM']:.3f}")

                col4, col5, col6 = st.columns(3)
                col4.metric("Densidade", f"{info['Densidade']} hab/km²")
                col5.metric("Escolarização", f"{info['Escolarização']}%")
                col6.metric("PIB", f"R$ {info['PIB']:,}".replace(",", "."))

            else:
                st.warning("Informações não encontradas para este município.")

        if municipio != "Geral" and not df_municipio_mapa.empty:
            col7,col8 = st.columns([1.2,1.5], gap='large')
            fig = px.choropleth_mapbox(
                data_frame=df_municipio_mapa,
                geojson=dfci,
                color="count",
                color_continuous_scale="greens",
                locations="Município Empregador",
                featureidkey="properties.name",
                center={"lat": -22.5, "lon": -44.1},  # ajuste conforme o município
                mapbox_style="carto-positron",
                zoom=8.2,
                opacity=1,
                hover_name="Município Empregador"
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(width=430, height=500, title='Mapa da Região')
            col8.plotly_chart(fig, use_container_width=True, key=f"mapa_{municipio}")
            col7.write(descricoes_municipios.get(municipio, "Descrição não disponível."))
            st.write('Fonte: IBGE')

        else:
            pass
        
        # Filtra o DataFrame para o município selecionado
        df_municipio2 = df2[df2["Município Empregador"] == municipio]
        
        # Abas internas para os gráficos
        abas_graficos = st.tabs(["Acidentes por Tempo","Acidentes por Idade", "CID", "CNAE"])  # Nome das abas dos gráficos, pode ser dinâmico também

        for j, nome_grafico in enumerate(["Acidentes por Tempo","Acidentes por Idade", "CID", "CNAE"]):  # Exemplo de gráficos
            with abas_graficos[j]:
                if not df_municipio2.empty:
                    if nome_grafico == "Acidentes por Tempo":
                        # Exemplo de gráfico PIP (usando a coluna 'Valor')
                        st.subheader('Distribuição de Acidentes no Tempo')
                        ##dados
                        df_municipio2['data'] = pd.to_datetime(df_municipio2['Data Acidente'])
                        df_municipio2['mes'] = df_municipio2['data'].dt.month
                        df_municipio2['ano'] = df_municipio2['data'].dt.year

                        df_contagem = df_municipio2['ano'].value_counts().reset_index()
                        df_contagem.columns = ['Ano', 'Contagem']

                        ##caixa de seleçao
                        anos = sorted(df_municipio2['ano'].unique())
                        opcoes = ['Geral'] + [str(ano) for ano in anos]
                        escolha = st.selectbox("Selecione o ano", opcoes,key=f"ano_select_{slugify(municipio)}")

                        if escolha == 'Geral':
                            dados_ano = df_municipio2['ano'].value_counts().sort_index()
                            fig = px.bar(x=dados_ano.index, y=dados_ano.values, labels={'x': 'Ano', 'y': 'Contagem'}, title='Distribuição por Ano')
                        else:
                            ano_escolhido = int(escolha)
                            df_filtrado = df_municipio2[df_municipio2['ano'] == ano_escolhido]
                            dados_mes = df_filtrado['mes'].value_counts().sort_index()
                            fig = px.bar(x=dados_mes.index, y=dados_mes.values, labels={'x': 'Mês', 'y': 'Contagem'}, title=f'Distribuição por Mês em {ano_escolhido}')
                            fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']))

                        fig.update_traces(texttemplate='%{y}', textposition='inside')
                        st.plotly_chart(fig, use_container_width=True, key=f"{nome_grafico}_{municipio}")
                    elif nome_grafico == "CNAE":
                        # Exemplo de gráfico CNAE (usando a coluna 'CNAE2.0 Empregador.1')
                        st.subheader("Distribuição de CNAE")
                        df_cnae = df_municipio2['CNAE2.0 Empregador.1'].value_counts().reset_index()
                        df_cnae.columns = ['CNAE2.0 Empregador.1', 'count']  # Renomeando para facilitar no gráfico

                        def grafico_atualizado2(n):
                            fig = px.bar(df_cnae.head(n), 
                                         x='CNAE2.0 Empregador.1', 
                                         y='count', 
                                         color='CNAE2.0 Empregador.1', 
                                         log_y=True)
                            return fig

                        # Usando o slider para escolher quantas categorias exibir
                        escolha2 = st.slider(label='Selecione a quantidade de informações',
                                            min_value=1,
                                            max_value=len(df_cnae),
                                            value=5,
                                            key=f"slider_{municipio}")

                        # Adicionando o key único para o gráfico para evitar o erro de ID duplicado
                        st.plotly_chart(grafico_atualizado2(escolha2), use_container_width=True, key=f"cnae_{municipio}")
                    
                    elif nome_grafico == "CID":
                        st.subheader("Distribuição de Ferimentos (CID)")
                        df_cid = df_municipio2['CID - Ferimento'].value_counts().reset_index()
                        def grafico_atualizado3(n):
                            fig23331 = px.bar(df_cid.head(n), 
                                y='count', 
                                x='CID - Ferimento',
                                color= 'CID - Ferimento',
                                log_y= True)
                            return fig23331  
                        
                        
                        # Usando o slider para escolher quantas categorias exibir
                        escolha3 = st.slider(label='Selecione a quantidade de informações',
                                            min_value=1,
                                            max_value=len(df_cid),
                                            value=5,
                                            key=f"slider2_{municipio}")
                        
                        st.plotly_chart(grafico_atualizado3(escolha3), use_container_width=True, key=f"cid_{municipio}")

                    elif nome_grafico == "Acidentes por Idade":
                        st.subheader('Distribuição dos Acidentes por Idade')

                        df_municipio2['Data Nascimento'] = pd.to_datetime(df_municipio2['Data Nascimento'])
                        df_municipio2['Data Acidente'] = pd.to_datetime(df_municipio2['Data Acidente'])
                        df_municipio2['Idade'] = df_municipio2['Data Acidente'] - df_municipio2['Data Nascimento']
                        df_municipio2['Idade2'] =  df_municipio2['Data Nascimento'] - df_municipio2['Data Acidente']
                        df_municipio2['Idade'] = df_municipio2['Idade'].dt.days
                        df_municipio2['Idade'] = df_municipio2['Idade'] / 365.25
                        df_municipio2['Idade'] = df_municipio2['Idade'].fillna(0)
                        df_municipio2['Idade'] = df_municipio2['Idade'].astype(int)

                        df_acidentes_limpo = df_municipio2[
                            (df_municipio2['Idade'] != 0) &
                            (df_municipio2['Sexo'] != 'Não Informado')].copy()

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
                        st.plotly_chart(fig33, use_container_width=True, key=f"{nome_grafico}_{municipio}")
                else:
                    st.write("Sem dados para exibir.")

