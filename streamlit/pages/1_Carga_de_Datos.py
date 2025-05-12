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
print(rango_fechas)  # imprime en consola que devuelve la funcion max_min_año_trimestre()

try:
    if not rango_fechas: #Si rango_fechas = false, va directamente a la excepcion
        raise ValueError("La lista rango_fechas está vacía")  

    trimestre_inicio = rango_fechas[3]
    año_inicio = rango_fechas[2]
    trimestre_fin = rango_fechas[1]
    año_fin = rango_fechas[0]

    st.write(
        f"El sistema contiene información desde el trimestre {trimestre_inicio}/{año_inicio} hasta el trimestre {trimestre_fin}/{año_fin}."
    )
except ValueError:
    st.write("El sistema no contiene informacion de ningun trimestre y año.")

st.button('Actualizacion de datos', on_click=rutas)
