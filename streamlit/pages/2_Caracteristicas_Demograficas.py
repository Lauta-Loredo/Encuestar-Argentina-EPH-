import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import matplotlib.pyplot as plt

project_root = Path(__file__).parent.parent.parent/'src'
sys.path.append(str(project_root))

import funciones_streamlit.grupo_edad as ats

st.title("📈 Caracteristicas Demográficas")

st.info("""En esta sección se visualizará información relacionada a la características demográficas de
la población argentina según la EPH.
""")

#Primer punto de esta pagina
st.divider()

df = ats.anio_trimestre_seleccion()

if df is None:
    st.error('Ocurrio un Error Imprevisto')
    st.stop()

#Input año
anios_disponibles = sorted(df["ANO4"].unique())
anios = st.selectbox("Seleccione un año: ", anios_disponibles)
#Input trimestre
tri_disponible = sorted(df[df["ANO4"] == anios]["TRIMESTRE"].unique())
trimestre = st.selectbox("Seleccione un trimestre: ",tri_disponible)

#Filtro los datos
df_filtrado = df[(df["ANO4"] == anios) & (df["TRIMESTRE"] == trimestre)]

if df_filtrado.empty:
    st.warning("No hay datos disponibles para ese año y trimestre")
    st.stop

grafico = ats.grafico_barras_grup_edad(df_filtrado, anios, trimestre)

if grafico is None:
    st.error('Ocurrio un error al configurar el grafico')
    st.stop()

st.pyplot(grafico)

st.divider()

