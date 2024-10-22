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

def restaurants_by_country(df):
   agrupamento_restourantes_por_pais = df.loc[:,["Restaurant ID","Country Code"]].groupby("Country Code").count().sort_values('Restaurant ID',ascending=False).reset_index()
   agrupamento_restourantes_por_pais.columns = ["Pais","Quantidade_de_restaurantes"]
   fig_1 = px.bar(agrupamento_restourantes_por_pais, x = 'Pais', y = 'Quantidade_de_restaurantes')
   return fig_1
def Cuisines_unique_by_country(df):
   paiscommaiorquantidadecolunariasdistintas = df.loc[:,["Cuisines","Country Code"]].groupby("Country Code").nunique().sort_values('Cuisines',ascending=False).reset_index()
   paiscommaiorquantidadecolunariasdistintas.columns = ["Pais","Quantidade_de_culinarias_unicas"]
   fig_2 = px.bar(paiscommaiorquantidadecolunariasdistintas,x='Pais',y='Quantidade_de_culinarias_unicas')
   return fig_2
def reviews_by_country(df):
   paiscommaiorquantidadedeavaliacoes = df.loc[:,["Votes","Country Code"]].groupby("Country Code").sum().sort_values('Votes',ascending=False).reset_index()
   paiscommaiorquantidadedeavaliacoes.columns = ["Pais","Avaliações_registradas"]
   fig_3 =px.bar(paiscommaiorquantidadedeavaliacoes, x='Pais',y='Avaliações_registradas')
   return fig_3
def restaurants_delivery_by_country(df):
   paiscommaiorquantidadederestourantesfazementrega = df.loc[df["Is delivering now"]==1,:].loc[:,["Restaurant ID","Country Code"]].groupby("Country Code").count().sort_values('Restaurant ID',ascending=False).reset_index()
   paiscommaiorquantidadederestourantesfazementrega.columns = ["Pais","Quantidade_de_restaurantes"]
   fig_4 = px.bar(paiscommaiorquantidadederestourantesfazementrega, x = 'Pais', y = 'Quantidade_de_restaurantes')
   return fig_4
def average_review_by_country(df):
   paiscommaiormediadeavaliacoes = df.loc[:,["Votes","Country Code"]].groupby("Country Code").agg({'Votes':['mean','std']}).reset_index()
   paiscommaiormediadeavaliacoes.columns = ["Pais","Media_quantidade_avaliações","Desvio Padrão"]
   fig_5 = px.bar(paiscommaiormediadeavaliacoes.sort_values('Media_quantidade_avaliações',ascending=False),x='Pais',y='Media_quantidade_avaliações')
   return fig_5
def average_rating_by_country(df):
   paiscommaiormediaemnota = df.loc[:,["Aggregate rating","Country Code"]].groupby("Country Code").agg({'Aggregate rating':["mean","std"]}).reset_index()
   paiscommaiormediaemnota.columns = ["Pais","Nota_media","Desvio Padrão"]
   fig_6 = px.bar(paiscommaiormediaemnota.sort_values('Nota_media',ascending=False).head(5),x='Pais',y='Nota_media')
   return fig_6
def average_price_for_two_by_country(df):
   mediaprecopratoparadoisporpais = df.loc[:,["Average Cost for two","Country Code"]].groupby("Country Code").agg({'Average Cost for two':["mean","std"]}).reset_index()
   mediaprecopratoparadoisporpais.columns = ["Pais","Media_preço_prato_para_dois","Desvio Padrão"]
   fig_7 = px.bar(mediaprecopratoparadoisporpais.sort_values('Media_preço_prato_para_dois',ascending=False),x='Pais',y='Media_preço_prato_para_dois')
   return fig_7
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

tab1,tab2 = st.tabs(['Primeiras medidas','Segundas medidas'])

with tab1:
   with st.container():
       col1, col2 = st.columns(2)
       with col1:
         fig_1 = restaurants_by_country(df)
         st.markdown("""Quantidade de restaurantes por Pais """)
         st.plotly_chart(fig_1, use_container_width=True)
       with col2:
         fig_2 = restaurants_by_country(df)
         st.markdown("""Culinarias unicas por pais""")
         st.plotly_chart(fig_2, use_container_width=True)
   with st.container():
       col3,col4 = st.columns(2)
       with col3:
         fig_3 = reviews_by_country(df)
         st.markdown("""Avaliações por pais""")
         st.plotly_chart(fig_3, use_container_width=True)
       with col4:
         fig_4 = restaurants_delivery_by_country(df)
         st.markdown("""Restaurantes que fazem entrega por pais - Top 4 paises""")
         st.plotly_chart(fig_4, use_container_width=True)
with tab2:
   with st.container():
       col5, col6, col7 = st.columns(3)
       with col5:
         fig_5 = average_review_by_country(df)
         st.markdown("""Média de avaliações por pais""")
         st.plotly_chart(fig_5, use_container_width=True)
       with col6:   
         fig_6 = average_rating_by_country(df)
         st.markdown("""Nota média por pais - Top 5 Paises""")
         st.plotly_chart(fig_6, use_container_width=True)
   with st.container():
       col7,col8 = st.columns(2)
       with col7:
         fig_7 = average_price_for_two_by_country(df)
         st.markdown("""Custo médio prato para duas pessoas por pais""")
         st.plotly_chart(fig_7, use_container_width=True)
       #with col8:
       #  fig_8 = cuisines_by_country(df)
       #  st.markdown("""Culinarias por pais""")
       #  st.plotly_chart(fig_8, use_container_width=True)


