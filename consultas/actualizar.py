def actualizar_consultas(instance):
    instance.dlg.comboBox.clear()
    nombres = []
    for consulta in instance.consultas:
        nombres.append(consulta['nombre'])
    instance.dlg.comboBox.addItems(nombres)