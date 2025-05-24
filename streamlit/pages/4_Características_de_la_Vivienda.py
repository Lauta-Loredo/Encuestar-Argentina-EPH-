from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime as dt

st.set_page_config(layout='wide')
st.title("🏘️ Características de la vivienda")

ruta_utils = Path(__file__).parents[2] / 'utils'

# Agregar al path solo si no está y si existe
if ruta_utils.exists() and str(ruta_utils) not in sys.path:
    sys.path.append(str(ruta_utils))

from constantes import TIPOS_VIVIENDAS

TIPO_VIVIENDA = 'IV1' #Renombro IV1
PRIMER_ANIO = 2016 #Año desde que tenemos datos
archivo = 'HogaresTotal.csv' #Nombre del archivo csv a analizar

def filtar_dataframe_por_anio(df_hogares):
    #Filtro el dataframe según si se selecciono un año o todos
    if anio_seleccionado != 'Todos':
        df_filtrado = df_hogares[df_hogares['ANO4'] == anio_seleccionado]
        if df_filtrado.empty:
            st.write("⚠️ No hay datos para el año seleccionado.")
            return None
    else:
        df_filtrado = df_hogares    
    
    #Elimino el dataframe original, para liberar memoria
    del(df_hogares)
    return df_filtrado

def calcular_cantidad(df):
    cantidad_hogares = df.shape[0]
    st.write(f'La cantidad de hogares, en el periodo seleccionado, del dataframe es {cantidad_hogares}.')

def grafico_tipo_de_viviendas(df):
    tipos_viviendas = df[TIPO_VIVIENDA].value_counts().rename(index = TIPOS_VIVIENDAS)
    fig, ax = plt.subplots()

    explode = [0.01] * len(tipos_viviendas)

    texts, autotexts = ax.pie(
        tipos_viviendas,
        labels=None,  # quitamos labels del pie
        shadow=True,
        explode=explode,
    )
    etiquetas = [f"{nombre} -> {valor}" for nombre, valor in zip(tipos_viviendas.index, tipos_viviendas.values)]
    # Leyenda al costado, con etiquetas de los índices
    ax.legend(
        etiquetas,
        title="Tipos de Viviendas",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    ax.set_title('Proporción de viviendas por tipo')
    st.pyplot(fig)

def convertir_csv(df):
    # Convertir a CSV en memoria
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📁 Descargar CSV",
            data=csv,
            file_name="Hogares.csv",
            mime="text/csv"
        )

anios = []

for  i in range((dt.now().year +  - PRIMER_ANIO)+1): 
    anio = PRIMER_ANIO + i
    anios.append(anio)

opciones = ['Seleccione un año...'] + ['Todos'] +  sorted(anios, reverse=True)

st.divider()

#Selectbox para seleccionar un año en especifico o todos los años
anio_seleccionado = st.selectbox( 
    "Seleccione un año para explorar las características habitacionales de la población argentina:",
    opciones
)

#Genero el dataframe de hogares
df_hogares = pd.read_csv(ruta_utils/archivo, sep=';')
if anio_seleccionado != 'Seleccione un año...':
    df = filtar_dataframe_por_anio(df_hogares)
    if df is not  None:
        calcular_cantidad(df)
        st.divider()

        st.subheader('Tipos de Viviendas')
        grafico_tipo_de_viviendas(df)
        
        st.subheader('Material Predominante por Aglomerdo ')
        
else: 
    st.write('Seleccione un año para poder trabajar con el dataframe.')