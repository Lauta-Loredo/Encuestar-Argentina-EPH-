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
    st.warning('Por favor, elija año y trimestre')
st.divider()

# 1.5.2 Informar la evolución del desempleo(tasa de desempleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de desempleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)
tasa = "desempleo"
aglomerado = emp.definir_aglomerado(df, "1.5.31", cons.NOMBRES_AGLOMERADOS)
evolucion = emp.tasa_des_empleo(df,tasa, aglomerado)
muestra = emp.muestra_tasa(tasa,evolucion)
st.divider()

# 1.5.3 Informar la evolución del empleo(tasa de empleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de empleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)
tasa = "empleo"
aglomerado = emp.definir_aglomerado(df,"1.5.32", cons.NOMBRES_AGLOMERADOS)
evolucion = emp.tasa_des_empleo(df, tasa, aglomerado)
muestra2 = emp.muestra_tasa(tasa, evolucion)
st.divider()


