from ...consultas.actualizar import actualizar_consultas

def reset_ventana_consulta(instance):
    # Restablecer la ventana a None y actualizar las consultas
    actualizar_consultas(instance)
    instance.ventana_consulta = None