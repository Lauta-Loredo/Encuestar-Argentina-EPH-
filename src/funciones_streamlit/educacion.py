import pandas as pd
from pathlib import Path
import streamlit as st
import plotly.express as px
import json
import altair as alt

# ---------------------------------------------------------------------------------------------------------------------
# LAS SIGUIENTES FUNCIONES SON PARA LA CARGA DE DATOS Y LA FILTRACION DE LAS COLUMNAS QUE PRECISO
# ---------------------------------------------------------------------------------------------------------------------


@st.cache_data
def carga_df():
    ruta_csv_individuos = (
        Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
    )

    columnas_necesarias = [
        "ANO4",
        "TRIMESTRE",
        "CH06",
        "NIVEL_ED",
        "PONDERA",
        "CODUSU",
        "NRO_HOGAR",
        "COMPONENTE",
    ]
    df = pd.read_csv(ruta_csv_individuos, delimiter=";", usecols=columnas_necesarias)

    # Chequeo que las columnas estén
    if not set(columnas_necesarias).issubset(df.columns):
        st.error("El archivo no contiene las columnas necesarias")
        st.stop()

    # Elimino duplicados
    subset_cols = ["ANO4", "CODUSU", "NRO_HOGAR", "COMPONENTE"]
    df_sin_duplicados = df.drop_duplicates(subset=subset_cols)
    return df_sin_duplicados


def anio_trimestre(df):
    # Selección de año-trimestre
    anios_disponibles = sorted(df["ANO4"].unique())
    anios_opciones = ["Seleccione un año..."] + list(map(int, anios_disponibles))

    anio_seleccionado = st.selectbox("Seleccione un año:", anios_opciones)

    trimestre_seleccionado = None
    if anio_seleccionado != "Seleccione un año...":
        trimestres_disponibles = sorted(
            df[df["ANO4"] == int(anio_seleccionado)]["TRIMESTRE"].unique()
        )
        trimestres_opciones = ["Seleccione un trimestre..."] + list(
            map(int, trimestres_disponibles)
        )

        trimestre_seleccionado = st.selectbox("Seleccione un trimestre:", trimestres_opciones)

    if trimestre_seleccionado != "Seleccione un trimestre...":
        return anio_seleccionado, trimestre_seleccionado
    else:
        return anio_seleccionado, None


def personalizacion_datos(df):
    anio, trimestre = anio_trimestre(df)

    df_trimestral = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)].copy()
    df_por_anio = df[df["ANO4"] == anio].copy()

    # Cambio los nombres int que tenia NIVEL_ED a str
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

    # Filtrar niveles educativos válidos
    df_por_anio = df_por_anio[df_por_anio["NIVEL_ED"].isin(valores_originales)].copy()
    df_por_anio["NIVEL_ED"] = df_por_anio["NIVEL_ED"].replace(diccionario_mapeo)

    df_trimestral = df_trimestral[df_trimestral["NIVEL_ED"].isin(valores_originales)].copy()
    df_trimestral["NIVEL_ED"] = df_trimestral["NIVEL_ED"].replace(diccionario_mapeo)

    resumen_trimestre = (
        df_trimestral.groupby("NIVEL_ED")["PONDERA"]
        .sum()
        .reset_index()
        .sort_values(by="PONDERA", ascending=True)
    )
    resumen_trimestre = resumen_trimestre.rename(
        columns={"NIVEL_ED": "Niveles Educativos", "PONDERA": "Cantidad Maxima"}
    )

    return resumen_trimestre, df_por_anio


# ---------------------------------------------------------------------------------------------------------------------
# LAS SIGUIENTES FUNCIONES SON PARA EL PUNTO 1.6.2
# ---------------------------------------------------------------------------------------------------------------------


