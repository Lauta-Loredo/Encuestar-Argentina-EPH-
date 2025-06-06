import streamlit as st
from pathlib import Path

PAGES_DIR = Path("pages")  #Ruta relativa 

st.set_page_config(page_title='EPH Insight', layout='wide')
st.title("EPH Insight")

def main(): 
    st.info("""
    Esta aplicación permite explorar y analizar los datos provenientes de la Encuesta Permanente de Hogares (EPH) de Argentina, una operación estadística continua realizada por el INDEC.  
    La EPH recopila información socioeconómica de los hogares urbanos en Argentina, datos como: empleo, ingresos, educación, características del hogar, integrantes, entre muchos más.
    """) 

if __name__ == '__main__':
    main()


st.divider()

# Secciones del dashboard
cols = st.columns(3)
secciones = [
    ("⬆️", "Carga de Datos", "1_Carga_de_Datos.py"),
    ("📊", "Características Demográficas", "2_Caracteristicas_Demograficas.py"),
    ("🏘️", "Características de la Vivienda", "3_Características_de_la_Vivienda.py"),
    ("💼", "Actividad y Empleo", "4_Actividad_y_Empleo.py"),
    ("🎓", "Educación", "5_Educacion.py"),
    ("💰", "Ingresos", "6_Ingresos.py"),
]

for i, (icono, texto, archivo) in enumerate(secciones):
    with cols[i % 3]:
        st.markdown(f"### {icono} {texto}")
        st.page_link(str(PAGES_DIR / archivo), label="Acceder")

st.markdown("""<hr style="margin-top: 50px;">""", unsafe_allow_html=True)

st.markdown("""
<div style='
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 5px;
    font-size: 10pt; 
    text-align: justify; 
    color: #333;
'>
<h4 style='font-size: 11pt; color: #222;'>Licencia MIT</h4>
<p>
Copyright (c) 2025 <strong>Grupo 26</strong>
</p>
<p>
Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:
</p>
<p style='
    text-align: center; 
    background-color: #e9e9e9;
    padding: 10px;
    border-radius: 3px;
    margin-top: 15px;
'>
Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
</p>
</div>
""", unsafe_allow_html=True)
