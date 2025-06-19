import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ajuste de rutas
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.consultas.consulta_leer_escribir import calcular_porcentajes_lectura
from src.consultas.ranking5 import ranking_aglomerados_nivel_sup
from src.funciones_streamlit import educacion as ed
from src.funciones_streamlit.funciones_en_comun import (
    selector_anios,
    selector_anio_trimestre,
    filtrar_dataframe_por_anio_y_trim,
)

# ------------------------------------------------------------------------------------
# Título e información inicial
# ------------------------------------------------------------------------------------
st.title("🧑‍🎓📚️ Educación")
st.info(
    """
    En esta sección se visualizará información relacionada al nivel de educación
    alcanzado por la población argentina según la EPH.
    """
)
st.divider()

if st.session_state.get("datos_actualizados", False):
    st.cache_data.clear()
    st.session_state["datos_actualizados"] = False

df = ed.carga_df()

if df is None or not isinstance(df, pd.DataFrame) or df.empty:
    st.info("Los datos no están disponibles o no pudieron cargarse correctamente.")
    st.stop()

# ------------------------------------------------------------------------------------
# 📌 Actividad 1.6.1 - Resumen Trimestral por Nivel Educativo
# ------------------------------------------------------------------------------------
st.subheader("📅 Resumen trimestral por nivel educativo")

anio, trimestre = selector_anio_trimestre(df, key="selector_1_6_1")

if anio in [None, "Seleccione un año..."]:
    st.info("Por favor seleccione un año.")
elif trimestre in [None, "Seleccione un trimestre..."]:
    st.info("Por favor seleccione un trimestre.")
else:
    df_trimestral = filtrar_dataframe_por_anio_y_trim(df, anio, trimestre)

    if df_trimestral is None or df_trimestral.empty:
        st.info("No hay datos disponibles para el año/trimestre seleccionado.")
    else:
        df_trimestral, _ = ed.procesar_niveles_educativos(
            df_trimestral, pd.DataFrame()
        )

        st.write(
            "Informa la cantidad máxima de personas que terminaron o no un nivel educativo"
        )
        df_trimestral = df_trimestral.set_index("Niveles Educativos")
        st.table(df_trimestral)

st.divider()

# ------------------------------------------------------------------------------------
# 📌 Actividad 1.6.2 - Nivel educativo más común por grupo etario
# ------------------------------------------------------------------------------------
st.subheader("📆 Nivel educativo más común por grupo etario")

anio_solo = selector_anios(df, key="selector_1_6_2")

if anio_solo and anio_solo != "Seleccione un año...":
    df_por_anio = df[df["ANO4"] == anio_solo].copy()
    _, df_por_anio = ed.procesar_niveles_educativos(pd.DataFrame(), df_por_anio)

    orden_etario = ["20-30", "30-40", "40-50", "50-60", "+60"]

    st.text(
        "Se informa el nivel educativo más común entre la población, "
        "separado por grupos etarios de 10 en 10 años."
    )

    seleccionar_todos = st.checkbox(
        "Seleccionar todos los grupos etarios", key="checkbox_grupos"
    )

    if seleccionar_todos:
        seleccion = orden_etario
    else:
        seleccion = st.multiselect(
            "", orden_etario, placeholder="¿Qué grupo etario desea ver?"
        )

    if seleccion and not df_por_anio.empty:
        try:
            resultados_por_grupos = ed.agrupamiento(df_por_anio, seleccion)
            fig = ed.grafico_barras(resultados_por_grupos, orden_etario)
            st.plotly_chart(fig, key="fig_1_6_2")
        except Exception as e:
            st.error(f"No se pudo generar el gráfico: {e}")
    else:
        st.info("Por favor seleccione al menos un grupo etario.")
else:
    st.info(
        "Por favor seleccione un año para activar la visualización del grupo etario "
        "y gráfico."
    )

st.divider()

# ------------------------------------------------------------------------------------
# 📌 Actividad 1.6.3 - Ranking de aglomerados
# ------------------------------------------------------------------------------------
st.subheader("🏙️ Ranking de aglomerados")

st.write(
    """
    Ranking de los 5 aglomerados con mayor porcentaje de hogares con dos o más ocupantes
    con estudios universitarios o superiores finalizados.
    """
)

try:
    data = ranking_aglomerados_nivel_sup()
    df_ranking = ed.exportar_csv(data, nombre_archivo="ranking_aglomerados.csv")
except Exception as e:
    st.error(f"Error al generar el ranking o exportar CSV: {e}")

st.divider()

# ------------------------------------------------------------------------------------
# 📌 Actividad 1.6.4 - Porcentajes de alfabetismo y analfabetismo
# ------------------------------------------------------------------------------------
st.subheader("🔤 Porcentajes de alfabetismo y analfabetismo")

try:
    anios, porcen_sabe, porcen_nosabe = calcular_porcentajes_lectura()

    for i in range(len(anios)):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Año {anios[i]}**")
        with col2:
            st.write(f"✔️ Capaces de leer: {porcen_sabe[i]}%")
        with col3:
            st.write(f"❌ Incapaces de leer: {porcen_nosabe[i]}%")

    st.markdown("---")

    chart = ed.grafica_porcentajes_lectura(anios, porcen_sabe, porcen_nosabe)
    st.altair_chart(chart, use_container_width=True, key="lectura_chart")
except Exception as e:
    st.error(f"Error al generar el gráfico de lectura: {e}")
