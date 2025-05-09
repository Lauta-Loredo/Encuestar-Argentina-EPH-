from pathlib import Path
from consulta_leer_escribir import obtener_años_trimestres
from aglomerados_sin_baños import cargar_datos_hogares
from mayores_nivel_ed import aglomerados_map

def filtrar_datos_por_anio(list_dic_dataset, year):
    """ En 'datos_filtrados' voy a guardar los diccionarios que correspondan con el año ingresado por el ususario
        Para devolverlos en una lista[diccionarios]"""
    datos_filtrados = []
    for row in list_dic_dataset:
        if row['ANO4'] == year:
            datos_filtrados.append(row)
    return datos_filtrados


def obtener_aglomerados_unicos(datos):
    """ recorro los datos ya filtrados por el año ingresado,
        Para devolver todos los aglomerados que alla en esos datos."""
    aglomerados_unicos = set()
    for row in datos:
        codigo_aglomerado = row['AGLOMERADO']
        aglomerados_unicos.add(codigo_aglomerado)
    return aglomerados_unicos

def cant_precarius(year, list_dic_dataset):
    """ Calcula el aglomerado con mayor y menor porcentaje de viviendas precarias. """
    aglomerado_min = ''
    aglomerado_max = ''
    cont_max = -1
    cont_min = float('inf')

    datos_año = filtrar_datos_por_anio(list_dic_dataset, year)
    
    aglomerados = obtener_aglomerados_unicos (datos_año)
    
    for aglomerado in aglomerados: # recorro los aglomerados
        total = 0
        precarios = 0
        for row in datos_año: # Recorro los datos filtrados por año
            if row['AGLOMERADO'] == aglomerado:
                total += 1
                if row['MATERIAL_TECHUMBRE'] == 'Material precario':
                    precarios += 1
        
        if total > 0:
            porcentaje = round((precarios / total) * 100)
            if porcentaje > cont_max:
                cont_max = porcentaje
                aglomerado_max = aglomerado
            if 0 < porcentaje < cont_min:
                cont_min = porcentaje
                aglomerado_min = aglomerado

    if cont_min == float('inf'):
        aglomerado_min = "Ninguno"
        cont_min = 0

    return aglomerado_max, cont_max, aglomerado_min, cont_min


def precarious_percentage():
    """ calcula y muestra los porcentajes.  """
    archivo_datos = Path(__file__).resolve().parent.parent.parent / 'utils' / 'HogaresTotal.csv'
    
    list_dic_dataset = cargar_datos_hogares(archivo_datos)
    anio_trimestre = obtener_años_trimestres(list_dic_dataset)
   
    year = input('Ingrese un año: ')

    if year not in anio_trimestre:
        print(f"⚠️ El año {year} no se encuentra en los datos.")
        return

    aglomerado_max, cont_max, aglomerado_min, cont_min = cant_precarius(year, list_dic_dataset)
    aglomerados = aglomerados_map()    

    print(f'📈 El aglomerado con mayor porcentaje de viviendas con materiales precarios es {aglomerados[aglomerado_max]} con un {cont_max}%')
    print(f'📉 El aglomerado con menor porcentaje de viviendas con materiales precarios es {aglomerados[aglomerado_min]} con un {cont_min}%')


