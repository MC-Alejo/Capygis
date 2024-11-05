def buscar_consulta(instance, nombre):
    bandera = False
    for consulta in instance.consultas:
        if nombre == consulta['nombre']:
            return consulta
    
    return bandera
