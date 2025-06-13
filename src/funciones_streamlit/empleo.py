import pandas as pd
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

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

def definir_anio(df,clave):
    anios_disponibles = sorted(df["ANO4"].unique())
    anios_opciones = ["Seleccione un año..."] + list(map(int, anios_disponibles))

    anio_seleccionado = st.selectbox("Seleccione un año:", anios_opciones,key=clave)

    if anio_seleccionado != "Seleccione un año...":
        return anio_seleccionado
    else:
        return None

def definir_trimestre(df, anio_seleccionado,clave):
    if anio_seleccionado is None:
        return None

    trimestres_disponibles = sorted(df[df["ANO4"] == int(anio_seleccionado)]["TRIMESTRE"].unique())
    trimestres_opciones = ["Seleccione un trimestre..."] + list(map(int, trimestres_disponibles))

    trimestre_seleccionado = st.selectbox("Seleccione un trimestre:", trimestres_opciones, key=clave) #<- ERROR ENCONTRADO, UTILICE UNA KEY PARA DIFERENCIAR ELEMENTOS SELECTBOX UTILIZANDO DOS FUNCIONES IGUALES

    if trimestre_seleccionado != "Seleccione un trimestre...":
        return trimestre_seleccionado
    else:
        return None

def muestra_tasa(tasa,evolucion):
    if evolucion:
        anios = list(evolucion.keys())
        tasas = list(evolucion.values())
        plt.plot(anios, tasas)
        fig, ax = plt.subplots()
        ax.bar(anios, tasas)
        ax.set_xlabel("Año")
        ax.set_ylabel(f"Tasa de {tasa} (%)")
        ax.set_title(f"Evolución de la tasa de {tasa}")
        st.pyplot(fig)
        st.divider()
    else:
        st.warning("Por favor, elije una opción")


# 1.5.1
def calcular_desocupados_por_nivel(df, anio, trimestre, NIVEL_EDUCATIVO):
    df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]
    df_desocupados = df_filtrado[(df_filtrado[ESTADO_LABORAL] == 2)]
    # cambio los numeros que representan cada nivel educativo por su descripcion
    df_desocupados["NIVEL_ED"] = df_desocupados["NIVEL_ED"].map(NIVEL_EDUCATIVO)
    # Esto cuenta cuántos desocupados hay para cada valor de NIVEL_ED (del 1 al 9):
    conteo = df_desocupados.groupby("NIVEL_ED").size().sort_index()
    return conteo

# 1.5.2
def definir_aglomerado(df,clave, NOMBRES_AGLOMERADOS):
    aglomerados_disponibles = sorted(df["AGLOMERADO"].unique())
    NOMBRES_AGLOMERADOS_INT = {int(key): dato for key, dato in NOMBRES_AGLOMERADOS.items()}
    # Generar las opciones tipo "2 - Gran La Plata"
    opciones = [f"{key} - {NOMBRES_AGLOMERADOS_INT.get(key, 'Aglomerado desconocido')}" for key in aglomerados_disponibles]
    opciones = ["Seleccione un aglomerado..."] + ["Todo el País"] + opciones

    aglomerado_elegido = st.selectbox("Seleccione un aglomerado:", opciones,key=clave)

    if aglomerado_elegido == "Seleccione un aglomerado...":
        return None

    if aglomerado_elegido == "Todo el País":
        return "pais"

    # extraer solo la key (esta antes del guion)
    codigo = int(aglomerado_elegido.split(" - ")[0])
    return codigo

def tasa_des_empleo(df,tasa,aglo=None):
    evolucion = {}

    for anio in sorted(df["ANO4"].unique()):
        df_anio = df[df["ANO4"] == anio]

        if aglo != "pais":
            df_anio = df_anio[df_anio["AGLOMERADO"] == aglo]
        
        # .shape[0] es la forma rápida de contar filas en pandas.
        desocupados = df_anio[df_anio[ESTADO_LABORAL] == 2].shape[0]
        ocupados = df_anio[df_anio[ESTADO_LABORAL] == 1].shape[0]
        total = desocupados + ocupados
        if tasa == "desempleo":
            if total > 0 :
                tasa = (desocupados / total) * 100
            else:
                tasa= 0
        elif tasa == "empleo":
            if total > 0 :
                tasa = (ocupados / total) * 100
            else:
                tasa= 0
        evolucion[anio] = tasa
    if aglo == None:
        return None
    return evolucion
