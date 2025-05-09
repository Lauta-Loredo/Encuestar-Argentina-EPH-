import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent  # Ajusta según niveles necesarios
sys.path.append(str(project_root))

from src.DataSet import max_min_año_trimestre
from src.automatizar_jupyter import rutas

rango_fechas = max_min_año_trimestre()

st.set_page_config(layout='wide')
st.title("⬆️ Carga de Datos")
print(rango_fechas)
if not rango_fechas:
    st.write(
        "El sistema no contiene informacion de ningun trimestre y año."
    )
else:
    st.write(
        "El sistema contiene informacion desde el trimestre {} hasta el trimestre {}.".format(
            str(rango_fechas[3]) + "/" + str(rango_fechas[2]),
            str(rango_fechas[1]) + "/" + str(rango_fechas[0]),
        )
    )

st.button('Actualizacion de datos', on_click=rutas)
