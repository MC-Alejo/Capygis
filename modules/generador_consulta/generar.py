from ...consultas.guardar import guardar_consultas

def generar_consulta(instance):
    nombre = instance.inputNombreConsulta.text().strip()
    capa = str(instance.inputCapaConsulta.currentText())
    columna = str(instance.inputColumnaConsulta.currentText())
    operador = str(instance.inputOperadorConsulta.currentText())
    unidad = instance.inputUnidadConsulta.text().strip()
    color = str(instance.selectedColor)

    if nombre and capa and columna and operador and unidad:  # Verificar que no esté vacío

        nueva_consulta = {
            "nombre": nombre,
            "capa": capa,
            "columna": columna,
            "operador": operador,
            "unidad": unidad,
            "color" : color
        }
        instance.consultas.append(nueva_consulta)

        guardar_consultas(instance)

        instance.ventana_consulta.accept()
