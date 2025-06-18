import json
from pathlib import Path
import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.funciones_streamlit.funciones_en_comun import crear_dataframe


# ---------------------------------------------------------------------------------------------------------------------
# CARGA Y PREPARACIÓN DE DATOS
# ---------------------------------------------------------------------------------------------------------------------

@st.cache_data
def carga_df():
    """Carga el DataFrame de individuos filtrando columnas necesarias."""
    columnas = [
        "ANO4",
        "TRIMESTRE",
        "CH06",
        "NIVEL_ED",
        "PONDERA",
        "CODUSU",
        "NRO_HOGAR",
        "COMPONENTE",
    ]
    try:
        return crear_dataframe("IndividuosTotal.csv", columnas=columnas)
    except FileNotFoundError as e:
        st.error(f"No se encontró el archivo de datos: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado al cargar datos: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------------------------------------------------------------
# PROCESAMIENTO DE NIVELES EDUCATIVOS
# ---------------------------------------------------------------------------------------------------------------------

def procesar_niveles_educativos(df_trimestral, df_por_anio):
    """
    Mapea y renombra los niveles educativos en ambos DataFrames.
    Devuelve:
    - Un resumen trimestral (agrupado y ponderado) si df_trimestral no está vacío.
    - El df_por_anio con niveles educativos renombrados.
    """
    valores_originales = [1, 2, 3, 4, 5, 6]
    nombres = [
        "Primario incompleto",
        "Primario completo",
        "Secundario incompleto",
        "Secundario completo",
        "Superior incompleto",
        "Superior completo",
    ]
    diccionario_mapeo = dict(zip(valores_originales, nombres))

    resumen_trimestre = pd.DataFrame()

    if isinstance(df_trimestral, pd.DataFrame) and not df_trimestral.empty:
        if "NIVEL_ED" in df_trimestral.columns:
            df_trimestral = df_trimestral[
                df_trimestral["NIVEL_ED"].isin(valores_originales)
            ].copy()
            df_trimestral["NIVEL_ED"] = df_trimestral["NIVEL_ED"].replace(
                diccionario_mapeo
            )

            resumen_trimestre = (
                df_trimestral.groupby("NIVEL_ED")["PONDERA"]
                .sum()
                .reset_index()
                .sort_values(by="PONDERA", ascending=True)
                .rename(
                    columns={
                        "NIVEL_ED": "Niveles Educativos",
                        "PONDERA": "Cantidad Maxima",
                    }
                )
            )

    if isinstance(df_por_anio, pd.DataFrame) and not df_por_anio.empty:
        if "NIVEL_ED" in df_por_anio.columns:
            df_por_anio = df_por_anio[
                df_por_anio["NIVEL_ED"].isin(valores_originales)
            ].copy()
            df_por_anio["NIVEL_ED"] = df_por_anio["NIVEL_ED"].replace(
                diccionario_mapeo
            )

    return resumen_trimestre, df_por_anio


# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.2
# ---------------------------------------------------------------------------------------------------------------------

def agrupamiento(df_por_anio, opciones):
    """Calcula el nivel educativo más común para cada grupo etario seleccionado."""
    if df_por_anio.empty:
        st.warning("El DataFrame para agrupamiento está vacío.")
        return {}

    df_filtrado = df_por_anio[df_por_anio["CH06"] >= 20]

    df_mascomun = (
        df_filtrado.groupby(["ANO4", "NIVEL_ED", "CH06"])["PONDERA"]
        .sum()
        .reset_index()
    )
    resultados_por_grupos = {}

    for rango in opciones:
        try:
            if rango == "+60":
                df_rango = df_mascomun[df_mascomun["CH06"] >= 60]
            else:
                li, ls = map(int, rango.split("-"))
                df_rango = df_mascomun[
                    (df_mascomun["CH06"] >= li) & (df_mascomun["CH06"] <= ls)
                ]

            df_nivel = df_rango.groupby("NIVEL_ED")["PONDERA"].sum().reset_index()
            if not df_nivel.empty:
                nivel_mas_comun = df_nivel.loc[df_nivel["PONDERA"].idxmax()]
                resultados_por_grupos[rango] = (
                    nivel_mas_comun["NIVEL_ED"],
                    nivel_mas_comun["PONDERA"],
                )
        except Exception as e:
            st.warning(f"No se pudo procesar el rango {rango}: {e}")

    return resultados_por_grupos


def grafico_barras(resultados_por_grupos, orden_etario):
    """Genera un gráfico de barras con el nivel educativo más común por grupo etario."""
    if not resultados_por_grupos:
        st.warning("No hay datos para graficar.")
        return None

    df_grafico = pd.DataFrame(
        [
            {"Grupo Etario": r, "Nivel Educativo": n, "PONDERA": p}
            for r, (n, p) in resultados_por_grupos.items()
        ]
    )

    df_grafico["Grupo Etario"] = pd.Categorical(
        df_grafico["Grupo Etario"], categories=orden_etario, ordered=True
    )
    df_grafico = df_grafico.sort_values("Grupo Etario")

    fig = px.bar(
        df_grafico,
        x="Grupo Etario",
        y="PONDERA",
        color="Nivel Educativo",
        title="Nivel educativo más común por grupo etario",
        labels={"PONDERA": "Total ponderado"},
        height=500,
    )
    fig.update_traces(textposition="outside", width=0.35)
    fig.update_layout(
        xaxis_title="Grupo Etario",
        yaxis_title="PONDERA",
        legend_title="Nivel Educativo",
    )

    return fig


# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.3
# ---------------------------------------------------------------------------------------------------------------------

arc_json = (
    Path(__file__).resolve().parent.parent.parent / "utils" / "data" / "aglomerados_coordenadas.json"
)


def exportar_csv(data):
    """Convierte un ranking de aglomerados a CSV con nombres legibles."""
    try:
        with open(arc_json, encoding="utf-8") as f:
            aglo_data = json.load(f)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo JSON: {arc_json}")
        return ""
    except json.JSONDecodeError as e:
        st.error(f"Error al leer el JSON: {e}")
        return ""

    ranking_con_nombres = {
        aglo_data.get(cod.zfill(2), {}).get("nombre", f"Aglomerado {cod}"): datos
        for cod, datos in data.items()
    }

    df = pd.DataFrame.from_dict(ranking_con_nombres, orient="index")
    return df.to_csv(index=True)


# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.4
# ---------------------------------------------------------------------------------------------------------------------

def grafica_porcentajes_lectura(años, porcentajes_sabe, porcentajes_nosabe):
    """Genera dos líneas separadas: una para personas que saben leer y otra para las que no saben leer."""
    try:
        df = pd.DataFrame({
            "Año": años,
            "Sabe leer": porcentajes_sabe,
            "No sabe leer": porcentajes_nosabe
        })

        df = df.melt(id_vars=["Año"], var_name="Lectura", value_name="Porcentaje")

    except Exception as e:
        st.error(f"Error al crear DataFrame para la gráfica: {e}")
        return alt.Chart(pd.DataFrame())

    chart_sabe = (
        alt.Chart(df[df["Lectura"] == "Sabe leer"])
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=60), strokeWidth=3)
        .encode(
            x=alt.X("Año:O", axis=alt.Axis(title="Año")),
            y=alt.Y(
                "Porcentaje:Q",
                title="Sabe leer (%)",
                scale=alt.Scale(domain=[90, 100])
            ),
            color=alt.value("#1f77b4"),
            tooltip=["Año", "Lectura", "Porcentaje"]
        )
        .properties(height=200)
    )

    chart_nosabe = (
        alt.Chart(df[df["Lectura"] == "No sabe leer"])
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=60), strokeWidth=3)
        .encode(
            x=alt.X("Año:O", axis=alt.Axis(title="Año")),
            y=alt.Y(
                "Porcentaje:Q",
                title="No sabe leer (%)",
                scale=alt.Scale(domain=[0, 10])
            ),
            color=alt.value("#d62728"),
            tooltip=["Año", "Lectura", "Porcentaje"]
        )
        .properties(height=200)
    )

    chart_final = alt.vconcat(chart_sabe, chart_nosabe).resolve_scale(x='shared')

    return chart_final
