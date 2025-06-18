from pathlib import Path
import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


sys.path.append(os.path.abspath("../code"))

from src.funciones_streamlit.funciones_en_comun import (
    selector_aglomerados,
    convertir_csv
)
from utils.constantes import (
    TIPOS_VIVIENDAS, 
    NOMBRES_AGLOMERADOS, 
    TIPOS_PISOS, 
    UBICACION_BANIOS, 
    DERECHO_PROPIEDAD
)

NOMBRES_AGLOMERADOS = {int(k): v for k, v in NOMBRES_AGLOMERADOS.items()}

VILLA_EMERGENCIA = 'IV12_3'
TIPO_VIVIENDA = 'IV1' 
TIPO_PISO = 'IV3'
UBICACION_BANIO = "IV9"
TIPO_TENENCIA = 'II7'


def calcular_cantidad(df,descripcion=None):
    cantidad = df['PONDERA'].sum()
    st.metric(descripcion, f"{cantidad:,.0f}")


def calcular_proporcion_tipo_viviendas(df):
    totales = df.groupby(TIPO_VIVIENDA)['PONDERA'].sum()
    proporciones = (totales / totales.sum()) * 100
    return proporciones.rename(index=TIPOS_VIVIENDAS).round(2)


def grafico_tipo_de_viviendas(tipos_viviendas):
    
    fig, ax = plt.subplots()
    
    explode = [0.01] * len(tipos_viviendas)
    
    texts, autotexts = ax.pie(
        tipos_viviendas,
        #labels=None,  # Quita labels del pie
        #shadow=True,  #Agrega sombra
        explode=explode, #Cunata separacion tiene del grafico de torta
    )
    
    etiquetas = [f"{nombre} -> {valor}%" for nombre, valor in zip(tipos_viviendas.index, tipos_viviendas.values)]
    
    # Leyenda al costado, con etiquetas de los índices
    ax.legend(
        etiquetas,
        title="Tipos de Viviendas",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    st.subheader('🏘️ Proporción de Viviendas por Tipo')
    st.text('''🔢 ¿Qué muestra? 
        Esta sección muestra un gráfico circular que presenta la proporción de viviendas según su tipo''')
    st.pyplot(fig)


def calcular_material_predominante_por_aglomerado(df):   
    predominantes_por_p_y_a = df.groupby(['AGLOMERADO',TIPO_PISO])['PONDERA'].sum().reset_index() # ponderar
    predominantes = (predominantes_por_p_y_a.loc[
        predominantes_por_p_y_a.groupby('AGLOMERADO')['PONDERA'].idxmax()
        ][['AGLOMERADO', TIPO_PISO]]
        )
    # Mapea a nombres
    predominantes[TIPO_PISO] = predominantes[TIPO_PISO].map(TIPOS_PISOS)
    
    # Mapea códigos de aglomerado a nombres
    predominantes['AGLOMERADO'] = predominantes['AGLOMERADO'].map(NOMBRES_AGLOMERADOS)

    # Renombra columnas
    predominantes = predominantes.rename(columns={TIPO_PISO: 'Material Predominante','AGLOMERADO': 'Aglomerado'})
    
    #Convierte a serie el dataframe para no mostrar el indice en st.table()
    return predominantes.set_index('Aglomerado')['Material Predominante']


def informar_material_predominante(serie):
    st.subheader('🧱 Material Predrominante de Piso por Aglormerado')
    st.text('''🏘️ ¿Qué muestra? 
        Esta sección se encarga por cada aglomerado, de informa cuál es el material más común en los pisos interiores de las viviendas (por ejemplo: cerámica, cemento, tierra, etc.).''')
    # Mostrar
    st.table(serie)


def calcular_proporcion_viviendas_banio(df):
    df_copy = df.copy()
    df_copy['banio_interior'] = df[UBICACION_BANIO] == next(iter(UBICACION_BANIOS))

    proporcion_banio = df_copy.groupby('AGLOMERADO', group_keys=True).apply(
        lambda x: (x['banio_interior'] * x['PONDERA']).sum() / x['PONDERA'].sum(),
        include_groups=False
    )
    
    proporcion_banio = proporcion_banio.rename(index = NOMBRES_AGLOMERADOS)
    
    # Lo pasamos a porcentaje
    proporcion_banio = (proporcion_banio * 100).round(2).sort_values(ascending=False)
    
    return proporcion_banio


def informar_prop_banio_interior(proporcion_banio):
    st.subheader('🚽 Proporcion Viviendas con Baño Interio')
    st.text('''🚽 ¿Qué muestra? 
        Esta sección se encarga de calcular el porcentaje de viviendad, de cada aglomerado, que poseen un baño en el interior de la misma.''')
    # Mostramos
    st.dataframe(proporcion_banio.rename("Porcentaje (%)"))


def calcular_evolucion_tenencia(df, aglomerado):
    # Mapear nombre a código
    cod_aglo = {v: k for k, v in NOMBRES_AGLOMERADOS.items()}.get(aglomerado)
    if cod_aglo is None:
        return None

    df_aglo = df[df['AGLOMERADO'] == cod_aglo].copy()
    df_aglo['PERIODO'] = df_aglo['ANO4'].astype(str) + "-T" + df_aglo['TRIMESTRE'].astype(str)

    varios_anios = df_aglo['ANO4'].nunique() > 1

    if varios_anios:
        agrupado = df_aglo.groupby(['ANO4', TIPO_TENENCIA])['PONDERA'].sum().unstack(fill_value=0)
        agrupado.index = agrupado.index.astype(str)
    else:
        agrupado = df_aglo.groupby(['PERIODO', TIPO_TENENCIA])['PONDERA'].sum().unstack(fill_value=0)

    # Normaliza a porcentajes
    agrupado = (agrupado.div(agrupado.sum(axis=1), axis=0) * 100).round(2)
    agrupado.rename(columns=DERECHO_PROPIEDAD, inplace=True)

    return agrupado


def informar_evolucion_tenencia(df):
    st.subheader('📈 Evolución de Tenencia de la Vivienda')
    st.text('''📈 ¿Qué muestra? 
        Permite ver cómo cambió a lo largo del tiempo el régimen de tenencia (propia, alquilada, prestada, etc.) en un aglomerado específico. 
        Podés elegir el aglomerado y qué tipos de tenencia querés visualizar.''')

    c1, c2 = st.columns(2)
    with c1:
        seleccion_aglomerado = selector_aglomerados()

    if seleccion_aglomerado == 'Seleccione un aglomerado...':
        st.warning('Debe seleccionar un aglomerado para ver el gráfico.')
        return

    agrupado = calcular_evolucion_tenencia(df, seleccion_aglomerado)
    if agrupado is None or agrupado.empty:
        st.warning("No hay datos disponibles para el aglomerado seleccionado.")
        return

    with c2:
        opciones_disponibles = [t for t in DERECHO_PROPIEDAD.values() if t in agrupado.columns]
        seleccion_tenencias = st.multiselect(
            'Seleccione los tipos de tenencia que desea visualizar:',
            options=opciones_disponibles,
        )

    if not seleccion_tenencias:
        st.warning('Debe seleccionar al menos un tipo de tenencia para continuar.')
        return

    st.line_chart(agrupado[seleccion_tenencias])


def calcular_cantidad_viviendas_en_villas(df):
    df_villas = df[df[VILLA_EMERGENCIA] == 1]
    
    cantidad_villa = df_villas.groupby('AGLOMERADO')['PONDERA'].sum()
    cantidad_villa = cantidad_villa.fillna(0) 
    
    total_aglomerados = df.groupby('AGLOMERADO')['PONDERA'].sum()
    
    porcentaje = (cantidad_villa / total_aglomerados * 100).round(2)
    
    resultado = pd.DataFrame({ 'Cantidad de Viviendas en Villa': cantidad_villa,
                            'Total Aglomerados' : total_aglomerados,
                            'Porcentaje (%)': porcentaje}).sort_values('Cantidad de Viviendas en Villa', ascending=False)
    
    resultado['Cantidad de Viviendas en Villa'] = resultado['Cantidad de Viviendas en Villa'].fillna(0)
    resultado['Porcentaje (%)'] = resultado['Porcentaje (%)'].fillna(0)
    
    return resultado.rename(index = NOMBRES_AGLOMERADOS)


def informar_viviendad_en_villas(resultado):
    st.subheader('Proporción de Viviendas en Villas por Aglomerado')
    st.text('''📉 ¿Qué muestra? 
        Una lista ordenada de los aglomerados según la cantidad de viviendas ubicadas en villas de emergencia.\
        Además del número, se informa el porcentaje que representan respecto al total.''')
    
    st.dataframe(resultado)


def calcular_condicion_de_habitabilidad(df):
    total_por_aglo = df.groupby('AGLOMERADO')['PONDERA'].sum().sort_index()
    
    insuficiente = df[df['CONDICION_DE_HABITABILIDAD'] == 'Insuficiente'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    regular = df[df['CONDICION_DE_HABITABILIDAD'] == 'Regular'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    saludable = df[df['CONDICION_DE_HABITABILIDAD'] == 'Saludable'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    buena = df[df['CONDICION_DE_HABITABILIDAD'] == 'Buena'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    
    insuficiente = (insuficiente / total_por_aglo * 100).round(2)
    regular = (regular / total_por_aglo * 100).round(2)
    saludable = (saludable / total_por_aglo * 100).round(2)
    buena = (buena / total_por_aglo * 100).round(2)
    
    
    df_habitabilidad = pd.DataFrame({'Insuficiente (%)': insuficiente,
                                    'Regular (%)' : regular,
                                    'Saludable (%)' : saludable,
                                    'Buena (%)' : buena,
                                    'Total' : total_por_aglo 
        })
    
    return df_habitabilidad.rename(index = NOMBRES_AGLOMERADOS).sort_index(ascending=True)


def informar_cond_habitabilidad(df_habitabilidad):
    st.subheader('🏠 Condiciones de Habitabilidad de las Viviendas por Aglomerado')
    st.text('''✅ ¿Qué muestra? 
        Por cada aglomerado, se presenta el porcentaje de viviendas según su condición de habitabilidad y el total de viviendas. \
        Además, podés descargar los resultados en un archivo CSV. ''')
    st.dataframe(df_habitabilidad)
    
    convertir_csv(df_habitabilidad,'condicion_habitabilidad.csv')
