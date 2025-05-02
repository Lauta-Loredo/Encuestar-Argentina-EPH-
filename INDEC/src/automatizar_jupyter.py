import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
from pathlib import Path
import DataSet

def ejecutar_notebook(ruta_notebook, tiempo_espera=600, kernel_name='python3'):
    """
    Ejecuta automáticamente todas las celdas de un notebook Jupyter.
    
    Parámetros:
    -----------
    ruta_notebook : str
        Ruta completa al archivo .ipynb que se desea ejecutar
    tiempo_espera : int, opcional
        Tiempo máximo de espera por cada celda (en segundos, default 600)
    kernel_name : str, opcional
        Nombre del kernel a utilizar (default 'python3')
    
    Retorna:
    --------
    None
    """
    try:
        # Cargar el notebook
        with open(ruta_notebook, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Configurar el preprocesador de ejecución
        ep = ExecutePreprocessor(timeout=tiempo_espera, kernel_name=kernel_name)
        
        # Ejecutar todas las celdas
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(ruta_notebook)}})
        
        # Guardar el notebook ejecutado (opcional)
        with open(ruta_notebook, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        print(f"Notebook {os.path.basename(ruta_notebook)} ejecutado exitosamente!")
    
    except Exception as e:
        print(f"Error al ejecutar el notebook: {str(e)}")
        raise

def rutas ():
    """Funcion principal para resetear los csv en base a los archivos disponibles"""

    ruta_archivo = Path(__file__).resolve().parent.parent / "notebooks" / "individuos.ipynb"
    ruta_archivo2 = Path(__file__).resolve().parent.parent / "notebooks" / "hogares.ipynb"
    ejecutar_notebook(ruta_archivo)
    ejecutar_notebook(ruta_archivo2)