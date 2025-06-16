from pathlib import Path
import sys
import os
import streamlit as st
import pandas as pd
from importlib import reload

from datetime import datetime as dt

st.set_page_config(layout='wide')
st.title("🏘️ Características de la vivienda")
sys.path.append(os.path.abspath("../code"))

from utils.constantes import (
    UTILS_PATH,
    HOGARES_CSV
)

import src.funciones_streamlit.viviendas as viviendas

reload(viviendas)

# Ahora vuelves a importar lo que necesitas para que sean accesibles con las funciones recargadas:
from src.funciones_streamlit.viviendas import (
    selector_anios,
    filtrar_dataframe_por_anio,
    calcular_cantidad,
    grafico_tipo_de_viviendas,
    material_predominante_por_aglomerado,
    proporcion_viviendas_banio,
    evolucion_tenencia,
    cantidad_viviendas_en_villas,
    condiciones_de_habitabilidad,
    footer
)

df_hogares = None

try:
    #Genero el dataframe de hogares
    df_hogares = pd.read_csv(UTILS_PATH/HOGARES_CSV, sep=';', low_memory=False)
except FileNotFoundError:
    st.error(f"Error: archivo CSV no encontrado")
except pd.errors.ParserError:  # Usá este en lugar de csv.Error para pandas
    st.error(" Error al leer el archivo CSV")
except Exception as e:
    st.error(f" Ocurrió una excepción inesperada: {e} ({type(e).__name__})")

st.divider()

anio_seleccionado = selector_anios(df_hogares)

if anio_seleccionado != 'Seleccione un año...':
    if df_hogares is not  None:
        df = filtrar_dataframe_por_anio(df_hogares,anio_seleccionado)
        calcular_cantidad(df)
        
        tabs = st.tabs(['Tipos de Viviendas',
                                'Material de piso predominante por aglomerado',
                                'Prop. viviendas con baño dentro del hogar',
                                'Evolución tenencia',
                                'Viviendas ubicadas en villas de emergencia',
                                'Cond. habitabilidad por aglomerado'
                                ])
        
        with tabs[0]:
            grafico_tipo_de_viviendas(df)
        
        with tabs[1]:
            material_predominante_por_aglomerado(df)
        
        with tabs[2]:
            proporcion_viviendas_banio(df)
        
        with tabs[3]:
            evolucion_tenencia(df)
        
        with tabs[4]:
            cantidad_viviendas_en_villas(df)
        
        with tabs[5]:
            condiciones_de_habitabilidad(df)
else: 
    st.warning('Seleccione un periodo para poder trabajar con el dataframe.')

footer()
