import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent  # Ajusta según niveles necesarios
sys.path.append(str(project_root))

from src.DataSet import año_trimestre
from src.automatizar_jupyter import rutas

rango_fechas = año_trimestre()

st.set_page_config(layout='wide')
st.title("⬆️ Carga de Datos")
print(rango_fechas)  # imprime en consola que devuelve la funcion max_min_año_trimestre()

try:
    if not rango_fechas: #Si rango_fechas = false, va directamente a la excepcion
        raise ValueError("La lista rango_fechas está vacía")  

    rango_fechas_ordenado = sorted(rango_fechas)
    
    anio_inicio, trimestre_inicio = rango_fechas_ordenado[0]
    anio_fin, trimestre_fin = rango_fechas_ordenado[-1]

    st.write(
        f"***El sistema contiene información desde el trimestre {trimestre_inicio} del año {anio_inicio} hasta trimestre {trimestre_fin} del año {anio_fin}.***"
    )

    #Aca se generan todos los años y trimestres que se esperan
    periodo_esperado = []
    anio, trimestre = anio_inicio, trimestre_inicio

    while (anio < anio_fin) or (anio == anio_fin and trimestre <= trimestre_fin):
        periodo_esperado.append((anio, trimestre))
        if trimestre == 4:
            anio += 1
            trimestre = 1
        else:
            trimestre += 1
    
    #Detecto faltantes
    falta = [f"{a} - T{t}" for (a,t) in periodo_esperado if (a,t) not in rango_fechas_ordenado]

    if not falta:
        st.success("**✅ El chequeo resultó exitoso y no se encontraron inconsistencias**")
    else:
        falta_en_texto = "  //  ".join(falta)
        st.error(f"**⚠️ Faltan los siguientes periodos: {falta_en_texto}**")

except ValueError:
    st.error("El sistema no contiene informacion de ningun trimestre y año.")

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