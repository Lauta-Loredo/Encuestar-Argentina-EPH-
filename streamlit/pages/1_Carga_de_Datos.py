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