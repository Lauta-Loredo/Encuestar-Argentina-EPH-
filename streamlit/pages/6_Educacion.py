import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import sys

project_root = Path(__file__).parent.parent.parent/'src'
sys.path.append(str(project_root))

import funciones_streamlit.cant_educacion as ced

st.title("🧑‍🎓📚️ Educacion")

st.info("""En esta sección se visualizará información relacionada al nivel de educación
        alcanzado por la población argentina según la EPH.""")
st.divider()


# Carga de datos
df = ced.carga_df()
df_final = ced.personalizacion_datos(df)

if df_final is not None and not df_final.empty:
    st.title("Resumen educativo Trimestral")
    df_final = df_final.set_index("Niveles Educativos")
    st.table(df_final)
else:
    st.warning("Por favor seleccione un año y trimestre válido para ver el resumen.")
