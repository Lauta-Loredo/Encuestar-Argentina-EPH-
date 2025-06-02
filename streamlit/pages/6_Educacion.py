import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import sys

project_root = Path(__file__).parent.parent.parent/'src'
sys.path.append(str(project_root))

import funciones_streamlit.educacion as ced

st.title("🧑‍🎓📚️ Educacion")

st.info("""En esta sección se visualizará información relacionada al nivel de educación
        alcanzado por la población argentina según la EPH.""")
st.divider()


# Carga de datos
df = ced.carga_df()
df_final,df_por_anio = ced.personalizacion_datos(df)

if isinstance(df_final, pd.DataFrame) and not df_final.empty:
    st.title("Resumen educativo Trimestral")
    df_final = df_final.set_index("Niveles Educativos")
    st.table(df_final)
else:
    st.warning("Por favor seleccione un año y trimestre válido para ver el resumen.")

st.divider() # Aca arranca el punto 1.6.2

orden_etario = ["20-30", "30-40", "40-50", "50-60", "+60"]

st.write(' Informacion sobre nivel educacional mas comun entre grupos etarios de 10 en 10')
seleccionar_todos = st.checkbox("Seleccionar todos los grupos etarios")
if seleccionar_todos:
    seleccion = orden_etario  
else:
    seleccion = st.multiselect(
        '',
        orden_etario,
        placeholder= "¿Qué grupo etario desea ver?"
    )

if seleccion:
    if isinstance(df_por_anio, pd.DataFrame) and not df_por_anio.empty:
        df_filtrado = df_por_anio[df_por_anio['CH06'] >= 20]
        

        # Agrupar por año, nivel educacional y edad
        df_mascomun = df_filtrado.groupby(['ANO4', 'NIVEL_ED_str', 'CH06'])['PONDERA'].sum().reset_index()

        resultados_por_grupos = {}

        for rango in seleccion:
            if rango == '+60':
                df_rango = df_mascomun[df_mascomun['CH06'] >= 60]
            else:
                limite_inferior, limite_superior = map(int, rango.split('-'))
                df_rango = df_mascomun[(df_mascomun['CH06'] >= limite_inferior) & (df_mascomun['CH06'] <= limite_superior)]

            # Agrupar por nivel educacional para encontrar el más común en este rango
            df_nivel = df_rango.groupby('NIVEL_ED_str')['PONDERA'].sum().reset_index()
            if not df_nivel.empty:
                nivel_mas_comun = df_nivel.loc[df_nivel['PONDERA'].idxmax()]
                resultados_por_grupos[rango] = (nivel_mas_comun['NIVEL_ED_str'], nivel_mas_comun['PONDERA'])

        for rango, (nivel, suma) in resultados_por_grupos.items():
            st.write(f"Rango {rango}: Nivel educacional más común = {nivel} (PONDERA total = {suma:.0f})")
else:
    st.info("Por favor seleccione al menos un grupo etario.")


