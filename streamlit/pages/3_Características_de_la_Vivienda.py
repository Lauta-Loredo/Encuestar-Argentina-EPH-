from pathlib import Path
import sys
import os
import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime as dt

st.set_page_config(layout='wide')
st.title("🏘️ Características de la vivienda")
sys.path.append(os.path.abspath("../code"))

from utils.constantes import (
    UTILS_PATH,
    HOGARES_CSV,
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
PRIMER_ANIO = 2016 #Año desde que tenemos datos


def filtrar_dataframe_por_anio(df_hogares, anio_seleccionado):
    # Filtro el dataframe según si se seleccionó un año o "Todos"
    if anio_seleccionado != 'Todos':
        df_filtrado = df_hogares[df_hogares['ANO4'] == anio_seleccionado]
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos para el año seleccionado.")
            return None
        return df_filtrado
    else:
        if df_hogares.empty:
            st.warning("⚠️ No hay datos en el sistema.")
        return df_hogares


def calcular_cantidad(df):
    cantidad_hogares = df['PONDERA'].sum()
    st.write(f'La cantidad de hogares, en el periodo seleccionado, del dataframe es {cantidad_hogares}.')


def grafico_tipo_de_viviendas(df):
    tipos_viviendas = df.groupby(TIPO_VIVIENDA)['PONDERA'].sum().rename(index=TIPOS_VIVIENDAS)
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
    st.subheader('🏘️ Proporción de Viviendas por Tipo')
    st.pyplot(fig)

'''
CORREGIR, VA ACOMODAR
'''
def material_predominante_por_aglomerado1(df):
    import numpy as np
    from st_aggrid import AgGrid
    
    # Prueba para comprabar que funciona
    #df.loc[:, TIPO_PISO] = np.random.randint(1, 4, size=len(df))
    
    predominantes_por_p_y_a = df.groupby(['AGLOMERADO',TIPO_PISO])['PONDERA'].sum().reset_index() # ponderar
    predominantes = (predominantes_por_p_y_a.loc[
        predominantes_por_p_y_a.groupby('AGLOMERADO')['PONDERA'].idxmax()
    ][['AGLOMERADO', TIPO_PISO]]
    )
    # Mapear a nombres
    predominantes[TIPO_PISO] = predominantes[TIPO_PISO].map(TIPOS_PISOS)
    
    # Mapear códigos de aglomerado a nombres
    predominantes['AGLOMERADO'] = predominantes['AGLOMERADO'].map(NOMBRES_AGLOMERADOS)

    # Renombrar columna
    predominantes = predominantes.rename(columns={TIPO_PISO: 'Material Predominante','AGLOMERADO': 'Aglomerado'})
    serie = predominantes.set_index('Aglomerado')['Material Predominante']
    
    st.subheader('🧱 Material Predrominante de Piso por Aglormerado')
    # Mostrar
    st.markdown(predominantes.to_html(index=False), unsafe_allow_html=True)
    st.table(serie)
    st.dataframe(predominantes,hide_index=True)


def proporcion_viviendas_banio(df):
    df_copy = df.copy()
    df_copy.loc[:, 'banio_interior'] = df[UBICACION_BANIO] == 1

    proporcion_banio = df_copy.groupby('AGLOMERADO', group_keys=True).apply(
        lambda x: (x['banio_interior'] * x['PONDERA']).sum() / x['PONDERA'].sum(),
        include_groups=False
)
    
    proporcion_banio = proporcion_banio.rename(index = NOMBRES_AGLOMERADOS)
    
    # Lo pasamos a porcentaje
    proporcion_banio = (proporcion_banio * 100).round(2).sort_values(ascending=False)
    
    st.subheader('🚽 Proporcion Viviendas con Baño Interio')
    st.text('Esta sección se engarga de calcular el porcentaje de viviendad, de cada aglomerado, que poseen un baño en el interior de la misma.')
    # Mostramos
    st.dataframe(proporcion_banio.rename("Porcentaje (%)"))


def evolucion_tenencia(df):
    st.subheader('📈 Evolución de Tenencia de la Vivienda')
    
    c1, c2 = st.columns(2)

    with c1:
        opciones_aglomerados = ['Seleccione un aglomerado...'] + sorted(NOMBRES_AGLOMERADOS.values())
        seleccion_aglomerado = st.selectbox(
            'Seleccione un aglomerado para visualizar su evolución de tenencia',
            opciones_aglomerados
        )

    with c2:
        seleccion_tenencias = st.multiselect(
            'Seleccione los tipos de tenencia que desea visualizar:',
            options=list(DERECHO_PROPIEDAD.values())
        )

    if seleccion_aglomerado == 'Seleccione un aglomerado...':
        st.warning('⚠️ Debe seleccionar un aglomerado para ver el gráfico.')
        return

    cod_aglo = {v: k for k, v in NOMBRES_AGLOMERADOS.items()}[seleccion_aglomerado]
    df_aglo = df.copy([df['AGLOMERADO'] == cod_aglo])

    # Agrupar por año y trimestre
    df_aglo['PERIODO'] = df_aglo['ANO4'].astype(str) + "-T" + df_aglo['TRIMESTRE'].astype(str)

    varios_anios = df_aglo['ANO4'].nunique() > 1

    if varios_anios:
        agrupado = df_aglo.groupby(['ANO4',TIPO_TENENCIA])['PONDERA'].sum().unstack(fill_value=0)
        agrupado = (agrupado.div(agrupado.sum(axis=1), axis=0) * 100).round(2)
        agrupado.index = agrupado.index.astype(str)  # eje X solo el año
    else:
        agrupado = df_aglo.groupby(['PERIODO',TIPO_TENENCIA])['PONDERA'].sum().unstack(fill_value=0)
        agrupado = (agrupado.div(agrupado.sum(axis=1), axis=0) * 100).round(2)

    agrupado.rename(columns=DERECHO_PROPIEDAD, inplace=True)
    agrupado = agrupado[seleccion_tenencias]

    st.line_chart(agrupado)


def cantidad_viviendas_en_villas(df):
    df_villas = df[df[VILLA_EMERGENCIA] == 1]
    
    cantidad_villa = df_villas.groupby('AGLOMERADO')['PONDERA'].sum()
    cantidad_villa = cantidad_villa.fillna(0) 
    
    total_aglomerados = df.groupby('AGLOMERADO')['PONDERA'].sum()
    
    porcentaje = (cantidad_villa / total_aglomerados * 100).round(2)
    
    resultado = pd.DataFrame({ 'Cantidad Viviendas en Villa': cantidad_villa,
                            'Total Aglomerados' : total_aglomerados,
                            'Porcentaje (%)': porcentaje}).sort_values('Cantidad Viviendas en Villa', ascending=False)
    
    resultado['Cantidad Viviendas en Villa'] = resultado['Cantidad Viviendas en Villa'].fillna(0)
    resultado['Porcentaje (%)'] = resultado['Porcentaje (%)'].fillna(0)
    
    resultado = resultado.rename(index = NOMBRES_AGLOMERADOS)
    
    st.subheader('Proporción de Viviendas en Villas por Aglomerado')
    
    st.dataframe(resultado)


def condiciones_de_habitabilidad(df):
    def convertir_csv(df):
    # Convertir a CSV en memoria
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="📁 Descargar CSV",
            data=csv,
            file_name="Hogares.csv",
            mime="text/csv"
        )
    
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
    
    df_habitabilidad = df_habitabilidad.rename(index = NOMBRES_AGLOMERADOS).sort_index(ascending=True)
    
    st.subheader('🏠 Condiciones de Habitabilidad de las Viviendas por Aglomerado')
    st.dataframe(df_habitabilidad)
    
    convertir_csv(df_habitabilidad)


