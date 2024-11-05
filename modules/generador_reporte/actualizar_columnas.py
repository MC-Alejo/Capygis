from qgis.PyQt.QtWidgets import QCheckBox

from qgis.core import (
    QgsMapLayerType,
    QgsProject,  #para importar las capas de Qgis
)


def actualizar_columnas(instance):

    # Obtener la capa seleccionada
    nombre_capa = instance.inputCapaReporte.currentText()
    layers = QgsProject.instance().mapLayers().values()
    capa_seleccionada = None

    # Buscar la capa por nombre
    for layer in layers:
        if layer.name() == nombre_capa:
            capa_seleccionada = layer
            break
    # Limpiar las columnas anteriores
    for i in reversed(range(instance.columnLayoutReporte.count())):
        instance.columnLayoutReporte.itemAt(i).widget().deleteLater()

    if capa_seleccionada and capa_seleccionada.type() == QgsMapLayerType.VectorLayer:
        # Obtener la capa seleccionada
        capa = QgsProject.instance().mapLayersByName(nombre_capa)[0]

        # Añadir una casilla de selección por cada columna de la capa
        for field in capa.fields():
            checkBox = QCheckBox(field.name())
            instance.columnLayoutReporte.addWidget(checkBox)