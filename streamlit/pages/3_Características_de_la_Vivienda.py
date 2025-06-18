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
    footer
)

reload(viviendas) 

# Ahora vuelves a importar lo que necesitas para que sean accesibles con las funciones recargadas:
from src.funciones_streamlit.viviendas import (
    calcular_cantidad,
    calcular_proporcion_tipo_viviendas,
    grafico_tipo_de_viviendas,
    calcular_material_predominante_por_aglomerado,
    informar_material_predominante,
    calcular_proporcion_viviendas_banio,
    informar_prop_banio_interior,
    informar_evolucion_tenencia,
    calcular_cantidad_viviendas_en_villas,
    informar_viviendad_en_villas,
    calcular_condicion_de_habitabilidad,
    informar_cond_habitabilidad
)

from utils.constantes import HOGARES_CSV
# Determina las columnas necesarias para el DF, asi no se sobrecarga la memoria
columnas_necesarias = ['ANO4','TRIMESTRE','PONDERA','AGLOMERADO','CONDICION_DE_HABITABILIDAD','IV1','IV3','IV9','IV12_3','II7']

# Invoca a la función y retorna el DF
df_hogares = crear_dataframe(HOGARES_CSV,columnas_necesarias)

# Verifica que el DF no este vacio
if df_hogares is not  None:
    
    # Selectbox para seleccionar un año
    anio_seleccionado = selector_anios(df_hogares,True)
    
    # Cuando el usuario selecciono el año, se filtra por el mismo
    if anio_seleccionado != 'Seleccione un año...':
        df = filtrar_dataframe_por_anio(df_hogares,anio_seleccionado)
        
        # Muestra la cantidad total de hogares en el periodo seleccionado
        calcular_cantidad(df,"**Cantidad de hogares en el periodo seleccionado**:")
        
        # Divide la pagina en tabs, mejora el orden
        tabs = st.tabs(['Tipos de Viviendas',
                                'Material de piso predominante por aglomerado',
                                'Prop. viviendas con baño dentro del hogar',
                                'Evolución tenencia',
                                'Viviendas ubicadas en villas de emergencia',
                                'Cond. habitabilidad por aglomerado'
                                ])
        
        with tabs[0]:
            grafico_tipo_de_viviendas(calcular_proporcion_tipo_viviendas(df))
        
        with tabs[1]:
            informar_material_predominante(calcular_material_predominante_por_aglomerado(df))

        with tabs[2]:
            informar_prop_banio_interior(calcular_proporcion_viviendas_banio(df))
        
        with tabs[3]:
            informar_evolucion_tenencia(df)
        
        with tabs[4]:
            informar_viviendad_en_villas(calcular_cantidad_viviendas_en_villas(df))
        
        with tabs[5]:
            informar_cond_habitabilidad(calcular_condicion_de_habitabilidad(df))
    else: 
        st.warning('Seleccione un periodo para poder trabajar con el dataframe.')

footer()
