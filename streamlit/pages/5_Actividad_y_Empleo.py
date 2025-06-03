from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime as dt

ruta_utils = Path(__file__).parents[2] / "utils"

st.set_page_config(layout="wide")
st.title("💼 Actividad y Empleo")
st.info("En esta sección se visualizará información relacionada a la actividad y empleo según la EPH.")

st.divider()
# 1.5.1 Para las personas desocupadas, informar la cantidad de ellas según sus estudios alcanzados. Se debe informar para un año y trimestre elegido por el usuario

