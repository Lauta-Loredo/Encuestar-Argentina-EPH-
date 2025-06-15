import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data
def cargar_df(ruta_df):

    COLUMNAS_NECESARIAS = ["ESTADO", "NIVEL_ED", "ANO4", "TRIMESTRE", "AGLOMERADO", "PP04A", "PONDERA"]
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


def muestra_tasa(tasa, evolucion):
    if evolucion:
        fig, ax = plt.subplots()
        anios = list(evolucion.keys())
        tasas = list(evolucion.values())
        ax.bar(anios, tasas, color="skyblue")
        ax.set_xlabel("Año")
        ax.set_ylabel(f"Tasa de {tasa} (%)")
        ax.set_title(f"Evolución de la tasa de {tasa}")
        st.pyplot(fig)
    else:
        st.warning("Por favor, elije una opción")


# 1.5.1
def calcular_desocupados_por_nivel(df, anio, trimestre, NIVEL_EDUCATIVO):
    # Creo una copia para asegurarme de no modificar el dataframe original.
    df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre) & (df[ESTADO_LABORAL] == 2)].copy()
    #le cambio el tipo de dato en la columna PONDERA, aca es donde modifico el dataframe, por eso la copia.
    df_filtrado['PONDERA'] = df_filtrado['PONDERA'].astype(int)
    df_filtrado["NIVEL_ED"] = df_filtrado["NIVEL_ED"].map(NIVEL_EDUCATIVO)
    # agrupa el dataframe filtrado por nivel educacional, y hace la suma por cada nivel segun la cantidad ponderada. Esto genera una serie donde muestra la cantidad total de personas segun nivel educativo, y lo ordena por indice.
    conteo = (df_filtrado.groupby("NIVEL_ED")['PONDERA'].sum().sort_index())
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


def tasa_des_empleo(df, tipo, aglo=None):
    evolucion = {}
    # Creo una copia para proteger de modificaciones el dataframe original
    df = df.copy()
    # Cambio el tipo de la columna PONDERA
    df["PONDERA"] = df["PONDERA"].astype(float)
    if aglo not in (None, "pais"):
        df = df[df["AGLOMERADO"] == aglo]

    for anio in sorted(df["ANO4"].unique()):
        df_anio = df[df["ANO4"] == anio]
        # .isin([1, 2]): devuelve una serie booleana (en el dataframe filtrado por año), con True para aquellos registros cuyo estado sea 1 (ocupado) o 2 (desocupado) y False para cualquier otro valor (por ejemplo, 3=inactivo).
        df_anio = df_anio[df_anio[ESTADO_LABORAL].isin([1, 2])]
        # Hago las sumatorias desde la columna PONDERA, .loc me deja seleccionar columna y fila a la vez. En este caso, filtra las filas dependiendo el estado laboral, y me retorna los datos de la columna PONDERA. Despues, hace .sum() sobre esa serie.
        desocupados = df_anio.loc[df_anio[ESTADO_LABORAL] == 2, "PONDERA"].sum()
        ocupados = df_anio.loc[df_anio[ESTADO_LABORAL] == 1, "PONDERA"].sum()
        total = desocupados + ocupados
        if tipo == "desempleo":
            if total > 0 :
                tasa = (desocupados / total) * 100
            else:
                tasa= 0
        elif tipo == "empleo":
            if total > 0 :
                tasa = (ocupados / total) * 100
            else:
                tasa= 0
        evolucion[anio] = tasa
    return None if aglo is None else evolucion
