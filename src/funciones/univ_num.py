def add_uni(data):
    for info in data:
        if not info.get("NIVEL_ED"):
            continue  # SI NO ENCUENTRA EN UN ELEMENTO DE LA LISTA EL ATRIBUTO NIVEL_ED CONTINUA BUSCANDO
        nivel = int(info["NIVEL_ED"])
        if nivel <= 3 or nivel >= 7:
            univ = 2  # No universitario
        elif 4 <= nivel <= 5:
            univ = 0  # Secundario completo o similar
        elif nivel == 6:
            univ = 1  # Universitario
        info["UNIVERSITARIO"] = univ
