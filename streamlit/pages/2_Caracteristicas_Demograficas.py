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

st.title("📊 Caracteristicas Demográficas")

st.info("""En esta sección se visualizará información relacionada a la características demográficas de
la población argentina según la EPH.
""")
st.warning("Selecciona el subtitulo que deseas visualizar, para asi poder ver su contenido")

# Distribución de la población por grupos y sexo cada 10 años
st.divider()
with st.expander("👩‍👦‍👦 Distribución de la población por grupos y sexo cada 10 años", expanded=False):
    df = ats.cargo_valido_columnas() #Cargo el DF con columnas que voy a usar

    if df is None:
        st.error('Ocurrió un Error Imprevisto')
        st.stop() #Si ocurre algo detego la app

    #Un selectbox para la seleccion de año y trimestre
    anios_disponibles = sorted(df["ANO4"].unique())
    anios = st.selectbox("Seleccione un año: ", anios_disponibles)
    tri_disponible = sorted(df[df["ANO4"] == anios]["TRIMESTRE"].unique())
    trimestre = st.selectbox("Seleccione un trimestre: ", tri_disponible)

    #Filtro los datos segun el año y trimestre seleccionados
    df_filtrado = df[(df["ANO4"] == anios) & (df["TRIMESTRE"] == trimestre)]

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para ese año y trimestre")
        st.stop()

    #Creo un grafico de barras por grupos de edad y sexo
    grafico = ats.grafico_barras_grup_edad(df_filtrado, anios, trimestre)

    if grafico is None:
        st.error('Ocurrió un error al configurar el gráfico')
        st.stop()

    st.pyplot(grafico) #Si el grafico se creo correctamente, se muestra

# Edad promedio por aglomerado
with st.expander("➗ Edad promedio de personas por aglomerado", expanded=False):
    ultimo_anio = df["ANO4"].max()
    df_ultimo_anio = df[df["ANO4"] == ultimo_anio]
    ultimo_trimestre = df_ultimo_anio["TRIMESTRE"].max()

    st.markdown(f'**Periodo de análisis:** {ultimo_anio}-T{ultimo_trimestre} (último disponible)')

    aglomerados = cpv.obtener_nombre_aglomerados()
    df_filtrado2 = df[(df['ANO4'] == ultimo_anio) & (df['TRIMESTRE'] == ultimo_trimestre)]
    df_filtrado2 = ats.calcular_edad_promedio(df_filtrado2)
    df_filtrado2['Nombre Aglomerado'] = df_filtrado2['AGLOMERADO'].astype(str).map(aglomerados)
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
with st.expander("📈 Evolución de la dependencia demográfica", expanded=False):
    aglomerados_opciones = [f"{codigo} - {nombre}" for codigo, nombre in aglomerados.items()]
    seleccion = st.selectbox("Selecciona un aglomerado para analizar", aglomerados_opciones, index=0)
    seleccion_codigo = seleccion.split(" - ")[0]
    df_filtrado3 = df[df["AGLOMERADO"] == int(seleccion_codigo)]

    resultado = ats.dependencia_demografica(df_filtrado3)

    if resultado.empty:
        st.warning("No hay datos disponibles para este aglomerado.")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(resultado.index, resultado["Dependencia"], marker="o", linestyle="-", color="tab:blue")
        ax.set_title(f"Evolución de la dependencia demográfica - {aglomerados[seleccion_codigo]}", fontsize=14)
        ax.set_xlabel("Período", fontsize=12)
        ax.set_ylabel("Índice de dependencia (%)", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        st.pyplot(fig)

# Evolución media y mediana
with st.expander("📉 Evolución de la Media y la Mediana de la edad", expanded=False):
    media_mediana = ats.media_mediana(df)

    if media_mediana.empty:
        st.warning("No hay datos disponibles")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(media_mediana["Periodo"], media_mediana["Media"], label="Media", marker='o')
        ax.plot(media_mediana["Periodo"], media_mediana["Mediana"], label="Mediana", marker='o')

        for i, row in media_mediana.iterrows():
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