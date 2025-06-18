from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from importlib import reload
import streamlit.components.v1 as components

import json
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
ruta_csv_individuos = (
    Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
)

from datetime import datetime as dt
import src.funciones_streamlit.empleo as emp
import utils.constantes as cons
reload(emp)

from src.funciones_streamlit.empleo import (
    definir_anio,
    definir_trimestre,
    muestra_tasa,
    calcular_desocupados_por_nivel,
    definir_aglomerado,
    tasa_des_empleo,
    ocupados_por_nivel,
    tasa_aglomerado,
    colores_aglomerado,
    graficar_mapa,
    footer
)
from src.funciones_streamlit.funciones_en_comun import (
    crear_dataframe
)


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

COLUMNAS_NECESARIAS = [
    "ESTADO",
    "NIVEL_ED",
    "ANO4",
    "TRIMESTRE",
    "AGLOMERADO",
    "PP04A",
    "PONDERA",
]

# cargo datos
df = crear_dataframe(ruta_csv_individuos,COLUMNAS_NECESARIAS)

# 1.5.1 Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados. Se debe informar para un año y trimestre elegido por el usuario
anio = definir_anio(df, "1.5.1A")
trimestre = definir_trimestre(df, anio, "1.5.1T")
if anio and trimestre:
    conteo = calcular_desocupados_por_nivel(df, anio, trimestre, cons.NIVEL_EDUCATIVO)
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
tipo = "desempleo"
aglomerado = definir_aglomerado(df, "1.5.31", cons.NOMBRES_AGLOMERADOS)
evolucion = tasa_des_empleo(df, tipo, aglomerado)
muestra = muestra_tasa(tipo, evolucion)
st.divider()

# 1.5.3 Informar la evolución del empleo(tasa de empleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
st.markdown(
    "<h2 style='text-align: center;'>Evolucion de la tasa de empleo segun aglomerado o país.</h2>",
    unsafe_allow_html=True,
)
tipo = "empleo"
aglomerado = definir_aglomerado(df, "1.5.32", cons.NOMBRES_AGLOMERADOS)
evolucion = tasa_des_empleo(df, tipo, aglomerado)
muestra2 = muestra_tasa(tipo, evolucion)
st.divider()

# 1.5.4
st.markdown(
    "<h2 style='text-align: center;'>Informacion por aglomerado sobre personas ocupadas y su tipo de ocupación.</h2>",
    unsafe_allow_html=True,
)

df_resultado = ocupados_por_nivel(df)  
st.dataframe(df_resultado)
st.divider()
# 1.5.5
datos_path = cons.DATA_PATH / "aglomerados_coordenadas.json"
with open(datos_path, "r", encoding="utf-8") as f:
    coordenadas_aglomerado = json.load(f)

tasas = tasa_aglomerado(df)
tipo = st.selectbox("Seleccioná el tipo de tasa que querés visualizar:", ("empleo", "desempleo"))
st.markdown(
    "<p>- Al elegir la tasa de empleo se ven puntos verdes en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Rojo en el caso contrario. </p>"
    "<p>- Al elegir la tasa de desempleo se ven puntos rojos en los aglomerados cuya"
    "tasa de empleo aumentó con el correr del tiempo. Verde en el caso contrario. </p>",
    unsafe_allow_html=True,
)
colores = colores_aglomerado(tipo, tasas)
mapa = graficar_mapa(coordenadas_aglomerado,colores)
MAPA_PATH = cons.UTILS_PATH / "mapa_aglomerados.html"
mapa.save(MAPA_PATH)
components.html(open(MAPA_PATH, "r", encoding="utf-8").read(), height=600)
st.divider()
# footer
footer()
