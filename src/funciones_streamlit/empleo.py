import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data
def cargar_df(ruta_df):

    COLUMNAS_NECESARIAS = ["ESTADO", "NIVEL_ED", "ANO4", "TRIMESTRE", "AGLOMERADO", "PP04A"]
    try:
        df = pd.read_csv(ruta_df,delimiter=";", usecols=COLUMNAS_NECESARIAS)

        if not set(COLUMNAS_NECESARIAS).issubset(df.columns):
            st.error("El archivo no contiene las columnas necesarias")
            st.stop()
            raise ValueError("El archivo no contiene las columnas necesarias.")
        else:
            return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV en la ruta especificada.")
        return None
    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV, ERROR: ", {str(e)})
        return None

TIPO_EMPLEO = "PP04A"
ESTADO_LABORAL = "ESTADO"

# Cargar datos ➔ 2. Filtrar año-trimestre ➔ 3. Filtrar desocupados ➔ 4. Agrupar por educación ➔ 5. Contar ponderado ➔ 6. Mostrar.

def definir_año():
    ruta_df = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
    df = cargar_df(ruta_df)

    anios_disponibles = sorted(df["ANO4"].unique())
    anios_opciones = ["Seleccione un año..."] + list(map(int, anios_disponibles))

    anio_seleccionado = st.selectbox("Seleccione un año:", anios_opciones)
    trimestre_seleccionado = None
    if anio_seleccionado != "Seleccione un año...":
        trimestres_disponibles = sorted(df[df["ANO4"] == int(anio_seleccionado)]["TRIMESTRE"].unique())
        trimestres_opciones = ["Seleccione un trimestre..."] + list(map(int,trimestres_disponibles))

        trimestre_seleccionado = st.selectbox("Seleccione un trimestre:", trimestres_opciones)

    if trimestre_seleccionado != "Seleccione un trimestre...":
        return anio_seleccionado, trimestre_seleccionado
    else:
        return anio_seleccionado, None

# 1.5.1
def calcular_desocupados_por_nivel(df, anio, trimestre, NIVEL_EDUCATIVO):
    df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]
    df_desocupados = df_filtrado[(df_filtrado[ESTADO_LABORAL] == 2)]
    # cambio los numeros que representan cada nivel educativo por su descripcion
    df_desocupados["NIVEL_ED"] = df_desocupados["NIVEL_ED"].map(NIVEL_EDUCATIVO)
    # Esto cuenta cuántos desocupados hay para cada valor de NIVEL_ED (del 1 al 9):
    conteo = df_desocupados.groupby("NIVEL_ED").size().sort_index()
    return conteo
