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

from datetime import datetime as dt
import src.funciones_streamlit.empleo as emp
from utils.constantes import (
    INDIVIDUOS_CSV,
    NIVEL_EDUCATIVO,
    NOMBRES_AGLOMERADOS,
    DATA_PATH,
    MAPA_PATH
)

reload(emp)

from src.funciones_streamlit.empleo import (
    muestra_tasa,
    calcular_desocupados_por_nivel,
    tasa_des_empleo,
    ocupados_por_nivel,
    tasa_aglomerado,
    colores_aglomerado,
    graficar_mapa,
)
from src.funciones_streamlit.funciones_en_comun import (
    crear_dataframe,
    selector_anio_trimestre,
    selector_aglomerados
)


st.set_page_config(layout="wide")
st.title("💼⚙️ Actividad y Empleo")
st.info(
    "En esta sección se visualizará información relacionada a la actividad y empleo según la EPH."
)

"""
Forzar recarga de datos cacheados en Streamlit cuando se actualiza algo, como un archivo o fuente de datos externa.
"""
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
st.divider()
mostrar_graficos = st.toggle("***Visualizar Datos Sobre Actividad y Empleo***", value=False)
if mostrar_graficos:
    # cargo datos
    df = crear_dataframe(INDIVIDUOS_CSV,COLUMNAS_NECESARIAS)
    st.markdown(
        "<h2 style='text-align: center;'>Información de personas desocupadas segun sus estudios alcanzados.</h2>",
        unsafe_allow_html=True,
    )
    if df is None:
        st.error("No se pudieron cargar los datos necesarios")
        st.stop
    # 1.5.1 Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados. Se debe informar para un año y trimestre elegido por el usuario
    anio, trimestre = selector_anio_trimestre(df, "1.5.1T")

    if anio not in ["Seleccione un año...", "Todos"] and trimestre:
        conteo = calcular_desocupados_por_nivel(df, anio, trimestre, NIVEL_EDUCATIVO)
        fig, ax = plt.subplots()
        ax.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
        ax.set_title("Distribución de desocupados según nivel educativo")
        st.pyplot(fig)
    else:
        st.warning("Por favor, elija año y trimestre.")

    st.divider()

    # 1.5.2 Informar la evolución del desempleo(tasa de desempleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
    st.markdown(
        "<h2 style='text-align: center;'>Evolucion de la tasa de desempleo segun aglomerado o país.</h2>",
        unsafe_allow_html=True,
    )
    tipo = "desempleo"
    aglomerado = selector_aglomerados("1.5.31")
    evolucion = tasa_des_empleo(df, tipo, aglomerado)
    muestra = muestra_tasa(tipo, evolucion)
    st.divider()

    # 1.5.3 Informar la evolución del empleo(tasa de empleo) a lo largo del tiempo. Se debe poder filtrar por aglomerado y en caso de no elegir ninguno se debe calcular para todo el país.
    st.markdown(
        "<h2 style='text-align: center;'>Evolucion de la tasa de empleo segun aglomerado o país.</h2>",
        unsafe_allow_html=True,
    )
    tipo = "empleo"
    aglomerado = selector_aglomerados("1.5.32")
    evolucion = tasa_des_empleo(df, tipo, aglomerado)
    muestra2 = muestra_tasa(tipo, evolucion)
    st.divider()

    # 1.5.4
    st.markdown(
        "<h2 style='text-align: center;'>Informacion por aglomerado sobre personas ocupadas y su tipo de ocupación.</h2>",
        unsafe_allow_html=True,
    )
    with st.expander("📊 Mostrar analisis por aglomerado"):
        df_resultado = ocupados_por_nivel(df)  
        st.dataframe(df_resultado)
    st.divider()

    # 1.5.5
    datos_path = DATA_PATH / "aglomerados_coordenadas.json"
    with open(datos_path, "r", encoding="utf-8") as f:
        coordenadas_aglomerado = json.load(f)

    tasas = tasa_aglomerado(df)
    tipo = st.selectbox(
        "Seleccioná el tipo de tasa que querés visualizar:",
        ("Seleccionar tasa...", "empleo", "desempleo"),
    )

    # Si el usuario no eligió nada válido, tipo será None
    if tipo == "Seleccionar tasa...":
        tipo = None
    st.markdown(
        "<p>- Al elegir la tasa de empleo se ven puntos verdes en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Rojo en el caso contrario. </p>"
        "<p>- Al elegir la tasa de desempleo se ven puntos rojos en los aglomerados cuya"
        "tasa de empleo aumentó con el correr del tiempo. Verde en el caso contrario. </p>",
        unsafe_allow_html=True,
    )
    if tipo:
        colores = colores_aglomerado(tipo, tasas)
        mapa = graficar_mapa(coordenadas_aglomerado,colores)
        mapa.save(MAPA_PATH)
        components.html(open(MAPA_PATH, "r", encoding="utf-8").read(), height=600)
    st.divider()
