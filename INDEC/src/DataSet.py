import os
import zipfile
import csv
from pathlib import Path 

def dataset_individuals(zip_folder):
    """Leo todos los archivos individuos.txt dentro de los zips por cada año-trimestre
        para luego guardarlos en la lista de diccionarios.

    Args:
        zip_folder (carpeta): donde estan los archivos zip que dentro tiene un txt de individuos y de hogares

    Returns:
        all_individuals: devuelve la lista de diccionarios con todos los datos de individuos de cada año-trimestre cargados.
    """
    all_individuals = []
    for file in os.listdir(zip_folder):
        if file.endswith(".zip"):
            zip_path = zip_folder / file
            with zipfile.ZipFile(zip_path) as all_txt:
                for zips_individuals in all_txt.namelist():
                    if  "usu_individual" in zips_individuals.lower() and zips_individuals.endswith(".txt"):
                        with all_txt.open(zips_individuals) as txt_individuals:
                            reader = csv.DictReader(txt_individuals.read().decode('utf-8').splitlines(), delimiter=';')
                            all_individuals.extend(reader)
     # Verificación
    print(f"✅ Se cargaron {len(all_individuals)} registros de individuos.")
    return all_individuals

def dataset_hogares(zip_folder):
    """Leo todos los archivos hogares.txt dentro de los zips por cada año-trimestre
        para luego guardarlos en la lista de diccionarios.
    Args:
         zip_folder (carpeta): donde estan los archivos zip que dentro tiene un txt de individuos y de hogares

    Returns:
        all_hogares: devuelve la lista de diccionarios con todos los datos de hogares de cada año-trimestre cargados.
    """
    
    all_hogares =[]
    for file in os.listdir(zip_folder):
        if file.endswith(".zip"):
            zip_path = zip_folder / file
            with zipfile.ZipFile(zip_path) as all_txt:
                for zips_hogares in all_txt.namelist():
                    if  "usu_hogar" in zips_hogares.lower() and zips_hogares.endswith(".txt"):
                        with all_txt.open(zips_hogares) as txt_hogares:
                            reader = csv.DictReader(txt_hogares.read().decode('utf-8').splitlines(), delimiter=';')
                            all_hogares.extend(reader)
    # Verificación
    print(f"✅ Se cargaron {len(all_hogares)} registros de hogares.")
    return all_hogares

#RECIBO LA LISTA DE DICCIONARIOS Y CREO UN ARCHIVO CSV CON ESOS DATOS EN CARPETA DATA

def guardar_como_csv(nombre_archivo, lista_diccionarios, delimitador = ";"):
    if not lista_diccionarios:
        print("⚠️ La lista está vacía, no se creó ningún archivo.")
        return

    # Obtener los nombres de columnas del primer diccionario
    columnas = list(lista_diccionarios[0].keys())

    # Ruta de salida en la carpeta "datos"

    ruta_archivo = Path(__file__).resolve().parent.parent / "utils" / f"{nombre_archivo}.csv"

    with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas, delimiter=delimitador)
        writer.writeheader()
        writer.writerows(lista_diccionarios)

    print(f"✅ Archivo {nombre_archivo} guardado en: {ruta_archivo}")

def max_min_año_trimestre():
    """Encuentra el año y trimestre maximo y minimo en el archivo de hogares e individuos.
    Retorna: una tupla(año, trimestre) maximos y minimos para individuos y hogares"""

    ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"
    ruta_hogares = Path(__file__).resolve().parent.parent.parent / "utils" / "HogaresTotal.csv"

    max_año_hogar = 0
    max_año_individuos = 0
    max_trimestre_hogar = 0
    max_trimestre_individuos = 0
    min_año_hogar = 10000
    min_año_individuos = 10000
    min_trimestre_hogar = 5
    min_trimestre_individuos = 5
    
    with open(ruta_hogares, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for r in reader:
            año = int(r['ANO4'])
            trimestre = int(r['TRIMESTRE'])
            
            #Actualiza máximo y minimo año y trimestre para hogares
            if año > max_año_hogar or (año == max_año_hogar and trimestre > max_trimestre_hogar):
                max_año_hogar, max_trimestre_hogar = año, trimestre
            if año < min_año_hogar or (año == min_año_hogar and trimestre < min_trimestre_hogar):
                min_año_hogar, min_trimestre_hogar = año, trimestre
    
    with open(ruta_individuos, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for r in reader:
            año = int(r['ANO4'])
            trimestre = int(r['TRIMESTRE'])
            
            #Actualiza minimo y maximo año y trimestre para individuos
            if año > max_año_individuos or (año == max_año_individuos and trimestre > max_trimestre_individuos):
                max_año_individuos, max_trimestre_individuos = año, trimestre
            if año < min_año_individuos or (año == min_año_individuos and trimestre < min_trimestre_individuos):
                min_año_individuos, min_trimestre_individuos = año, trimestre
    
    return max_año_hogar, max_trimestre_hogar, min_año_hogar, min_trimestre_hogar, max_año_individuos, max_trimestre_individuos, min_año_individuos, min_trimestre_individuos