from pathlib import Path
import csv

def porcentaje_extranjeros_universitarios():
    
    ruta_individuos = Path(__file__).resolve().parent.parent / "utils" / "IndividuosTotal.csv"
    
    if ruta_individuos is None:
        ruta_individuos = Path("../utils/IndividuosTotal.csv")  # ruta relativa si no se pasa una

    if not ruta_individuos.exists():
        print(f"No se encontró el archivo en: {ruta_individuos.resolve()}")
        return
    
    year = input("Ingrese el año(YYYY): ")
    quarter = input("Ingrese el trimeste (1, 2, 3 o 4): ") 
    total = 0
    pers = 0
    
    with open(ruta_individuos, mode='r', encoding='utf-8') as individuos_file:
        individuos = list(csv.DictReader(individuos_file, delimiter=";"))
        print(individuos[0])
        for i in individuos:
            if i['ANO4'] == year and i['TRIMESTRE'] == quarter:
                total += 1
                if i['CH15'] in ('4', '5') and i['CH12'] in ('6', '7', '8'):
                    pers += 1
    print(f"El porcentaje de personas no nacidas en Argentina con nivel universitario o superior es: { (round(pers/total * 100, 2) )if total != 0 else 'N/A'}%")