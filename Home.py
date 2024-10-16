import streamlit as st
from PIL import Image


st.set_page_config(page_title = "Home",page_icon="U+1F4C8", layout="wide")#função que iremos usar usar para configuração de nossa imagem 
#image_path = 'c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/logo.png'
#image = Image.open(image_path)
#st.sidebar.image( image,width=120)

st.sidebar.markdown('# Caio Góes Projetos')
st.sidebar.markdown('## Panorama de culinarias e restaurantes')
st.sidebar.markdown("""---""")

st.write("# Dashboard de analise")

st.markdown("""O dashboard tem como objetivo mostrar um panorama geral de restaurantes e culinarias, categorizados por pais e cidade. Os datos foram extraidos da plataforma kangle""")