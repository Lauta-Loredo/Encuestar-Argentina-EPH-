from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
ruta_csv_individuos = (
    Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
)

from datetime import datetime as dt
import funciones_streamlit.empleo as emp
import utils.constantes as cons


st.set_page_config(layout="wide")
st.title("💼⚙️ Actividad y Empleo")
st.info(
    "En esta sección se visualizará información relacionada a la actividad y empleo según la EPH."
)

st.divider()
st.markdown(
    "<h2 style='text-align: center;'>Información de personas desocupadas segun sus estudios alcanzados.</h2>",
    unsafe_allow_html=True,
)

if st.session_state.get("datos_actualizados", False):
    st.cache_data.clear()  # fuerza recarga
    st.session_state["datos_actualizados"] = False


# cargo datos
df = emp.cargar_df(ruta_csv_individuos)

# 1.5.1 Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados. Se debe informar para un año y trimestre elegido por el usuario
anio = emp.definir_anio(df, "1.5.1A")
trimestre = emp.definir_trimestre(df, anio, "1.5.1T")
if anio and trimestre:
    conteo = emp.calcular_desocupados_por_nivel(df, anio, trimestre, cons.NIVEL_EDUCATIVO)
    fig, ax = plt.subplots()
    ax.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
    ax.set_title("Distribución de desocupados según nivel educativo")
    st.pyplot(fig)
else:
    st.warning("Por favor, elija año y trimestre")
st.divider()

# 1.5.2 Informar la evolución del desempleo(tasa de desempleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de desempleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)
tasa = "desempleo"
aglomerado = emp.definir_aglomerado(df, "1.5.31", cons.NOMBRES_AGLOMERADOS)
evolucion = emp.tasa_des_empleo(df, tasa, aglomerado)
muestra = emp.muestra_tasa(tasa, evolucion)
st.divider()

# 1.5.3 Informar la evolución del empleo(tasa de empleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de empleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)
tasa = "empleo"
aglomerado = emp.definir_aglomerado(df, "1.5.32", cons.NOMBRES_AGLOMERADOS)
evolucion = emp.tasa_des_empleo(df, tasa, aglomerado)
muestra2 = emp.muestra_tasa(tasa, evolucion)
st.divider()

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)