def agrupamiento(df_por_anio, opciones):
    df_filtrado = df_por_anio[df_por_anio["CH06"] >= 20]

    # Agrupamos por año, nivel educativo y edad
    df_mascomun = (
        df_filtrado.groupby(["ANO4", "NIVEL_ED", "CH06"])["PONDERA"]
        .sum()
        .reset_index()
    )
    resultados_por_grupos = {}

    for rango in opciones:
        if rango == "+60":
            df_rango = df_mascomun[df_mascomun["CH06"] >= 60]
        else:
            limite_inferior, limite_superior = map(int, rango.split("-"))
            df_rango = df_mascomun[
                (df_mascomun["CH06"] >= limite_inferior)
                & (df_mascomun["CH06"] <= limite_superior)
            ]

        # Agrupar por nivel educativo
        df_nivel = df_rango.groupby("NIVEL_ED")["PONDERA"].sum().reset_index()

        if not df_nivel.empty:
            nivel_mas_comun = df_nivel.loc[df_nivel["PONDERA"].idxmax()]
            resultados_por_grupos[rango] = (
                nivel_mas_comun["NIVEL_ED"],
                nivel_mas_comun["PONDERA"],
            )

    return resultados_por_grupos


def grafico_barras(resultados_por_grupos, orden_etario):
    # Creo un dataframe a partir del resultados_por_grupos
    df_grafico = pd.DataFrame(
        [
            {"Grupo Etario": r, "Nivel Educativo": n, "PONDERA": p}
            for r, (n, p) in resultados_por_grupos.items()
        ]
    )

    # Esto lo uso para que las barras a la hora de ser visualizadas por el usuario estén ordenadas
    # sin importar el orden de selección
    df_grafico["Grupo Etario"] = pd.Categorical(
        df_grafico["Grupo Etario"], categories=orden_etario, ordered=True
    )

    # Ordenar el DataFrame según ese orden
    df_grafico = df_grafico.sort_values("Grupo Etario")

    # Creo el Gráfico
    st.subheader("Visualización gráfica del nivel educativo más común por grupo etario")

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
        xaxis_title="Grupo Etario", yaxis_title="PONDERA", legend_title="Nivel Educativo"
    )

    return fig


# ---------------------------------------------------------------------------------------------------------------------
# LAS SIGUIENTES FUNCIONES SON PARA EL PUNTO 1.6.3
# ---------------------------------------------------------------------------------------------------------------------

arc_json = Path(__file__).resolve().parent.parent.parent / "utils" / "data" / "aglomerados_coordenadas.json"


def exportar_csv(data):
    # utilizo el archivo "aglomerados_coordenadas" para extraer los nombres de los aglomerados

    with open(arc_json, encoding="utf-8") as f:
        aglo_data = json.load(f)

    # cambio el codigo de aglomerado por su nombre
    ranking_con_nombres = {}
    for cod, datos in data.items():
        # cod.zfill tuve que agregarlo porque me generaba error
        # los codigos con un solo digito en el diccionario porque el json tenía un 0 delante del dígito EJ: 02
        nombre = aglo_data.get(cod.zfill(2), {}).get("nombre", f"Aglomerado {cod}")
        ranking_con_nombres[nombre] = datos

    # convierto el diccionario en dataframe
    df = pd.DataFrame.from_dict(ranking_con_nombres, orient="index")

    # convierto ranking 5 en CSV
    csv = df.to_csv(index=True)

    return csv


# ---------------------------------------------------------------------------------------------------------------------
# LAS SIGUIENTES FUNCIONES SON PARA EL PUNTO 1.6.4
# ---------------------------------------------------------------------------------------------------------------------


def grafica_porcentajes_lectura(años, porcentajes_sabe, porcentajes_nosabe):
    df = pd.DataFrame(
        {
            "Año": años * 2,
            "Porcentaje": porcentajes_sabe + porcentajes_nosabe,
            "Lectura": ["Sabe leer"] * len(años) + ["No sabe leer"] * len(años),
        }
    )

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Año:Q", axis=alt.Axis(title="Año", format="d")),
            y=alt.Y("Porcentaje:Q", title="Porcentaje (%)"),
            color="Lectura:N",
            tooltip=["Año", "Lectura", "Porcentaje"],
        )
        .properties(title="Porcentaje de personas que saben/no saben leer por año", width=700, height=400)
        .interactive()
    )

    return chart
