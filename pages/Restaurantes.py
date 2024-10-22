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
   
#   return mapa
def reviews_by_restaurants(df):
   restaurantecommaiorquantidadedeavaliacoes = df.loc[:,["Votes","Restaurant Name"]].groupby("Restaurant Name").sum().sort_values('Votes',ascending=False).reset_index().head(10)
   restaurantecommaiorquantidadedeavaliacoes.columns = ["Restaurante","Quantidade de avaliações"]
   fig_1 = px.bar(restaurantecommaiorquantidadedeavaliacoes, x="Restaurante", y="Quantidade de avaliações")
   return fig_1
def average_rating_by_restaurants(df):
   restaurantecommaiornotamedia = df.loc[:,["Aggregate rating","Restaurant Name"]].groupby("Restaurant Name").agg({"Aggregate rating":["mean","std"]}).reset_index().head(10)
   restaurantecommaiornotamedia.columns = ["Restaurante","Nota Média","Desvio Padrão"]
   fig_2 = px.bar(restaurantecommaiornotamedia, x="Restaurante", y="Nota Média")
   return fig_2
def average_price_for_two_by_restaurants(df):
   restaurantepratoparaduaspessoas = df.loc[:,["Average Cost for two","Restaurant Name"]].groupby("Restaurant Name").agg({"Average Cost for two":["mean","std"]}).reset_index().head(10)
   restaurantepratoparaduaspessoas.columns = ["Restaurante","Custo médio prato para duas pessoas","Desvio Padrão"]
   fig_3 = px.bar(restaurantepratoparaduaspessoas.sort_values('Custo médio prato para duas pessoas',ascending=False), x = 'Restaurante', y = 'Custo médio prato para duas pessoas')
   return fig_3
def unique_cuisines_by_restaurants(df):
   restaurantescomculinariasdistintas = df.loc[:,["Cuisines","Restaurant Name"]].groupby("Restaurant Name").nunique().reset_index().head(10)
   restaurantescomculinariasdistintas.columns = ["Restaurante","Quantidade_culinarias_distintas"]
   fig_4 = px.bar(restaurantescomculinariasdistintas.sort_values('Quantidade_culinarias_distintas',ascending=False),x='Restaurante',y='Quantidade_culinarias_distintas')
   return fig_4
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
   with st.container():
       latitude_media = df['Latitude'].mean()
       longitude_media = df['Longitude'].mean()

       mapa = folium.Map(location=[latitude_media, longitude_media], zoom_start=12)
      
       def definir_cor(aggregate_rating):
          if aggregate_rating >= 4.5:
             return 'darkgreen'
          elif 4.0 <= aggregate_rating < 4.5:
             return 'green'
          elif 3.5 <= aggregate_rating < 4.0:
             return 'lightgreen'
          elif 3.0 <= aggregate_rating < 3.5:
             return 'orange'
          elif 2.5 <= aggregate_rating < 3.0:
             return 'red'
          else:
             return 'darkred'

#Função para definir a cor com base em uma coluna (por exemplo, 'Aggregate rating')
       for index,row in df.iterrows():
           cor = definir_cor(row['Aggregate rating'])
           folium.Marker(
           location=[row['Latitude'], row['Longitude']],
           popup=row['Restaurant Name'],  
           icon=folium.Icon(color=cor)
       ).add_to(mapa)

       mapa.save('mapa_restaurantes.html')
      
       st.markdown("""Quantidade de avaliações por restaurante - Top 10 restaurantes""")

       folium_static(mapa)
      
       
with tab2:
   with st.container():
      col1, col2 = st.columns(2)
      with col1:
         fig_1 = reviews_by_restaurants(df)
         st.markdown("""Quantidade de avaliações por restaurante - Top 10 restaurantes""")
         st.plotly_chart(fig_1, use_container_width=True)
      with col2:
         fig_2 = unique_cuisines_by_restaurants(df)
         st.markdown("""Nota média por restaurante - Top 10 restaurantes""")
         st.plotly_chart(fig_2, use_container_width=True)
   with st.container():
      col1, col2 = st.columns(2)
      with col1:
         fig_3 = average_rating_by_restaurants(df)
         st.markdown("""Custo médio prato para duas pessoas por restaurante""")
         st.plotly_chart(fig_3, use_container_width=True)
      with col2:
         fig_4 = average_price_for_two_by_restaurants(df)
         st.markdown("""Quantidade de culinarias distintas por restaurante - Top 10 restaurantes""")
         st.plotly_chart(fig_4, use_container_width=True)

