import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Ajuste de ruta del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.funciones_streamlit.funciones_en_comun import (
    selector_anio_trimestre,
    crear_dataframe,
)
from src.funciones_streamlit.ingresos import (
    cargar_datos_canasta_basica,
    obtener_valor_canasta_trimestral,
    calcular_pobreza_indigencia,
    mostrar_info_canasta_basica
)
from utils.constantes import HOGARES_CSV

st.set_page_config(layout='wide')
st.title("💰 Línea de Pobreza e Indigencia")

st.info("""
**En esta sección se visualiza información sobre líneas de pobreza e indigencia \
basadas en la canasta básica familiar.**

Se analiza la situación socioeconómica de los hogares argentinos con 4 \
integrantes basándose en:
- **ITF (Ingreso Total Familiar)**: Sumatoria de ingresos individuales de \
todos los componentes del hogar
- **Canasta Básica Familiar**: Dataset con valores desde 2016 con \
frecuencia mensual
- **Líneas de Pobreza e Indigencia**: Calculadas según los valores \
oficiales de la canasta básica

**Nota metodológica**: Los resultados no poseen valor estadístico oficial \
ya que los montos de canasta básica pertenecen a CABA y la EPH es a \
nivel nacional.
""")

st.divider()

# Mostrar información de carga
with st.spinner("Cargando datos..."):
    df_canasta = cargar_datos_canasta_basica()
    
    columnas_hogares = [
        'ANO4', 'TRIMESTRE', 'CODUSU', 'NRO_HOGAR', 
        'IX_TOT', 'PONDERA', 'AGLOMERADO', 'ITF'
    ]
    df_hogares = crear_dataframe(HOGARES_CSV, columnas=columnas_hogares)

if df_canasta is None or df_hogares is None:
    st.error("❌ No se pudieron cargar los datos necesarios")
    st.stop()

# Selectores de filtros
st.subheader("🔍 Selección de Período")

# Usar la función común selector_anio_trimestre
anio_seleccionado, trimestre_seleccionado = selector_anio_trimestre(df_hogares)

# Información sobre política de agregación
with st.expander("ℹ️ Información sobre Cálculo", expanded=False):
    st.write("""
    Para los cálculos de líneas de pobreza e indigencia se utiliza el \
**promedio trimestral** de los valores de canasta básica.
    
    Cada trimestre contiene 3 valores mensuales que se promedian para \
obtener un valor más estable y representativo del período.
    """)

st.divider()

# Procesamiento y cálculos
if (anio_seleccionado not in ["Seleccione un año...", None] and
        trimestre_seleccionado is not None):

    anio_int = int(anio_seleccionado)
    trimestre_int = int(trimestre_seleccionado)

    st.subheader("📊 Resultados del Análisis")

    # Obtener valores de canasta básica usando SIEMPRE promedio
    valores_canasta = obtener_valor_canasta_trimestral(
        df_canasta, anio_int, trimestre_int
    )

    if valores_canasta is not None:
        # Mostrar información de la canasta básica
        mostrar_info_canasta_basica(valores_canasta)

        # Calcular pobreza e indigencia
        resultados = calcular_pobreza_indigencia(
            df_hogares, valores_canasta, anio_int, trimestre_int
        )

        if resultados is not None:
            # Visualizaciones
            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de torta
                st.write("#### 🥧 Distribución por Situación")

                # Datos para el gráfico
                labels = ['No Pobres', 'Pobres (no indigentes)', 'Indigentes']
                sizes = [
                    resultados['porcentaje_no_pobres'],
                    (resultados['porcentaje_pobreza'] -
                     resultados['porcentaje_indigencia']),
                    resultados['porcentaje_indigencia']
                ]
                colors = ['#2E8B57', '#FFD700', '#DC143C']

                # Crear DataFrame para Plotly
                df_pie = pd.DataFrame({
                    'Situación': labels,
                    'Porcentaje': sizes,
                    'Color': colors
                })

                # Filtrar valores > 0 para el gráfico
                df_pie = df_pie[df_pie['Porcentaje'] > 0]

                if not df_pie.empty:
                    fig = px.pie(
                        df_pie,
                        values='Porcentaje',
                        names='Situación',
                        color='Situación',
                        color_discrete_map={
                            'No Pobres': '#2E8B57',
                            'Pobres (no indigentes)': '#FFD700',
                            'Indigentes': '#DC143C'
                        }
                    )
                    fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay datos suficientes para mostrar el gráfico")

            with col2:
                st.subheader("📈 Análisis de Hogares con 4 Integrantes")

                # Primera fila de métricas
                col2_1, col2_2 = st.columns(2)

                with col2_1:
                    total_hogares = resultados['total_hogares']
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; \
border-radius: 5px; margin-bottom: 10px; min-height: 120px; \
display: flex; flex-direction: column; justify-content: space-between;">
                        <h4 style="margin: 0; color: #1f77b4;">Total Hogares</h4>
                        <h2 style="margin: 5px 0; color: #1f77b4;">\
{total_hogares:,}</h2>
                        <p style="margin: 0; color: #666; font-size: 14px; \
font-weight: bold;">Hogares con 4 integrantes representados</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2_2:
                    porc_indigencia = resultados['porcentaje_indigencia']
                    hogares_indigencia = resultados['hogares_indigencia']
                    st.markdown(f"""
                    <div style="background-color: #ffe6e6; padding: 15px; \
border-radius: 5px; margin-bottom: 10px; min-height: 120px; \
display: flex; flex-direction: column; justify-content: space-between;">
                        <h4 style="margin: 0; color: #dc3545;">😢 Indigencia</h4>
                        <h2 style="margin: 5px 0; color: #dc3545;">\
{porc_indigencia}%</h2>
                        <p style="margin: 0; color: #666; font-size: 14px; \
font-weight: bold;">{hogares_indigencia:,} hogares</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Segunda fila de métricas
                col2_3, col2_4 = st.columns(2)

                with col2_3:
                    porc_pobreza = resultados['porcentaje_pobreza']
                    hogares_pobreza = resultados['hogares_pobreza']
                    st.markdown(f"""
                    <div style="background-color: #fff3cd; padding: 15px; \
border-radius: 5px; margin-bottom: 10px; min-height: 120px; \
display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <h4 style="margin: 0; color: #856404;">📉 Pobreza</h4>
                            <h2 style="margin: 5px 0; color: #856404;">\
{porc_pobreza}%</h2>
                            <p style="margin: 0; color: #666; font-size: 14px; \
font-weight: bold;">{hogares_pobreza:,} hogares</p>
                        </div>
                        <p style="margin: 0; color: #856404; \
font-size: 12px; font-weight: bold; background-color: #fff8e1; \
padding: 3px 6px; border-radius: 3px; display: inline-block; \
align-self: flex-start;">(incluye indigencia)</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2_4:
                    porc_no_pobres = resultados['porcentaje_no_pobres']
                    hogares_no_pobres = resultados['hogares_no_pobres']
                    st.markdown(f"""
                    <div style="background-color: #d4edda; padding: 15px; \
border-radius: 5px; margin-bottom: 10px; min-height: 120px; \
display: flex; flex-direction: column; justify-content: space-between;">
                        <h4 style="margin: 0; color: #155724;">✅ No Pobres</h4>
                        <h2 style="margin: 5px 0; color: #155724;">\
{porc_no_pobres}%</h2>
                        <p style="margin: 0; color: #666; font-size: 14px; \
font-weight: bold;">{hogares_no_pobres:,} hogares</p>
                    </div>
                    """, unsafe_allow_html=True)

else:
    st.info("👆 Seleccione un año y trimestre para ver los resultados del análisis") 