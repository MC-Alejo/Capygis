from ...consultas.actualizar import actualizar_consultas

def reset_ventana_reporte(instance):
    # Restablecer la ventana a None y actualizar las consultas
    instance.ventana_reporte = None
    instance.inputCapaReporte = None
    instance.columnLayoutReporte = None
    instance.columnGroupBoxReporte = None
