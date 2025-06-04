from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"

from datetime import datetime as dt
import funciones_streamlit.empleo as emp
import utils.constantes as cons


st.set_page_config(layout="wide")
st.title("💼⚙️ Actividad y Empleo")
st.info("En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.")

st.divider()
st.markdown(
    "<h2 style='text-align: center;'>Información de personas desocupadas segun sus estudios alcanzados.</h2>",
    unsafe_allow_html=True,
)

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
    st.warning('Por favor, elija año y trimestre')
st.divider()

# 1.5.2 Informar la evolución del desempleo(tasa de desempleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de desempleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)

aglomerado = emp.definir_aglomerado(df,cons.NOMBRES_AGLOMERADOS)
evolucion = emp.tasa_desempleo(df, aglomerado)
if evolucion:
    anios = list(evolucion.keys())
    tasas = list(evolucion.values())
    plt.plot(anios, tasas)
    fig, ax = plt.subplots()
    ax.bar(anios, tasas)
    ax.set_xlabel("Año")
    ax.set_ylabel("Tasa de desempleo (%)")
    ax.set_title("Evolución de la tasa de desempleo")
    st.pyplot(fig)
    st.divider()
else:
    st.warning("Por favor, elije una opción")