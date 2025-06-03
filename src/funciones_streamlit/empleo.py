import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data
def cargar_df():

    ruta_df = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"

    COLUMNAS_NECESARIAS = ["ESTADO", "NIVEL_ED", "ANO4", "TRIMESTRE", "AGLOMERADO", "PP04A"]
    try:
        df = pd.read_csv(ruta_df,delimiter=";", usecols=COLUMNAS_NECESARIAS)

        if not set(COLUMNAS_NECESARIAS).issubset(df.columns):
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

NIVEL_EDUCATIVO = "NIVEL_ED"
TIPO_EMPLEO = "PP04A"
ESTADO_LABORAL = "ESTADO"
# 1.5.1: ESTADO = 2, CH12 = 1-9, ANO4 = input, TRIMESTRE= input
