import streamlit as st
import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent/'src'
sys.path.append(str(project_root))


import funciones_streamlit.educacion as ed
import consultas.ranking5 as r5
import consultas.consulta_leer_escribir as le

st.title("🧑‍🎓📚️ Educacion")

st.info("""En esta sección se visualizará información relacionada al nivel de educación
        alcanzado por la población argentina según la EPH.""")

st.divider() # Aca arranca el punto 1.6.1

if st.session_state.get("datos_actualizados", False):
    st.cache_data.clear()  # fuerza recarga
    st.session_state["datos_actualizados"] = False  # reiniciamos la bandera

# Carga de datos
df = ed.carga_df()
df_trimestral,df_por_anio = ed.personalizacion_datos(df)

# Hasta que el usuario no seleccione un año y trimestre no se va a visualizar ni ejecutar nada de la pagina
if isinstance(df_trimestral, pd.DataFrame) and not df_trimestral.empty:
    st.title("Resumen educativo Trimestral")
    st.write(' Informacion la cantidad maxima de personas que terminaron o no un nivel educativo')
    df_trimestral = df_trimestral.set_index("Niveles Educativos")
    st.table(df_trimestral)

    st.divider() # Aca arranca el punto 1.6.2


    orden_etario = ["20-30", "30-40", "40-50", "50-60", "+60"]

    st.write(' Informacion sobre nivel educacional mas comun entre grupos etarios de 10 en 10')
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
        
        st.plotly_chart(fig)

    else:
        st.info("Por favor seleccione al menos un grupo etario.")
  

    st.divider() # Aca arranca el punto 1.6.3

    st.write('''Ranking de los 5
    aglomerados con mayor porcentaje de hogares con dos o más ocupantes con estudios
    universitarios o superiores finalizados''')

    # Llamo a la funcion ranking 5 
    data = r5.ranking_englomerados_nivelSup()

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
    años, porcen_sabe, porcen_nosabe = le.calcular_porcentajes_lectura()
    
    # Muestro los porcentajes en formato texto
    for i in range(len(años)):
        st.write(f"**Año {años[i]}**")
        st.write(f"✔️ Capaces de leer: {porcen_sabe[i]}%")
        st.write(f"❌ Incapaces de leer: {porcen_nosabe[i]}%")
        st.markdown("---")

    # llamo al grafico creado y lo dejo en segundo plano
    with st.expander("📈 Ver gráfico de lectura por año (preciso)"):
        chart = ed.grafica_porcentajes_lectura(años, porcen_sabe, porcen_nosabe)
        st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Por favor seleccione un año y trimestre válido para ver el resumen.")