import pandas as pd
import matplotlib.pyplot as plt
from . import funciones_en_comun as fc
import streamlit as st


def cargar_csv():
    """
    Carga un DataFramea travez de una funcion donde le envio las columnas relevantes,
    seleccionando columnas relevantes y eliminando filas incompletas.
    """
    archivo = "IndividuosTotal.csv"
    columnas = ["ANO4", "TRIMESTRE", "CH06", "CH04_str", "PONDERA", "AGLOMERADO"]
    df = fc.crear_dataframe (archivo, columnas)
    if df is None:
        return None
        
    # Validar columnas necesarias para dropna
    columnas_esperadas = {"ANO4", "TRIMESTRE", "CH06", "CH04_str", "AGLOMERADO"}
    if not columnas_esperadas.issubset(df.columns):
        st.warning("⚠️ Columnas requeridas no están presentes en el DataFrame.")
        return None

    #Devuelvo el df eliminando filas que no tengan datos de edad o de pondera  
    return df[columnas].dropna(subset=["PONDERA", "CH06"])

def calcular_edad_promedio(df):
    """
    Calcula la edad promedio ponderada por aglomerado.
    """
    df["CH06_ponderada"] = df["CH06"] * df["PONDERA"]
    resultado = df.groupby("AGLOMERADO").agg(
        edad_promedio=("CH06_ponderada", "sum"),
        poblacion_representada=("PONDERA", "sum")
    )
    resultado["edad_promedio"] = resultado["edad_promedio"] / resultado["poblacion_representada"]
    return resultado.sort_values("edad_promedio").reset_index()


def grafico_barras_grup_edad(df, anio, trimestre):
    """
    Crea un gráfico de barras por grupos de edad y sexo.
    """
    try:
        bins = list(range(0, 101, 10))
        labels = [f"{i}-{i+9}" for i in bins[:-1]]
        df["grupo_edad"] = pd.cut(df["CH06"], bins=bins, labels=labels, right=False)

        df_agrupado = df.groupby(["grupo_edad", "CH04_str"])["PONDERA"].sum().reset_index(name="cantidad")
        df_pivot = df_agrupado.pivot(index="grupo_edad", columns="CH04_str", values="cantidad").fillna(0)

        # Validar presencia de columnas esperadas
        if not {"Femenino", "Masculino"}.issubset(df_pivot.columns):
            print("Error: No se encontraron las columnas esperadas para género.")
            return None

        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(df_pivot.index))
        width = 0.35

        mujeres = df_pivot["Femenino"]
        varones = df_pivot["Masculino"]

        rects1 = ax.bar([i - width / 2 for i in x], mujeres, width, label="Mujeres", color="pink")
        rects2 = ax.bar([i + width / 2 for i in x], varones, width, label="Varones", color="blue")

        for rect in rects1 + rects2:
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2., height,
                f"{int(round(height)):,}".replace(",", "."),
                ha="center", va="bottom", fontsize=5
            )

        ax.set_title(f"Cantidad de personas por grupo de edad y sexo ({anio}-T{trimestre})")
        ax.set_xlabel("Grupo de edad")
        ax.set_ylabel("Cantidad de personas")
        ax.set_xticks(list(x))
        ax.set_xticklabels(df_pivot.index)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
        return None


def dependencia_demografica(df):
    """
    Calcula el índice de dependencia demográfica por período.
    """
    columnas = ["ANO4", "TRIMESTRE", "CH06", "PONDERA"]
    if not all(col in df.columns for col in columnas):
        faltantes = [col for col in columnas if col not in df.columns]
        raise ValueError(f"Faltan columnas necesarias: {faltantes}")

    resultados = []

    for (anio, trimestre), grupo in df.groupby(["ANO4", "TRIMESTRE"]):
        pob_0_14 = grupo[(grupo["CH06"] >= 0) & (grupo["CH06"] <= 14)]["PONDERA"].sum()
        pob_15_64 = grupo[(grupo["CH06"] >= 15) & (grupo["CH06"] <= 64)]["PONDERA"].sum()
        pob_65_mas = grupo[grupo["CH06"] >= 65]["PONDERA"].sum()

        if pob_15_64 > 0:
            dependencia = ((pob_0_14 + pob_65_mas) / pob_15_64) * 100
            resultados.append({
                "Año": anio,
                "Trimestre": trimestre,
                "Dependencia": dependencia,
                "Poblacion inactiva": pob_0_14 + pob_65_mas,
                "Poblacion activa": pob_15_64
            })

    if not resultados:
        return pd.DataFrame(columns=["Año", "Trimestre", "Dependencia"])

    df_resultado = pd.DataFrame(resultados)
    df_resultado.sort_values(by=["Año", "Trimestre"], inplace=True)
    df_resultado["Periodo"] = df_resultado["Año"].astype(str) + "-T" + df_resultado["Trimestre"].astype(str)
    df_resultado.set_index("Periodo", inplace=True)
    df_resultado["Dependencia"] = pd.to_numeric(df_resultado["Dependencia"], errors="coerce")

    return df_resultado[["Dependencia"]]


def media_mediana(df):
    """
    Calcula la media ponderada y la mediana simple de edad por período.
    """
    resultados = []

    for (anio, trimestre), grupo in df.groupby(["ANO4", "TRIMESTRE"]):
        edades = grupo["CH06"]
        ponderaciones = grupo["PONDERA"]

        media = (edades * ponderaciones).sum() / ponderaciones.sum()
        mediana = edades.median()

        resultados.append({
            "ANO4": anio,
            "TRIMESTRE": trimestre,
            "Media": media,
            "Mediana": mediana,
            "Periodo": f"{anio}-T{trimestre}"
        })

    return pd.DataFrame(resultados)
