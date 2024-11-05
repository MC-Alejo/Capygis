
from qgis.core import ( 
    QgsMapLayerType,
    QgsProject
)

def cargar_columnas(instance):
    # Limpiar el ComboBox de columnas
    instance.inputColumnaConsulta.clear()

    # Obtener la capa seleccionada
    nombre_capa = instance.inputCapaConsulta.currentText()
    layers = QgsProject.instance().mapLayers().values()
    capa_seleccionada = None

    # Buscar la capa por nombre
    for layer in layers:
        if layer.name() == nombre_capa:
            capa_seleccionada = layer
            break

    # Verificar si la capa es válida y obtener sus campos (columnas)
    if capa_seleccionada and capa_seleccionada.type() == QgsMapLayerType.VectorLayer:
        campos = capa_seleccionada.fields()
        columnas = []
        for field in campos:
            columnas.append(field.name())

        # Añadir las columnas al ComboBox
        instance.inputColumnaConsulta.addItems(columnas)
