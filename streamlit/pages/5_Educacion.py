import streamlit as st
import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent/'src'
sys.path.append(str(project_root))


import funciones_streamlit.educacion as ed
from consultas.ranking5 import ranking_aglomerados_nivel_sup
from consultas.consulta_leer_escribir import calcular_porcentajes_lectura

st.title("🧑‍🎓📚️ Educacion")

st.info("""En esta sección se visualizará información relacionada al nivel de educación
        alcanzado por la población argentina según la EPH.""")

st.divider() # Aca arranca el punto 1.6.1

if st.session_state.get("datos_actualizados", False):
    st.cache_data.clear()  # fuerza recarga
    st.session_state["datos_actualizados"] = False  # reiniciamos la bandera

# Carga de datos
df = ed.carga_df()

st.title("Informacion educativa Trimestral")

df_trimestral,df_por_anio = ed.personalizacion_datos(df)

# Hasta que el usuario no seleccione un año y trimestre no se va a visualizar ni ejecutar nada de la pagina
if isinstance(df_trimestral, pd.DataFrame) and not df_trimestral.empty:
    st.write(' Informa la cantidad maxima de personas que terminaron o no un nivel educativo')
    df_trimestral = df_trimestral.set_index("Niveles Educativos")
    st.table(df_trimestral)

    st.divider() # Aca arranca el punto 1.6.2


    orden_etario = ["20-30", "30-40", "40-50", "50-60", "+60"]

    st.title('Resumen sobre nivel educacional')
    st.text(' En esta seccion respecto al año seleccionado anteriormente se informa el nivel educativo mas comun entre la poblacion separados por grupos etario de pares de 10 en 10')
    seleccionar_todos = st.checkbox("Seleccionar todos los grupos etarios")
    if seleccionar_todos:
        seleccion = orden_etario  
    else:
        seleccion = st.multiselect(
            '',
            orden_etario,
            placeholder= "¿Qué grupo etario desea ver?"
        )

    if seleccion and (isinstance(df_por_anio, pd.DataFrame) and not df_por_anio.empty):
        
        # Aca hago la filtracion por edad y educacion 
        resultados_por_grupos = ed.agrupamiento(df_por_anio,seleccion)
        
        # creo el grafico para visualizar lo obtenido en resultados_por_grupos
        fig = ed.grafico_barras(resultados_por_grupos, orden_etario)
        
        st.plotly_chart(fig, key="fig")

    else:
        st.info("Por favor seleccione al menos un grupo etario.")
  

    st.divider() # Aca arranca el punto 1.6.3

    st.write('''Ranking de los 5
    aglomerados con mayor porcentaje de hogares con dos o más ocupantes con estudios
    universitarios o superiores finalizados''')

    # Llamo a la funcion ranking 5 
    data = ranking_aglomerados_nivel_sup()

    # le paso "data" que contiene el diccionario con el top 5 aglomerados y me lo devuelve a csv
    csv = ed.exportar_csv(data)

    # Este boton exporta y descarga el archivo CSV
    st.download_button(
        label="📄 Descargar CSV",
        data=csv,
        file_name='datos.csv',
        mime='text/csv'
    )

    st.divider() # Aca arranca el punto 1.6.4
    
    # Llamo a la consulta leer_escribir
    años, porcen_sabe, porcen_nosabe = calcular_porcentajes_lectura()
    
    # Muestro los porcentajes en formato texto
    for i in range(len(años)):
        st.write(f"**Año {años[i]}**")
        st.write(f"✔️ Capaces de leer: {porcen_sabe[i]}%")
        st.write(f"❌ Incapaces de leer: {porcen_nosabe[i]}%")
        st.markdown("---")

    # llamo al grafico creado y lo dejo en segundo plano
    chart = ed.grafica_porcentajes_lectura(años, porcen_sabe, porcen_nosabe)
    st.altair_chart(chart, use_container_width=True, key="lectura_chart")
else:
    st.warning("Por favor seleccione un año y trimestre válido para ver el resumen.")

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