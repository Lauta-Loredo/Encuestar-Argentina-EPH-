import pandas as pd
from pathlib import Path
import streamlit as st


@st.cache_data
def carga_df ():

    ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
    
    columnas_necesarias = ["ANO4", "TRIMESTRE", "CH06","NIVEL_ED_str", "PONDERA", "CODUSU", "NRO_HOGAR", "COMPONENTE"]
    df = pd.read_csv(ruta_csv_individuos, delimiter=";", usecols=columnas_necesarias)
    
    # Chequeo que las columnas esten
    if not set(columnas_necesarias).issubset(df.columns):
        st.error("El archivo no contiene las columnas necesarias")
        st.stop()
    
    # Elimino duplicados
    subset_cols = ["ANO4", "CODUSU", "NRO_HOGAR", "COMPONENTE"]
    df_sin_duplicados = df.drop_duplicates(subset=subset_cols)
    return df_sin_duplicados

def anio_trimestre (df):
    
    
    # Seleccion de anio-trimestre
    anios_disponibles = sorted(df["ANO4"].unique())
    anios_opciones = ["Seleccione un año..."] + list(map(int,anios_disponibles))

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

    
def personalizacion_datos(df):
    
    # Seleccion de anio-trimestre
    anio, trimestre = anio_trimestre(df)

    df = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]
    df_por_anio = df[(df["ANO4"] == anio)]
    # Agrupo y sumo Ponderaciones
    df_resumen = (df.groupby('NIVEL_ED_str')['PONDERA'].sum().reset_index())
    # Ordeno
    df_resumen = df_resumen.sort_values(by='PONDERA', ascending=True)   
    #Elimino dato no relevante     
    df_resumen = df_resumen[df_resumen["NIVEL_ED_str"] != "Sin informacion"]
    # Cambios nombres de las columnas 
    cambios_nom_columns = {'NIVEL_ED_str':'Niveles Educativos', 'PONDERA' : 'Cantidad Maxima'}
    df_final = df_resumen.rename(columns = cambios_nom_columns)
    
    return df_final,df_por_anio
    
def agrupamiento (df):
    
    df_mascomun = (df.groupby('NIVEL_ED_str')['PONDERA'].sum().reset_index())
