import streamlit as st
from pathlib import Path

PAGES_DIR = Path("pages")  #Ruta relativa 

st.set_page_config(page_title='EPH Insight', layout='wide')
st.title("EPH Insight")

def main(): 
    st.info("""
    **Esta aplicación permite explorar y analizar los datos provenientes de la Encuesta Permanente de Hogares (EPH) de Argentina, una operación estadística continua realizada por el INDEC.  
    La EPH recopila información socioeconómica de los hogares urbanos en Argentina, datos como: empleo, ingresos, educación, características del hogar, integrantes, entre muchos más.**
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
    ("💼⚙️ ", "Actividad y Empleo", "4_Actividad_y_Empleo.py"),
    ("🧑‍🎓📚️", "Educación", "5_Educacion.py"),
    ("💰", "Ingresos", "6_Ingresos.py"),
]

for i, (icono, texto, archivo) in enumerate(secciones):
    with cols[i % 3]:
        st.markdown(f"### {icono} {texto}")
        st.page_link(str(PAGES_DIR / archivo), label="Acceder")

st.markdown("""
    <style>
    .footer-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ddd;
        border-top: 1px solid #bbb;
        z-index: 100;
    }

    .footer-container {
        max-width: 960px;
        margin: auto;
        padding: 10px 20px 10px 20px;  /* Menos padding vertical */
        font-size: 10pt;
        color: #333;
    }

    .footer-container h4 {
        font-size: 11pt;
        color: #222;
        margin: 0 0 5px 0;
    }

    .footer-container p {
        margin: 2px 0;
        text-align: justify;
    }

    .footer-container .footer-note {
        text-align: center;
        background-color: #ccc;
        padding: 6px;
        border-radius: 3px;
        margin-top: 8px;
        font-size: 9.5pt;
    }

    /* MÁS espacio inferior para evitar solapamiento */
    .main > div {
        padding-bottom: 220px;
    }
    </style>

    <div class="footer-wrapper">
        <div class="footer-container">
            <h4>Licencia MIT</h4>
            <p>
            Copyright (c) 2025 <strong>Grupo 26</strong>
            </p>
            <p>
            Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados...
            </p>
            <p class="footer-note">
            Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)