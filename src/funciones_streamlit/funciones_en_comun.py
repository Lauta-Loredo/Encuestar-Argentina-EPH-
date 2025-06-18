from pathlib import Path
import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Agrega la ruta al módulo utils
sys.path.append(os.path.abspath("../code"))

from utils.constantes import UTILS_PATH, HOGARES_CSV
from utils.constantes import NOMBRES_AGLOMERADOS

@st.cache_data
def crear_dataframe(archivo_csv, columnas=None):
    """
    Crea un DataFrame a partir de un archivo CSV ubicado en UTILS_PATH.
    Si se especifican columnas, devuelve solo esas columnas válidas.
    Muestra advertencias si el archivo está vacío o si hay columnas inválidas.
    """
    try:
        df = pd.read_csv(UTILS_PATH / archivo_csv, sep=';', low_memory=False)

        if df.empty:
            print("El archivo está vacío")
            st.warning("⚠️ ERROR INESPERADO")
            return None

        if columnas is not None:
            columnas_validas = [col for col in columnas if col in df.columns]
            if len(columnas_validas) < len(columnas):
                columnas_invalidas = set(columnas) - set(columnas_validas)
                print(f"Algunas columnas no existen y fueron omitidas: {columnas_invalidas}")
                st.warning("⚠️ ERROR INESPERADO")
            df = df[columnas_validas]

        return df

    except FileNotFoundError:
        print("Error: archivo CSV no encontrado")
        st.warning("⚠️ ERROR INESPERADO")
    except pd.errors.ParserError:
        print("Error al leer el archivo CSV")
        st.warning("⚠️ ERROR INESPERADO")
    except Exception as e:
        print(f"Ocurrió una excepción inesperada: {e} ({type(e).__name__})")
        st.warning("⚠️ ERROR INESPERADO")

    return None


def filtrar_dataframe_por_anio(df, anio_seleccionado):
    """
    Filtra el DataFrame por un año específico si se selecciona uno.
    Si se selecciona 'Todos', devuelve el DataFrame completo.
    """
    if anio_seleccionado != 'Todos':
        df_filtrado = df[df['ANO4'] == anio_seleccionado]
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos para el año seleccionado.")
            return None
        return df_filtrado

    if df.empty:
        st.warning("⚠️ No hay datos en el sistema.")
    return df


def filtrar_dataframe_por_anio_y_trim(df, anio, trim):
    """
    Filtra el DataFrame por año y trimestre si se seleccionan.
    Devuelve None si no hay datos disponibles para la selección.
    """
    df_fil_anio = filtrar_dataframe_por_anio(df, anio)

    if trim != 'Todos':
        df_fil_anio = df[df['TRIMESTRE'] == trim]
        if df_fil_anio.empty:
            st.warning("⚠️ No hay datos para el trimestre seleccionado.")
            return None
        return df_fil_anio

    if df.empty:
        st.warning("⚠️ No hay datos en el sistema.")
    return df


def selector_anios(df,todos=False,key=None):
    """
    Crea un selector de años basado en los disponibles en el DataFrame.
    Si `todos` es True, incluye la opción 'Todos'.
    """
    if key is None:
        key = "selector_anio"
    anios_disponibles = sorted(df['ANO4'].dropna().unique(), reverse=True)
    opciones = ['Seleccione un año...']

    if todos:
        opciones.append('Todos')

    opciones += list(anios_disponibles)

    anio_seleccionado = st.selectbox(
        "Seleccione un año para explorar las características de la población argentina:",
        opciones,
        key = key
    )

    return anio_seleccionado


def selector_anio_trimestre(df,key=None):
    """
    Muestra dos selectores: uno para año y otro para trimestre disponible según el año seleccionado.
    Devuelve una tupla (anio, trimestre) o (anio, None).
    """
    col1, col2 = st.columns(2)
    if key is None:
        key = "selector_anio_trim"
    
    with col1:
        anio_seleccionado = selector_anios(df)

    with col2:
        trimestre_seleccionado = None

        if anio_seleccionado not in ["Seleccione un año...", "Todos"]:
            anio_int = int(anio_seleccionado)
            trimestres_disponibles = sorted(
                df[df["ANO4"] == anio_int]["TRIMESTRE"].unique()
            )
            trimestres_opciones = ["Seleccione un trimestre..."] + list(map(int, trimestres_disponibles))

            trimestre_seleccionado = st.selectbox(
                "Seleccione un trimestre:",
                trimestres_opciones,
                key = key
            )

    if trimestre_seleccionado and trimestre_seleccionado != "Seleccione un trimestre...":
        return anio_seleccionado, trimestre_seleccionado

    return anio_seleccionado, None


def selector_aglomerados(key=None):
    """
    Muestra un selector de aglomerados basado en los valores del diccionario NOMBRES_AGLOMERADOS.
    """
    if key is None:
        key = "selector_aglomerados"
    aglomerados_opciones = ['Sleccione un aglomerado...'] + [f"{codigo} - {nombre}" for codigo, nombre in NOMBRES_AGLOMERADOS.items()]
    seleccion = st.selectbox("Selecciona un aglomerado para analizar", aglomerados_opciones, index=0,key=key)
    if seleccion != 'Sleccione un aglomerado...':
        seleccion_codigo = seleccion.split(" - ")[0]
        
        return int(seleccion_codigo)


def convertir_csv(df, nombre_archivo="archivo.csv", key=None, indice=True):
    """
    Permite descargar el DataFrame como archivo CSV desde la interfaz de Streamlit.
    """
    csv = df.to_csv(index=indice).encode('utf-8')
    if key is None:
        key = f"descarga_{id(df)}"
    st.download_button(
        label="📁 Descargar CSV",
        data=csv,
        file_name=nombre_archivo,
        mime="text/csv",
        key=key
    )


def footer():
    """
    Muestra un pie de página fijo con información de licencia y autores del sistema.
    """
    st.markdown("""
    <style>
    html, body, #root {
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        overflow-x: hidden;
    }

    .main > div {
        padding-bottom: 80px; /* espacio para que el footer no tape contenido */
    }

    .footer-wrapper {
        position: fixed;  /* fijo en pantalla */
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        background-color: #ddd;
        border-top: 1px solid #bbb;
        padding: 10px 20px;
        font-size: 10pt;
        color: #333;
        box-sizing: border-box;
        z-index: 9999; /* para que esté arriba de todo */
    }

    .footer-container {
        max-width: 960px;
        margin: auto;
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
    </style>

    <div class="footer-wrapper">
        <div class="footer-container">
            <h4>Licencia MIT</h4>
            <p>
            Copyright (c) 2025 <strong>Grupo 26</strong>
            </p>
            <p>
            Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software...
            </p>
            <p class="footer-note">
            Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

