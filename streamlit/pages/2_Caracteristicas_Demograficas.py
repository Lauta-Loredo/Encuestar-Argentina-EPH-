import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📈 Caracteristicas Demográficas")

st.info("""En esta sección se visualizará información relacionada a la características demográficas de
la población argentina según la EPH.
""")

ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
st.divider()

def cargar_csv():
    df = pd.read_csv(ruta_csv_individuos, delimiter=";")
    columnas = ["ANO4","TRIMESTRE","CH06","CH04_str"]
    df = df[columnas]
    return df

df = cargar_csv()

#VALIDO LA EXISTENCIA DE LAS COLUMNAS
columnas = {"ANO4","TRIMESTRE","CH06","CH04_str"}
if not columnas.issubset(df.columns):
    st.error("El archivo no contiene las columnas necesarias")
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

#Creacion de los grupos de edad de 10 en 10:

#Creo una lista que va desde el 0 al 100 pero de 10 en 10
bins = list(range(0,101,10))

#Creo lista con etiquetas en formato str --> "i-i+9", para cada numero i en bins
labels = [f"{i}-{i+9}" for i in bins [:-1]]

#Creo columna en df llamada "grupo_edad", con .cut asigno un grupo de edad a cada persona
df_filtrado["grupo_edad"] = pd.cut(df_filtrado["CH06"], bins=bins, labels=labels, right=False)

#Agrupo el df por combinacion de grupo de edad y sexo ,y con
#.size() convierto el resultado de agrupacionen una columna nueva llamada cantidad
df_agrupado = df_filtrado.groupby(["grupo_edad","CH04_str"]).size().reset_index(name="cantidad")

#Definir para que cada sexo sea una columna
df_pivot = df_agrupado.pivot(index="grupo_edad",columns="CH04_str", values="cantidad").fillna(0)

#Grafico con bar_char

st.subheader(f"Cantidad de personas por grupo de edad (de a 10 años) y sexo ({anios}-T{trimestre})")
st.bar_chart(df_pivot)

st.divider()

