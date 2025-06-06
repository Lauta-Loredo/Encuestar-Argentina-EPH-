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

if st.button("Actualizar datos"):
    rutas() 
    st.cache_data.clear()  # limpia el caché global
    st.session_state["datos_actualizados"] = True  
    st.rerun()
    st.success("Datos actualizados correctamente.")

st.markdown("""<hr style="margin-top: 50px;">""", unsafe_allow_html=True)

st.markdown("""
<div style='
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 5px;
    font-size: 10pt; 
    text-align: justify; 
    color: #333;
'>
<h4 style='font-size: 11pt; color: #222;'>Licencia MIT</h4>
<p>
Copyright (c) 2025 <strong>Grupo 26</strong>
</p>
<p>
Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:
</p>
<p style='
    text-align: center; 
    background-color: #e9e9e9;
    padding: 10px;
    border-radius: 3px;
    margin-top: 15px;
'>
Desarrollado por Diego Arrechea, Ulises Rodriguez, Axel Morano, Lautaro Loredo y Lucentini Joaquin · UNLP · 2025
</p>
</div>
""", unsafe_allow_html=True)