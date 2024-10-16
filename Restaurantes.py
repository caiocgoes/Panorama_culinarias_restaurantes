import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image 
import folium
from streamlit_folium import folium_static

#======
#codigo
#======

#----funções----#

def restaurants_unique(df):
   restaurantes_unicos = df["Restaurant ID"].nunique()
   return restaurantes_unicos
def Country_unique(df):
   paises_unicos = df["Country Code"].nunique()
   return paises_unicos
def City_unique(df):
   cidades_unicas = df["City"].nunique()
   return cidades_unicas
def Cuisines_unique(df):
   tipos_culinarias_unicos = df["Cuisines"].nunique()
   return tipos_culinarias_unicos
def Rating_unique(df):
   avaliacoes_unicas = df["Votes"].nunique()
   return avaliacoes_unicas
def clean_code(df):
    df = df.dropna()
    df = df.drop_duplicates()
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    df["Restaurant ID"] = df["Restaurant ID"].astype(object)
    df["Classificacao_preco_prato"] = df["Price range"]
    for i in df['Classificacao_preco_prato']:
        if i == 1:
           df["Classificacao_preco_prato"] = df['Classificacao_preco_prato'].replace(i, 'Barato') 
        elif i == 2:
           df["Classificacao_preco_prato"] = df['Classificacao_preco_prato'].replace(i, 'Normal')
        elif i == 3:
           df["Classificacao_preco_prato"] = df['Classificacao_preco_prato'].replace(i, 'Caro')
        else:
           df["Classificacao_preco_prato"] = df['Classificacao_preco_prato'].replace(i, 'Gourmet')

    for dado in df['Country Code']:
        if dado == 1:
           df["Country Code"] = df['Country Code'].replace(dado, 'India') 
        elif dado == 14:
           df["Country Code"] = df['Country Code'].replace(dado, 'Australia')
        elif dado == 30:
           df["Country Code"] = df['Country Code'].replace(dado, 'Brazil')
        elif dado == 37:
           df["Country Code"] = df['Country Code'].replace(dado, 'Canada')
        elif dado == 94:
           df["Country Code"] = df['Country Code'].replace(dado, 'Indonesia')
        elif dado == 148:
           df["Country Code"] = df['Country Code'].replace(dado, 'New Zeland')
        elif dado == 162:
           df["Country Code"] = df['Country Code'].replace(dado, 'Philippines')
        elif dado == 166:
           df["Country Code"] = df['Country Code'].replace(dado, 'Quatar')
        elif dado == 184:
           df["Country Code"] = df['Country Code'].replace(dado, 'Singapure')
        elif dado == 189:
           df["Country Code"] = df['Country Code'].replace(dado, 'South Africa')
        elif dado == 191:
           df["Country Code"] = df['Country Code'].replace(dado, 'Sri Lanka')
        elif dado == 208:
           df["Country Code"] = df['Country Code'].replace(dado, 'Turkey')
        elif dado == 214:
           df["Country Code"] = df['Country Code'].replace(dado, 'United Arab Emirates')
        elif dado == 215:
           df["Country Code"] = df['Country Code'].replace(dado, 'England')
        else:
           df["Country Code"] = df['Country Code'].replace(dado, 'United States of America')
    return df

#----dados-que-serão-usados---#

df1 = pd.read_csv('zomato.csv')

df = clean_code(df1)

#--barra-lateral--##

#---filtros---#

#---Pagina---#

tab1,tab2 = st.tabs(['Geral','Graficos'])

with tab1:
   with st.container():
       col1, col2, col3,col4,col5 = st.columns(5)
       with col1:
          st.metric("Restaurantes unicos cadastrados",restaurants_unique(df))
       with col2:
          st.metric("Paises unicos cadastrados",Country_unique(df))
       with col3:
          st.metric("Cidades unicas cadastradas",City_unique(df))
       with col4:
          st.metric("Culinarias unicas cadastradas",Cuisines_unique(df))
       with col5:
          st.metric("Avaliações registradas",Rating_unique(df))
