import streamlit as st
from pathlib import Path

# Configuración general de la página
st.set_page_config(page_title='EPH Insight', layout='wide')
st.title("EPH Insight")

# Ruta relativa para los links
PAGES_DIR = Path("pages")

tab1, tab2 = st.tabs(["🏠 Inicio", "📄 Información Legal"])

# TAB 1: Página de inicio con links
with tab1:
    st.info("""
    **Esta aplicación permite explorar y analizar los datos provenientes de la Encuesta Permanente de Hogares (EPH) de Argentina, una operación estadística continua realizada por el INDEC.  
    La EPH recopila información socioeconómica de los hogares urbanos en Argentina, datos como: empleo, ingresos, educación, características del hogar, integrantes, entre muchos más.**
    """)

    st.divider()

    cols = st.columns(3)
    secciones = [
        ("⬆️", "Carga de Datos", "1_Carga_de_Datos.py"),
        ("📊", "Características Demográficas", "2_Caracteristicas_Demograficas.py"),
        ("🏘️", "Características de la Vivienda", "3_Características_de_la_Vivienda.py"),
        ("💼⚙️", "Actividad y Empleo", "4_Actividad_y_Empleo.py"),
        ("🧑‍🎓📚️", "Educación", "5_Educacion.py"),
        ("📈💸", "Línea de Pobreza e Indigencia", "6_Ingresos_Pobreza.py"),

    ]

    for i, (icono, texto, archivo) in enumerate(secciones):
        with cols[i % 3]:
            st.markdown(f"### {icono} {texto}")
            st.page_link(str(PAGES_DIR / archivo), label="Acceder")

# TAB 2: Información legal y autores
with tab2:
    st.subheader("Licencia MIT")
    st.markdown("""
    **Copyright (c) 2025 [Grupo 26]**

    Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:

    El aviso de copyright anterior y este aviso de permiso deberán incluirse en todas las copias o partes sustanciales del Software.

    **EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO**, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITÁNDOSE A LAS GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O LOS TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑO O OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE OTRO TIPO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.
    """)

    # Sección centrada vertical y horizontalmente
    st.markdown("""
    <div style="height: 40vh; display: flex; align-items: center; justify-content: center;">
        <div style="text-align: center;">
            <h4>Desarrollado por</h4>
            <p>Lucentini Joaquin | Loredo Lautaro | Rodriguez Ulises | Morano Axel Martin | Arrechea Diego</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


