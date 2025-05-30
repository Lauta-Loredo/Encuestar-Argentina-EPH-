import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def cargar_csv(ruta):
    """
    Carga del DataFrame en base a la ruta que le envio
    """
    try:
        df = pd.read_csv(ruta, delimiter=";")
        columnas = ["ANO4","TRIMESTRE","CH06","CH04_str","PONDERA"] #Columnas que voy a precisar
        df = df[columnas] #Definicion del DF que solo voy a precisar
        return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV en la ruta especificada.")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {str(e)}")
        return None

def anio_trimestre_seleccion ():

    ruta_csv_individuos = Path(__file__).parent.parent.parent / "utils" / "IndividuosTotal.csv"

    df = cargar_csv(ruta_csv_individuos)

    if df is None:
        return None

    # VALIDO LA EXISTENCIA DE LAS COLUMNAS
    columnas = {"ANO4","TRIMESTRE","CH06","CH04_str"}
    if not columnas.issubset(df.columns):
        print("Error: El archivo no contiene las columnas necesarias")
        return None

    return df

def grafico_barras_grup_edad(df_filtrado,anios,trimestre):
    """
    Crea el grafico de barras por grupos de edad y lo devulve para ser impreso en Streamlit
    """

    #Creacion de los grupos de edad de 10 en 10:
    bins = list(range(0,101,10))
    labels = [f"{i}-{i+9}" for i in bins[:-1]]
    df_filtrado["grupo_edad"] = pd.cut(df_filtrado["CH06"], bins=bins, labels=labels, right=False)

    #Agrupo el df por combinacion de grupo de edad y sexo
    df_agrupado = df_filtrado.groupby(["grupo_edad","CH04_str"])["PONDERA"].sum().reset_index(name="cantidad")

    #Definir para que cada sexo sea una columna
    try:
        df_pivot = df_agrupado.pivot(index="grupo_edad", columns="CH04_str", values="cantidad").fillna(0)
    except Exception as e:
        print(f"Error al procesar los datos: {str(e)}")
        exit()

    #Grafico con matplotlib
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        #Posiciones de las barras
        x = range(len(df_pivot.index))
        width = 0.35
        
        #Verificar qué columnas de género existen
        if 'Femenino' in df_pivot.columns and 'Masculino' in df_pivot.columns:
            mujeres = df_pivot['Femenino']
            varones = df_pivot['Masculino']
        else:
            print("Error: No se encontraron las columnas esperadas para género")
            return None
        
        #Crear las barras
        rects1 = ax.bar([i - width/2 for i in x], mujeres, width, label='Mujeres', color='pink')
        rects2 = ax.bar([i + width/2 for i in x], varones, width, label='Varones', color='blue')

        #Agregar los valores exactos encima de cada barra
        for rect in rects1 + rects2:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., height,
                    f'{int(round(height)):,}'.replace(",","."), #Separador de mil
                    ha='center', va='bottom', fontsize=5)
        
        #Configuración del gráfico
        ax.set_title(f'Cantidad de personas por grupo de edad y sexo ({anios}-T{trimestre})')
        ax.set_xlabel('Grupo de edad')
        ax.set_ylabel('Cantidad de personas')
        ax.set_xticks(x)
        ax.set_xticklabels(df_pivot.index)
        ax.legend()
        
        #Rotar etiquetas para mejor legibilidad
        plt.xticks(rotation=45)
        
        #Ajustar layout para que no se corten las etiquetas
        plt.tight_layout()
        
        #Devuelvo el gráfico
        return fig

    except Exception as e:
        print(f"Error al generar el gráfico: {str(e)}")
        return None