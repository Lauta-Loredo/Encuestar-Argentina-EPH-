def renombrar_claves(h):
    h["TIPO_PISO"] = h.pop("IV3")
    h["HAY_AGUA"] = h.pop("IV6")
    h["ORIGEN_AGUA"] = h.pop("IV7")
    h["TIENE_BANIO"] = h.pop("IV8")
    h["UBICACION_BANIO"] = h.pop("IV9")
    h["TIPO_BANIO"] = h.pop("IV10")
    h["DESAGUE"] = h.pop("IV11")


def condicion_de_habitabilidad(hogares):
    
    # Inicializa puntaje
    points = 0
    for h in hogares: 
        
        #Renombro las variables con un nombre mas significativo
        renombrar_claves(h)
        # Condición inmediata de habitabilidad insuficiente
        # Si no hay baño o agua
        if (h["TIENE_BANIO"] == '1' or h["HAY_AGUA"] == '3'):
            h["CONDICION_DE_HABITABILIDAD"] = "Insuficiente"
        else:
            # Condiciones estructurales básicas del hogar

            # Tipo de vivienda (mejor cuanto menor el número)
            match h["TIPO_PISO"] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            # Tipo de baño
            match h["HAY_AGUA"] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            # Tipo de agua
            match h["ORIGEN_AGUA"] :
                case "3":
                    points += 1
                case "2":
                    points += 2
                case "1":
                    points += 3
            # Tipo de desagüe
            match h["UBICACION_BANIO"] :
                case "2":
                    points += 1
                case "1":
                    points += 3
            #Tipo baño
            match h["TIPO_BANIO"] :
                case "2":
                    points += 1
                case "1":
                    points += 2
            #Manejo de desague
            match h["DESAGUE"] :
                case "2":
                    points += 2
                case "1":
                    points += 4

            match h["MATERIAL_TECHUMBRE"]:
                case "Material precario":
                    points += 1
                case "Material durable":
                    points += 2

            # Asignación final según puntaje acumulado
            if points >= 6 :
                h["CONDICION_DE_HABITABILIDAD"] = "Regular"
            elif points >= 10 :
                h["CONDICION_DE_HABITABILIDAD"] = "Saludable"
            else:
                h["CONDICION_DE_HABITABILIDAD"] = "Buena"