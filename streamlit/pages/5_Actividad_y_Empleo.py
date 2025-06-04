from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime as dt

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"

import funciones_streamlit.empleo as emp
import utils.constantes as cons


st.set_page_config(layout="wide")
st.title("💼⚙️ Actividad y Empleo")
st.info("En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.")

st.divider()
st.markdown(
    "<h2 style='text-align: center;'>Informacion de personas desocupadas segun sus estudios alcanzados.</h2>",
    unsafe_allow_html=True,
)

# cargo datos
df = emp.cargar_df(ruta_csv_individuos)

# 1.5.1 Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados. Se debe informar para un año y trimestre elegido por el usuario
anio, trimestre = emp.definir_año()
if anio and trimestre:
    conteo = emp.calcular_desocupados_por_nivel(df, anio, trimestre, cons.NIVEL_EDUCATIVO)
    fig, ax = plt.subplots()
    ax.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
    ax.set_title("Distribución de desocupados según nivel educativo")
    st.pyplot(fig)
else:
    st.warning('Por favor, elija año y trimestre')
st.divider()
