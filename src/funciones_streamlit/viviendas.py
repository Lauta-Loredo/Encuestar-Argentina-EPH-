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
    '''
    Calcula la cantidad ponderada de objetos que hay en el dataframe y los pondera
    Parametros que recibe: un dataframe y una descripcion para mostrar en pantalla
    '''
    cantidad = df['PONDERA'].sum()
    st.metric(descripcion, f"{cantidad:,.0f}")


def calcular_proporcion_tipo_viviendas(df):
    """
    Calcula la proporción de viviendas según su tipo.
    Parámetros:
    - df: DataFrame que contiene las columnas de tipo de vivienda y ponderación.
    Devuelve:
    - Serie con los porcentajes redondeados por tipo de vivienda, con etiquetas descriptivas.
    """
    # Calcula el total por tipo de vivienda
    totales = df.groupby(TIPO_VIVIENDA)['PONDERA'].sum()
    
    # Calcula los respectivos porcentajes
    proporciones = (totales / totales.sum()) * 100
    
    # Devuelve: una Serie con porcentajes y redondea, de cada tipo de vivienda
    return proporciones.rename(index=TIPOS_VIVIENDAS).round(2)


def grafico_tipo_de_viviendas(tipos_viviendas):
    # Crea la figura y los ejes para el gráfico
    fig, ax = plt.subplots()
    
    # Define un desplazamiento para cada porción del gráfico (para separarlas un poco)
    explode = [0.01] * len(tipos_viviendas)
    
    # Crea el gráfico de torta sin etiquetas, usando los valores proporcionados
    texts, autotexts = ax.pie(
        tipos_viviendas,
        explode=explode,  # Cantidad de separación entre sectores
    )
    
    # Genera las etiquetas para la leyenda
    etiquetas = [f"{nombre} -> {valor}%" for nombre, valor in zip(tipos_viviendas.index, tipos_viviendas.values)]
    
    # Agrega una leyenda al costado derecho del gráfico con las etiquetas generadas
    ax.legend(
        etiquetas,
        title="Tipos de Viviendas",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    
    # Agrega un subtítulo en Streamlit
    st.subheader('🏘️ Proporción de Viviendas por Tipo')
    
    # Agrega una breve descripción textual en Streamlit
    st.text('''🔢 ¿Qué muestra? 
        Esta sección muestra un gráfico circular que presenta la proporción de viviendas según su tipo''')
    
    # Muestra el gráfico en Streamlit
    st.pyplot(fig)


def calcular_material_predominante_por_aglomerado(df):
    
    # Agrupa por aglomerado y tipo de piso
    predominantes_por_p_y_a = df.groupby(['AGLOMERADO',TIPO_PISO])['PONDERA'].sum().reset_index()
    
    # Se queda con el tipo de piso que tuvo mayor cantidad
    predominantes = (predominantes_por_p_y_a.loc[
        predominantes_por_p_y_a.groupby('AGLOMERADO')['PONDERA'].idxmax()
        ][['AGLOMERADO', TIPO_PISO]]
        )
    
    # Reemplaza los códigos del tipo de piso por nombres descriptivos
    predominantes[TIPO_PISO] = predominantes[TIPO_PISO].map(TIPOS_PISOS)
    
    # Reemplaza los códigos de aglomerado por sus nombres
    predominantes['AGLOMERADO'] = predominantes['AGLOMERADO'].map(NOMBRES_AGLOMERADOS)

    # Renombra las columnas para hacer el resultado más legible
    predominantes = predominantes.rename(columns={TIPO_PISO: 'Material Predominante','AGLOMERADO': 'Aglomerado'})
    
    # Devuelve una Serie indexada por aglomerado con el material predominant
    return predominantes.set_index('Aglomerado')['Material Predominante']


def informar_material_predominante(serie):
    st.subheader('🧱 Material Predrominante de Piso por Aglormerado')
    st.text('''🏘️ ¿Qué muestra? 
        Esta sección se encarga por cada aglomerado, de informa cuál es el material más común en los pisos interiores de las viviendas (por ejemplo: cerámica, cemento, tierra, etc.).''')
    # Muestra la serie con los valores
    st.table(serie)


def calcular_proporcion_viviendas_banio(df):
    
    # Hacem una copia del DataFrame para no modificar el original
    df_copy = df.copy()
    
        
    # Crea una columna booleana que indica si el baño está en el interior
    # Compara el primer valor del diccionario UBICACION_BANIOS, que significa banio interior
    df_copy['banio_interior'] = df[UBICACION_BANIO] == next(iter(UBICACION_BANIOS))

        
    # Calcula la proporción ponderada de viviendas con baño interior por aglomerado
    proporcion_banio = df_copy.groupby('AGLOMERADO', group_keys=True).apply(
        lambda x: (x['banio_interior'] * x['PONDERA']).sum() / x['PONDERA'].sum(),
        include_groups=False
    )
    
    # Reemplaza indicepor los nombres de los aglomerados
    proporcion_banio = proporcion_banio.rename(index = NOMBRES_AGLOMERADOS)
    
    # Calculamos los porcentaje
    proporcion_banio = (proporcion_banio * 100).round(2).sort_values(ascending=False)
    
    return proporcion_banio


def informar_prop_banio_interior(proporcion_banio):
    st.subheader('🚽 Proporcion Viviendas con Baño Interio')
    st.text('''🚽 ¿Qué muestra? 
        Esta sección se encarga de calcular el porcentaje de viviendad, de cada aglomerado, que poseen un baño en el interior de la misma.''')
    # Muestra en streamlit
    st.dataframe(proporcion_banio.rename("Porcentaje (%)"))


def calcular_evolucion_tenencia(df,cod_aglo):
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
    
    # Crea dos columnas para dividir la interfaz
    c1, c2 = st.columns(2)
    
    # Selector de aglomerado en la primera columna
    with c1:
        seleccion_aglomerado = selector_aglomerados('selector_aglomerados_viviendas')
        
    # Verifica que se haya seleccionado un aglomerado válido
    if seleccion_aglomerado == 'Sleccione un aglomerado...':
        st.warning('Debe seleccionar un aglomerado para ver el gráfico.')
        return

    # Calcula la evolución de la tenencia para el aglomerado elegido
    agrupado = calcular_evolucion_tenencia(df, seleccion_aglomerado)
    
    # Verifica que existan datos disponibles
    if agrupado is None or agrupado.empty:
        st.warning("No hay datos disponibles para el aglomerado seleccionado.")
        return

    # Selector de tipos de tenencia en la segunda columna
    with c2:
        opciones_disponibles = [t for t in DERECHO_PROPIEDAD.values() if t in agrupado.columns]
        seleccion_tenencias = st.multiselect(
            'Seleccione los tipos de tenencia que desea visualizar:',
            options=opciones_disponibles,
        )

    # Verifica que se haya seleccionado al menos una opción
    if not seleccion_tenencias:
        st.warning('Debe seleccionar al menos un tipo de tenencia para continuar.')
        return

    # Título de la sección en Streamlit
    st.subheader('📈 Evolución de Tenencia de la Vivienda')
    
    # Descripción explicativa en Streamlit
    st.text('''📈 ¿Qué muestra? 
        Permite ver cómo cambió a lo largo del tiempo el régimen de tenencia (propia, alquilada, prestada, etc.) en un aglomerado específico. 
        Podés elegir el aglomerado y qué tipos de tenencia querés visualizar.''')
    
    # Muestra el gráfico de líneas con la evolución de los tipos seleccionados
    st.line_chart(agrupado[seleccion_tenencias])


def calcular_cantidad_viviendas_en_villas(df):
    
    # Filtra solo las viviendas que están en villas de emergencia (valor 1 en la columna correspondiente)
    df_villas = df[df[VILLA_EMERGENCIA] == 1]
    
    # Suma ponderada de viviendas en villas por aglomerado
    cantidad_villa = df_villas.groupby('AGLOMERADO')['PONDERA'].sum()
    
    # Asegura que no haya valores nulos
    cantidad_villa = cantidad_villa.fillna(0) 
    
    # Suma total de viviendas por aglomerado, incluyendo todas las viviendas
    total_aglomerados = df.groupby('AGLOMERADO')['PONDERA'].sum()
    
    # Calcula el porcentaje de viviendas en villas sobre el total por aglomerado
    porcentaje = (cantidad_villa / total_aglomerados * 100).round(2)
    
    # Crea un DataFrame con los tres indicadores: cantidad de villas, total y porcentaje
    resultado = pd.DataFrame({ 'Cantidad de Viviendas en Villa': cantidad_villa,
                            'Total Aglomerados' : total_aglomerados,
                            'Porcentaje (%)': porcentaje}).sort_values('Cantidad de Viviendas en Villa', ascending=False)
    
    resultado['Cantidad de Viviendas en Villa'] = resultado['Cantidad de Viviendas en Villa'].fillna(0)
    resultado['Porcentaje (%)'] = resultado['Porcentaje (%)'].fillna(0)
    
    # Renombra los índices con los nombres legibles de los aglomerados
    return resultado.rename(index = NOMBRES_AGLOMERADOS)


def informar_viviendad_en_villas(resultado):
    st.subheader('Proporción de Viviendas en Villas por Aglomerado')
    st.text('''📉 ¿Qué muestra? 
        Una lista ordenada de los aglomerados según la cantidad de viviendas ubicadas en villas de emergencia.\
        Además del número, se informa el porcentaje que representan respecto al total.''')
    
    st.dataframe(resultado)


def calcular_condicion_de_habitabilidad(df):
    # Calcula el total de viviendas ponderadas por aglomerado
    total_por_aglo = df.groupby('AGLOMERADO')['PONDERA'].sum().sort_index()
    
    # Filtra y agrupa las viviendas por su condicion de habitabilidad por aglomerado
    # Reindexa para que todos los aglomerados estén presentes
    insuficiente = df[df['CONDICION_DE_HABITABILIDAD'] == 'Insuficiente'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    regular = df[df['CONDICION_DE_HABITABILIDAD'] == 'Regular'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    saludable = df[df['CONDICION_DE_HABITABILIDAD'] == 'Saludable'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    buena = df[df['CONDICION_DE_HABITABILIDAD'] == 'Buena'].groupby('AGLOMERADO')['PONDERA'].sum().reindex(total_por_aglo.index, fill_value=0)
    
    # Calcula los porcentajes respecto al total ponderado por aglomerado
    insuficiente = (insuficiente / total_por_aglo * 100).round(2)
    regular = (regular / total_por_aglo * 100).round(2)
    saludable = (saludable / total_por_aglo * 100).round(2)
    buena = (buena / total_por_aglo * 100).round(2)
    
    # Crea un DataFrame con todas las proporciones y el total
    df_habitabilidad = pd.DataFrame({'Insuficiente (%)': insuficiente,
                                    'Regular (%)' : regular,
                                    'Saludable (%)' : saludable,
                                    'Buena (%)' : buena,
                                    'Total' : total_por_aglo 
        })
    
    # Renombra los índices con los nombres de los aglomerados y ordena alfabéticamente
    return df_habitabilidad.rename(index = NOMBRES_AGLOMERADOS).sort_index(ascending=True)


def informar_cond_habitabilidad(df_habitabilidad):
    st.subheader('🏠 Condiciones de Habitabilidad de las Viviendas por Aglomerado')
    st.text('''✅ ¿Qué muestra? 
        Por cada aglomerado, se presenta el porcentaje de viviendas según su condición de habitabilidad y el total de viviendas. \
        Además, podés descargar los resultados en un archivo CSV. ''')
    st.dataframe(df_habitabilidad)
    
    convertir_csv(df_habitabilidad,'condicion_habitabilidad.csv')