anios = []


#Genero una lista con los años que hay desde 2016 hasta la actualidad para que el usuario elija el periodo.
for i in range((dt.now().year - PRIMER_ANIO) + 1):
    anio = PRIMER_ANIO + i
    anios.append(anio)

#Las opciones para el selectbox
opciones = ['Seleccione un año...'] + ['Todos'] +  sorted(anios, reverse=True)
#mostrar solo los anios que tengo


st.divider()

#Selectbox para seleccionar un año en especifico o todos los años
anio_seleccionado = st.selectbox( 
    "Seleccione un año para explorar las características habitacionales de la población argentina:",
    opciones
)
df = None

if anio_seleccionado != 'Seleccione un año...':
    try:
        #Genero el dataframe de hogares
        df_hogares = pd.read_csv(UTILS_PATH/HOGARES_CSV, sep=';', low_memory=False)
        df = filtrar_dataframe_por_anio(df_hogares,anio_seleccionado)
    except FileNotFoundError:
        st.error(f"Error: archivo CSV no encontrado")
    except pd.errors.ParserError:  # Usá este en lugar de csv.Error para pandas
        st.error(" Error al leer el archivo CSV")
    except Exception as e:
        st.error(f"⚠️ Ocurrió una excepción inesperada: {e} ({type(e).__name__})")
    if df is not  None:
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
            material_predominante_por_aglomerado1(df)
        
        with tabs[2]:
            proporcion_viviendas_banio(df)
        
        with tabs[3]:
            evolucion_tenencia(df)
        
        with tabs[4]:
            cantidad_viviendas_en_villas(df)
        
        with tabs[5]:
            condiciones_de_habitabilidad(df)
else: 
    st.write('Seleccione un año para poder trabajar con el dataframe.')

st.markdown("""
    <style>
    .footer-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ddd;
        border-top: 1px solid #bbb;
        z-index: 100;
    }

    .footer-container {
        max-width: 960px;
        margin: auto;
        padding: 10px 20px 10px 20px;  /* Menos padding vertical */
        font-size: 10pt;
        color: #333;
    }

    .footer-container h4 {
        font-size: 11pt;
        color: #222;
        margin: 0 0 5px 0;
    }

    .footer-container p {
        margin: 2px 0;
        text-align: justify;
    }

    .footer-container .footer-note {
        text-align: center;
        background-color: #ccc;
        padding: 6px;
        border-radius: 3px;
        margin-top: 8px;
        font-size: 9.5pt;
    }

    /* MÁS espacio inferior para evitar solapamiento */
    .main > div {
        padding-bottom: 220px;
    }
    </style>

    <div class="footer-wrapper">
        <div class="footer-container">
            <h4>Licencia MIT</h4>
            <p>
            Copyright (c) 2025 <strong>Grupo 26</strong>
            </p>
            <p>
            Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados...
            </p>
            <p class="footer-note">
            Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)