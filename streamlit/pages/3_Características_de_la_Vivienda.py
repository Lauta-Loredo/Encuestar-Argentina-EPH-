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

from constantes import TIPOS_VIVIENDAS, NOMBRES_AGLOMERADOS, TIPOS_PISOS, UBICACION_BANIOS, DERECHO_PROPIEDAD

NOMBRES_AGLOMERADOS = {int(k): v for k, v in NOMBRES_AGLOMERADOS.items()}

UBICACION_BANIO = "IV9" 
TIPO_VIVIENDA = 'IV1' #Renombro IV1
TIPO_PISO = 'IV3'
PRIMER_ANIO = 2016 #Año desde que tenemos datos
archivo = 'HogaresTotal.csv' #Nombre del archivo csv a analizar

def filtrar_dataframe_por_anio(df_hogares):
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
        shadow=True,  #Agrego sombra
        explode=explode, #Cunata separacion tiene del grafico de torta
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


def material_predominante_por_aglomerado(df):
    import numpy as np

    # Prueba para comprabar que funciona
    #df.loc[:, TIPO_PISO] = np.random.randint(1, 4, size=len(df))
    
    predominantes = df.groupby('AGLOMERADO')[TIPO_PISO].apply(lambda x: x.mode().iloc[0])
    
    # Mapear a nombres
    predominantes = predominantes.map(TIPOS_PISOS)
    
    # Renombrar índice
    predominantes = predominantes.rename(index=NOMBRES_AGLOMERADOS)
    
    # Mostrar
    st.dataframe(predominantes.rename("Material Predominante"))

def proporcion_viviendas_banio(df):
    
    df_copy = df.copy()
    df_copy.loc[:, 'banio_interior'] = df[UBICACION_BANIO] == 1

    proporcion_banio = df_copy.groupby('AGLOMERADO')['banio_interior'].mean()
    
    proporcion_banio = proporcion_banio.rename(index = NOMBRES_AGLOMERADOS)
    
    # Lo pasamos a porcentaje
    proporcion_banio = (proporcion_banio * 100).round(2).sort_values(ascending=False)
    # Mostramos
    st.dataframe(proporcion_banio.rename("Porcentaje (%)"))

def evolucion_tenencia():
    c1,c2 = st.columns(2)
    with c1: 
        opciones_aglomerados = ['Seleccione un aglomerado...'] + sorted(NOMBRES_AGLOMERADOS.values())
        seleccion_aglomerado = st.selectbox('Selecione una aglomerado para visualizar su evolucion de tenencia',
                opciones_aglomerados)
    with c2:
        seleccion_tenencias = st.multiselect(
        'Seleccione los tipos de tenencia que desea visualizar:',
        options=list(DERECHO_PROPIEDAD.values())
        )

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

#Genero una lista con los años que hay desde 2016 hasta la actualidad para que el usuario elija el periodo.
for i in range((dt.now().year - PRIMER_ANIO) + 1):
    anio = PRIMER_ANIO + i
    anios.append(anio)

#Las opciones para el selectbox
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
    df = filtrar_dataframe_por_anio(df_hogares)
    if df is not  None:
        calcular_cantidad(df)
        
        st.divider()
        st.subheader('Tipos de Viviendas')
        grafico_tipo_de_viviendas(df)
        
        st.divider()
        st.subheader('Material de piso predominante por aglomerado')
        material_predominante_por_aglomerado(df)
        
        
        st.dataframe(df[TIPO_PISO])
        st.divider()
        st.subheader('Proporción de viviendas con baño dentro del hogar')
        proporcion_viviendas_banio(df)
        
        st.divider()
        evolucion_tenencia()
else: 
    st.write('Seleccione un año para poder trabajar con el dataframe.')

st.markdown("""<hr style="margin-top: 50px;">""", unsafe_allow_html=True)

st.markdown("""
<div style='
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 5px;
    font-size: 10pt; 
    text-align: justify; 
    color: #333;
'>
<h4 style='font-size: 11pt; color: #222;'>Licencia MIT</h4>
<p>
Copyright (c) 2025 <strong>Grupo 26</strong>
</p>
<p>
Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:
</p>
<p style='
    text-align: center; 
    background-color: #e9e9e9;
    padding: 10px;
    border-radius: 3px;
    margin-top: 15px;
'>
Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
</p>
</div>
""", unsafe_allow_html=True)