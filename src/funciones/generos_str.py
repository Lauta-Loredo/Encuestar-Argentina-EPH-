def int_to_str (list_disc_indi):
    """cambia losv alores de CH04 de integer a string
        valor 1 = Masculino.
        valor 2 = Femenino.
        
    Args:
        list_disc_indi (list_disc): recibe los datos en crudo

    Returns:
        _type_: los devuelve ya modificados
    """
    for i,dict in enumerate(list_disc_indi):
        if list_disc_indi[i]['CH04'] == '1':
                list_disc_indi[i]['CH04_str'] = 'Masculino'
        else:
            list_disc_indi[i]['CH04_str'] = 'Femenino'
