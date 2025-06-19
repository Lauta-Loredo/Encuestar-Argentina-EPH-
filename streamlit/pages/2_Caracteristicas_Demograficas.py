import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import matplotlib.pyplot as plt

#Agrego direccion raiz del proyecto al sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

#Importo algunas funciones
from src.funciones_streamlit import demografia as ats
from src.consultas import calcular_porc_viviendas_prop as cpv #Modulo para obtener los aglomerados
from src.funciones_streamlit import funciones_en_comun as fc
from utils.constantes import NOMBRES_AGLOMERADOS

st.title("📊 Caracteristicas Demográficas")

st.info("""**En esta sección se visualizará información relacionada a las características demográficas de
la población argentina según la EPH.**\n
\n***Para continuar por favor active el toggle Visualizar Datos Demograficos y seleccione el subtitulo de su agrado, para asi poder ver su contenido***
""")

st.divider()
mostrar_graficos = st.toggle("***Visualizar Datos Demograficos***", value=False)

if mostrar_graficos:
    #Creo el DataFrame
    df = ats.cargar_csv() #Cargo el DF con columnas que voy a usar

    if df is None:
        st.stop() #Si ocurre algo detego la app

    # Distribución de la población por grupos y sexo cada 10 años
    st.divider()
    with st.expander("**👩‍👦‍👦 Distribución de la población por grupos y sexo cada 10 años**", expanded=False):
        anios, trimestre = fc.selector_anio_trimestre(df)

        #Valido la selección antes de continuar
        if anios in ["Seleccione un año...", None] or trimestre in ["Seleccione un trimestre...", None]:
            st.info("Por favor, seleccione un año y un trimestre para ver el gráfico.")
        else:
            # Filtro los datos según el año y trimestre seleccionados
            df_filtrado = df[(df["ANO4"] == anios) & (df["TRIMESTRE"] == trimestre)]

            if df_filtrado.empty:
                st.warning("No hay datos disponibles para ese año y trimestre.")
            else:
                # Creo un gráfico de barras por grupos de edad y sexo
                grafico = ats.grafico_barras_grup_edad(df_filtrado, anios, trimestre)

                if grafico is None:
                    st.error("Ocurrió un error al configurar el gráfico.")
                else:
                    st.pyplot(grafico)

    # Edad promedio por aglomerado
    with st.expander("**➗ Edad promedio de personas por aglomerado**", expanded=False):
        ultimo_anio = df["ANO4"].max()
        df_ultimo_anio = df[df["ANO4"] == ultimo_anio]
        ultimo_trimestre = df_ultimo_anio["TRIMESTRE"].max()

        st.markdown(f'**Periodo de análisis:** {ultimo_anio}-T{ultimo_trimestre} (último disponible)')

        df_filtrado2 = df[(df['ANO4'] == ultimo_anio) & (df['TRIMESTRE'] == ultimo_trimestre)]
        df_filtrado2 = ats.calcular_edad_promedio(df_filtrado2)
        df_filtrado2['Nombre Aglomerado'] = df_filtrado2['AGLOMERADO'].astype(str).map(NOMBRES_AGLOMERADOS)
        df_filtrado2 = df_filtrado2.sort_values(by='AGLOMERADO')
        df_filtrado2['Año'] = ultimo_anio
        df_filtrado2['Trimestre'] = ultimo_trimestre

        orden_columnas = ['Año', 'Trimestre', 'AGLOMERADO', 'Nombre Aglomerado',
                        'poblacion_representada', 'edad_promedio']
        df_filtrado2 = df_filtrado2[orden_columnas]

        st.dataframe(
            df_filtrado2.style.format({
                'edad_promedio': '{:.1f} años',
                'poblacion_representada': '{:,.0f} personas'
            }),
            height=400,
            column_config={
                "AGLOMERADO": "Código Aglomerado",
                "Nombre Aglomerado": "Nombre del Aglomerado",
                "edad_promedio": "Edad Promedio",
                "poblacion_representada": "Población Representada",
                "Año": "Año",
                "Trimestre": "Trimestre"
            }
        )

    # Evolución de la dependencia demográfica
    with st.expander("**📈 Evolución de la dependencia demográfica**", expanded=False):
        #Llamo a una funcion para seleccionar un aglomerado para analizar
        seleccion = fc.selector_aglomerados()
        if str(seleccion).isnumeric():
            df_filtrado3 = df[df["AGLOMERADO"] == int(seleccion)]

            _, df_dep = ats.evoluciones(df_filtrado3)

            if df_dep.empty:
                st.warning("No hay datos disponibles para este aglomerado.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df_dep.index, df_dep["Dependencia"], marker="o", linestyle="-", color="tab:blue")

                for x, y in zip(df_dep.index, df_dep['Dependencia']):
                    ax.text(x, y + 0.07, f"{y: .2f}", ha="center", va="bottom", fontsize=9, color="black")

                ax.set_title(f"Evolución de la dependencia demográfica - {NOMBRES_AGLOMERADOS[str(seleccion)]}", fontsize=14)
                ax.set_xlabel("Período", fontsize=12)
                ax.set_ylabel("Índice de dependencia (%)", fontsize=12)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True)
                st.pyplot(fig)

    # Evolución media y mediana
    with st.expander("**📉 Evolución de la Media y la Mediana de la edad**", expanded=False):
        df_edad, _ = ats.evoluciones(df)

        if df_edad.empty:
            st.warning("No hay datos disponibles")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df_edad["Periodo"], df_edad["Media"], label="Media", marker='o')
            ax.plot(df_edad["Periodo"], df_edad["Mediana"], label="Mediana", marker='o')

            for i, row in df_edad.iterrows():
                ax.text(row["Periodo"], row["Media"] + 0.07, f"{row['Media']:.1f}", 
                        ha='center', va='bottom', fontsize=9, color='blue')
                ax.text(row["Periodo"], row["Mediana"] - 0.07, f"{row['Mediana']:.1f}", 
                        ha='center', va='top', fontsize=9, color='orange')

            ax.set_title("Evolución de la Media y la Mediana de la edad")
            ax.set_xlabel("Periodo")
            ax.set_ylabel("Edad")
            ax.legend()
            ax.grid(True)
            plt.xticks(rotation=45)
            st.pyplot(fig)