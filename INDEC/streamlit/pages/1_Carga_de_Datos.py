import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent  # Ajusta según niveles necesarios
sys.path.append(str(project_root))

from src.DataSet import max_min_año_trimestre
from src.automatizar_jupyter import rutas

max_año_hogar, max_trimestre_hogar, min_año_hogar, min_trimestre_hogar, max_año_individuos, max_trimestre_individuos, min_año_individuos, min_trimestre_individuos = max_min_año_trimestre()
()
st.set_page_config(layout='wide')
st.title("⬆️ Carga de Datos")

st.write(
'El sistema contiene informacion desde el trimestre {} hasta el trimestre {}.'.format(str(min_trimestre_hogar) + '/' + str(min_año_hogar), str(max_trimestre_hogar) + '/' + str(max_año_hogar))
)

st.button('Actualizacion de datos', on_click=rutas)
