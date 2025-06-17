from pathlib import Path
import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


sys.path.append(os.path.abspath("../code"))


from utils.constantes import (
    UTILS_PATH,
    HOGARES_CSV
)

from utils.constantes import (
    NOMBRES_AGLOMERADOS,
)

NOMBRES_AGLOMERADOS = {int(k): v for k, v in NOMBRES_AGLOMERADOS.items()}

@st.cache_data
def crear_dataframe(columnas=None):
    try:
        #Genero el dataframe de hogares
        df = pd.read_csv(UTILS_PATH / HOGARES_CSV, sep=';', low_memory=False)
        if df.empty:
            st.warning(f"El archvio está vacío.")
            return None
        if columnas is not None:
            df = df[columnas]
        return df
    except FileNotFoundError:
        st.error(f"Error: archivo CSV no encontrado")
    except pd.errors.ParserError:  # Usá este en lugar de csv.Error para pandas
        st.error(" Error al leer el archivo CSV")
    except Exception as e:
        st.error(f" Ocurrió una excepción inesperada: {e} ({type(e).__name__})")
    return None


def filtrar_dataframe_por_anio(df, anio_seleccionado):
    # Filtro el dataframe según si se seleccionó un año o "Todos"
    if anio_seleccionado != 'Todos':
        df_filtrado = df[df['ANO4'] == anio_seleccionado]
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos para el año seleccionado.")
            return None
        return df_filtrado
    else:
        if df.empty:
            st.warning("⚠️ No hay datos en el sistema.")
        return df


def filtrar_dataframe_por_anio_y_trim(df,anio,trim):
    df_fil_anio = filtrar_dataframe_por_anio(df,anio)
    if trim != 'Todos':
        df_fil_anio = df[df['TRIMESTRE'] == trim]
        if df_fil_anio.empty:
            st.warning("⚠️ No hay datos para el trim seleccionado.")
            return None
        return df_fil_anio
    else:
        if df.empty:
            st.warning("⚠️ No hay datos en el sistema.")
        return df


def selector_anios(df,todos=False):
    #Años disponibles en el dataframe
    anios_disponibles = sorted(df['ANO4'].dropna().unique(), reverse=True)
    opciones = ['Seleccione un año...']
    if todos:
        opciones.append('Todos')
    
    opciones += list(anios_disponibles)
    
    #Selectbox para seleccionar un año en especifico o todos los años
    anio_seleccionado = st.selectbox( 
        "Seleccione un año para explorar las características de la población argentina:",
        opciones
    )
    
    return anio_seleccionado


def selector_anio_trimestre(df):
    col1, col2 = st.columns(2)

    with col1:
        anio_seleccionado = selector_anios(df)

    with col2:
        trimestre_seleccionado = None

        # Verificamos que sea un año válido (no texto)
        if anio_seleccionado not in ["Seleccione un año...", "Todos"]:
            anio_int = int(anio_seleccionado)
            trimestres_disponibles = sorted(df[df["ANO4"] == anio_int]["TRIMESTRE"].unique())
            trimestres_opciones = ["Seleccione un trimestre..."] + list(map(int, trimestres_disponibles))

            trimestre_seleccionado = st.selectbox(
                "Seleccione un trimestre:",
                trimestres_opciones,
            )
        
    if trimestre_seleccionado and trimestre_seleccionado != "Seleccione un trimestre...":
        return anio_seleccionado, trimestre_seleccionado
    else:
        return anio_seleccionado, None


def selector_aglomerados():
    opciones_aglomerados = ['Seleccione un aglomerado...'] + sorted(NOMBRES_AGLOMERADOS.values())
    seleccion_aglomerado = st.selectbox(
            'Seleccione un aglomerado para visualizar su evolución de tenencia',
            opciones_aglomerados
        )
    return seleccion_aglomerado


def convertir_csv(df):
    # Conveierte a CSV el dataframe en memoria
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="📁 Descargar CSV",
            data=csv,
            file_name="Hogares.csv",
            mime="text/csv"
        )


def footer():
    st.markdown("""
    <style>
    .footer-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ddd;
        border-top: 1px solid #bbb;
        z-index: 100;
    }

    .footer-container {
        max-width: 960px;
        margin: auto;
        padding: 10px 20px 10px 20px;  /* Menos padding vertical */
        font-size: 10pt;
        color: #333;
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

    /* MÁS espacio inferior para evitar solapamiento */
    .main > div {
        padding-bottom: 220px;
    }
    </style>

    <div class="footer-wrapper">
        <div class="footer-container">
            <h4>Licencia MIT</h4>
            <p>
            Copyright (c) 2025 <strong>Grupo 26</strong>
            </p>
            <p>
            Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados...
            </p>
            <p class="footer-note">
            Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
