from pathlib import Path
import sys
import os
import streamlit as st
from importlib import reload

st.set_page_config(layout='wide')
st.title("🏘️ Características de la vivienda")
st.markdown(
    "En esta sección se visualiza información relacionada con las características habitacionales de la población argentina según los datos de la EPH. "
    "Podés seleccionar un año específico para analizar o elegir ver todos los períodos disponibles en el sistema."
)
st.divider()

sys.path.append(os.path.abspath("../code"))

import src.funciones_streamlit.viviendas as viviendas
import src.funciones_streamlit.funciones_en_comun as funciones_en_comun

reload(funciones_en_comun)

from src.funciones_streamlit.funciones_en_comun import (
    crear_dataframe,
    selector_anios,
    filtrar_dataframe_por_anio,
    footer,

)

reload(viviendas) 

# Ahora vuelves a importar lo que necesitas para que sean accesibles con las funciones recargadas:
from src.funciones_streamlit.viviendas import (
    calcular_cantidad,
    grafico_tipo_de_viviendas,
    material_predominante_por_aglomerado,
    proporcion_viviendas_banio,
    evolucion_tenencia,
    cantidad_viviendas_en_villas,
    condiciones_de_habitabilidad,
)

df_hogares = crear_dataframe()

if df_hogares is not  None:
    anio_seleccionado = selector_anios(df_hogares)
    if anio_seleccionado != 'Seleccione un año...':
        df = filtrar_dataframe_por_anio(df_hogares,anio_seleccionado)
        calcular_cantidad(df,"**Cantidad de hogares en el periodo seleccionado**:")
    
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
