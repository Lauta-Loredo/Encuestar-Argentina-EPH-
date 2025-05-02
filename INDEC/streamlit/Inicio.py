import streamlit as st
from pathlib import Path

PAGES_DIR = Path("pages")  #Ruta relativa 

st.set_page_config(page_title='EPH Insight', layout='wide')
st.title("EPH Insight")

def main(): 
    st.info("""
    Esta aplicación va permitir explorar y analizar los datos provenientes de la Encuesta Permanente de Hogares (EPH) de Argentina, una operación estadística continua realizada por el INDEC.  
    La EPH recopila información socioeconómica de los hogares urbanos en Argentina, datos como: empleo, ingresos, educación, características del hogar, integrantes, entre muchos más.
    """) 

if __name__ == '__main__':
    main()

st.divider()

c1,c2,c3 = st.columns(3)

with c1:
    st.page_link(str(PAGES_DIR / '1_Carga_de_Datos.py'), label= 'Carga de Datos',icon='⬆️')
with c2:
    st.page_link(str(PAGES_DIR / '2_Busqueda_por_Temas.py'), label= 'Busqueda por Temas',icon='🔎')
with c3:
    st.page_link(str(PAGES_DIR / '3_Visualizacion.py'), label= 'Carga de Datos',icon='📊')