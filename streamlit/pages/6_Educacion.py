import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

st.title("🧑‍🎓📚️ Educacion")

st.info("""En esta sección se visualizará información relacionada al nivel de educación
        alcanzado por la población argentina según la EPH.""")

ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"
st.divider()

# Carga de datos

def cargar_csv():
    df = pd.read_csv(ruta_csv_individuos, delimiter=";")
    columnas = ["ANO4", "NIVEL_ED_str", "PONDERA", "CODUSU", "NRO_HOGAR", "COMPONENTE"]
    df = df[columnas]
    return df

df = cargar_csv()

columnas = ["ANO4", "NIVEL_ED_str", "PONDERA", "CODUSU", "NRO_HOGAR", "COMPONENTE"]
if not set(columnas).issubset(df.columns):
    st.error("El archivo no contiene las columnas necesarias")
    st.stop()

anios_disponibles = sorted(df["ANO4"].unique())
anios = st.selectbox("Seleccione un año: ", anios_disponibles)

#Averiguo los datos para las educaciones maximas por año
st.write (df.shape)

nivel_orden = {
    "Primario incompleto": 1,
    "Primario completo": 2,
    "Secundario incompleto": 3,
    "Secundario completo": 4,
    "Terciario/Universitario incompleto": 5,
    "Terciario/Universitario completo": 6,
}
df['nivel_num'] = df['NIVEL_ED_str'].map(nivel_orden)

# Quedarse con la entrada de nivel educativo más alto por persona y año
df_nivel_max = df.sort_values('nivel_num', ascending=False).drop_duplicates(
    subset=['ANO4', 'CODUSU', 'NRO_HOGAR', 'COMPONENTE']
)

df_sin_duplicados = df.drop_duplicates(subset=['ANO4', 'CODUSU', 'NRO_HOGAR', 'COMPONENTE'])
df_resumen = (df_nivel_max.groupby(['ANO4', 'NIVEL_ED_str'])['PONDERA'].sum().reset_index())

# Ordenar columnas
df_final = df_resumen.groupby('NIVEL_ED_str')['PONDERA'].sum().reset_index()
df_final = df_final.sort_values(by='PONDERA', ascending=True)
st.title("Resumen educativo anual (EPH)")
st.dataframe(df_final)


# conteo_de_niveles = df["NIVEL_ED_str"].value_counts() 

# maximo_nivel_primario = conteo_de_niveles[["Superior o universitario","Secundario incompleto","Secundario completo","Primario completo"]].sum()
# st.write(maximo_nivel_primario)

# maximo_nivel_secundario = conteo_de_niveles[["Superior o universitario","Secundario completo"]].sum()
# st.write(maximo_nivel_secundario)

# maximo_nivel_superior_universitario = conteo_de_niveles[["Superior o universitario"]].sum()
# st.write(maximo_nivel_superior_universitario)

# claves = ('max_lvl_primario', 'max_lvl_secundario', 'max_lvl_universitario')
# comparaciones = [maximo_nivel_primario, maximo_nivel_secundario, maximo_nivel_superior_universitario]

# fig,ax = plt.subplots(figsize=(10,10))

# ax.pie(comparaciones, labels=claves, autopct='%1.2f%%', startangle= 90)

# # Agregar título
# plt.title('Maximos Niveles Educativos')

# ax.axis('equal')

# # Mostrar el gráfico de torta
# st.pyplot(fig)