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

def restaurants_by_city(df):
   cidadecommaisrestourantesregistrados = df.sort_values('Restaurant ID', ascending = True).loc[:,["Restaurant ID","City"]].groupby("City").count().sort_values('Restaurant ID',ascending=False).reset_index().head(10)
   cidadecommaisrestourantesregistrados.columns = ["Cidade","Quantidade_de_restaurantes"]
   fig_1 = px.bar(cidadecommaisrestourantesregistrados, x = 'Cidade', y = 'Quantidade_de_restaurantes' )
   return fig_1
def restaurants_average_above_4_by_city(df):
   cidadecommaisrestourantesregistradoscomnotaquatro = df.loc[df["Aggregate rating"] > 4,:].loc[:,["Restaurant ID","City"]].groupby("City").count().sort_values('Restaurant ID',ascending = False).reset_index().head(10)
   cidadecommaisrestourantesregistradoscomnotaquatro.columns = ["Cidade","Quantidade_de_restaurantes"]
   fig_2 = px.bar(cidadecommaisrestourantesregistradoscomnotaquatro, x= 'Cidade', y = 'Quantidade_de_restaurantes')
   return fig_2
def average_price_for_two_by_citys(df):
   cidadecommaiormediadevalordepratopradois = df.loc[:,["Average Cost for two","City"]].groupby("City").agg({"Average Cost for two":["mean","std"]}).reset_index().head(10)
   cidadecommaiormediadevalordepratopradois.columns = ["Cidade","Media_de_prato_para_dois","Desvio Padrão"]
   fig_3 = px.bar(cidadecommaiormediadevalordepratopradois.sort_values('Media_de_prato_para_dois',ascending=False), x = 'Cidade', y = 'Media_de_prato_para_dois')
   return fig_3
def cuisines_unique_by_country(df):
   cidadecommaisculinariadistinta = df.loc[:,["Cuisines","City"]].groupby("City").nunique().sort_values('Cuisines',ascending=False).reset_index().head(10)
   cidadecommaisculinariadistinta.columns = ["Cidade","Quantidade_de_tipos_de_culinarias"]
   fig_4 = px.bar(cidadecommaisculinariadistinta, x = 'Cidade', y = 'Quantidade_de_tipos_de_culinarias')
   return fig_4
def restaurants_has_table_booking_by_city(df):
   cidadequepossuimaiorquantidadederestourantesreserva = df.loc[df["Has Table booking"]==1,:].loc[:,["Restaurant ID","City"]].groupby("City").count().sort_values('Restaurant ID',ascending=False).reset_index().head(10)
   cidadequepossuimaiorquantidadederestourantesreserva.columns = ["Cidade","Quantidade_restaurantes_fazem_reserva"]
   fig_5 = px.bar(cidadequepossuimaiorquantidadederestourantesreserva, x = 'Cidade', y = 'Quantidade_restaurantes_fazem_reserva')
   return fig_5
def restaurants_delivery_by_city(df):
   cidadecommaiorquantidadederestourantesquefazementrega = df.loc[df["Is delivering now"]==1,:].loc[:,["Restaurant ID","City"]].groupby("City").count().sort_values('Restaurant ID',ascending=False).reset_index().head(10)
   cidadecommaiorquantidadederestourantesquefazementrega.columns = ["Cidade","Quantidade_de_restaurantes"]
   fig_6 = px.bar(cidadecommaiorquantidadederestourantesquefazementrega,x='Cidade',y='Quantidade_de_restaurantes')
   return fig_6
def restaurants_online_booking_by_city(df):
   cidadesqueaceitampedidosonline = df.loc[df["Has Online delivery"]==1,:].loc[:,["Restaurant ID","City"]].groupby("City").count().sort_values('Restaurant ID',ascending=False).reset_index().head(10)
   cidadesqueaceitampedidosonline.columns = ["Cidade","Quantidade_de_restaurantes"]
   fig_7 = px.bar(cidadesqueaceitampedidosonline, x = "Cidade", y = 'Quantidade_de_restaurantes')
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
         fig_1 = restaurants_by_city(df)
         st.markdown(""" Quantidade de restaurantes por cidades """)
         st.plotly_chart(fig_1, use_container_width=True)
       with col2:
         fig_2 = restaurants_average_above_4_by_city(df)
         st.markdown(""" Culinarias de restaurantes com nota acima de 4 por cidades """)
         st.plotly_chart(fig_2, use_container_width=True)
   with st.container():
       col3,col4 = st.columns(2)
       with col3:
         fig_3 = average_price_for_two_by_citys(df)
         st.markdown(""" Media de prato para dois por cidades """)
         st.plotly_chart(fig_3, use_container_width=True)
       with col4:
         fig_4 = cuisines_unique_by_country(df)
         st.markdown(""" Quantidade de tipos de culinarias diferentes por cidades """)
         st.plotly_chart(fig_4, use_container_width=True)
with tab2:
   with st.container():
       col5, col6, col7 = st.columns(3)
       with col5:
         fig_5 = restaurants_has_table_booking_by_city(df)
         st.markdown(""" Quantidade de restaurantes que fazem reservas por cidades """)
         st.plotly_chart(fig_5, use_container_width=True)
       with col6:   
         fig_6 = restaurants_online_booking_by_city(df)
         st.markdown(""" Quantidade de restaurantes que aceitam pedidos online por cidades """)
         st.plotly_chart(fig_6, use_container_width=True)
   with st.container():
       col7,col8 = st.columns(2)
       with col7:
         fig_7 = average_price_for_two_by_citys(df)
         st.markdown(""" Quantidade de restaurantes que fazem entrega por cidades""")
         st.plotly_chart(fig_7, use_container_width=True)
    
       #with col8:
       #  fig_8 = cuisines_by_country(df)
       #  st.markdown("""Culinarias por pais""")
       #  st.plotly_chart(fig_8, use_container_width=True)


