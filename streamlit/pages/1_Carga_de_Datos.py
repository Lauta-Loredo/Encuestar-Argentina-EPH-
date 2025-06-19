import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent  # Ajusta según niveles necesarios
sys.path.append(str(project_root))

from src.DataSet import año_trimestre
from src.automatizar_jupyter import rutas
from src.funciones_streamlit.funciones_en_comun import footer

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
        f"***El sistema contiene información desde el {trimestre_inicio}° trimestre del año {anio_inicio} hasta el {trimestre_fin}° trimestre del año {anio_fin}.***"
    )
    
    periodo_esperado = []
    anio, trimestre = anio_inicio, trimestre_inicio

    while (anio < anio_fin) or (anio == anio_fin and trimestre <= trimestre_fin):
        periodo_esperado.append((anio, trimestre))
        if trimestre == 4:
            anio += 1
            trimestre = 1
        else:
            trimestre += 1

    # Agrupar faltantes por año usando un diccionario común
    faltantes = {}
    for a, t in periodo_esperado:
        if (a, t) not in rango_fechas_ordenado:
            if a not in faltantes:
                faltantes[a] = []
            faltantes[a].append(f"T{t}")

    # Mostrar resultado
    if not faltantes:
        st.success("✅ El chequeo resultó exitoso y no se encontraron inconsistencias")
    else:
        mensaje = "⚠️ Faltan los siguientes períodos:\n\n"
        for a in sorted(faltantes.keys()):
            trimestres = ", ".join(faltantes[a])
            mensaje += f" || **{a}**: {trimestres}\n"
        st.error(mensaje)

except ValueError:
    st.error("El sistema no contiene informacion de ningun trimestre y año.")


except ValueError:
    st.error("El sistema no contiene informacion de ningun trimestre y año.")

if st.button("Actualizar datos"):
    rutas() 
    st.cache_data.clear()  # limpia el caché global
    st.session_state["datos_actualizados"] = True  
    st.rerun()