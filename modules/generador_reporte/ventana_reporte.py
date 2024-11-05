from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QComboBox, QGroupBox, QScrollArea, QWidget

from qgis.core import (
    QgsProject,  #para importar las capas de Qgis
)

from .reset_ventana import reset_ventana_reporte
from .actualizar_columnas import actualizar_columnas
from .generar import generar_reporte_pdf


def mostrar_ventana_reporte(instance):
    # Verificar si la ventana ya existe y, si no, crearla
    if not instance.ventana_reporte:
        # Crear un nuevo diálogo como ventana de consulta
        instance.ventana_reporte = QDialog()
        instance.ventana_reporte.setWindowTitle("Generar reporte PDF")
        instance.ventana_reporte.resize(500, 600)  # Ancho 500, Alto 600

        # Crear un diseño para la ventana
        layout = QVBoxLayout()

        # Añadir una etiqueta
        label = QLabel("Seleccione la capa a realizar reporte:")
        layout.addWidget(label)

        # ComboBox para seleccionar la capa
        instance.inputCapaReporte = QComboBox()
        layers = QgsProject.instance().mapLayers().values()

        layer_list = []

        for layer in layers:
            layer_list.append(layer.name())
        instance.inputCapaReporte.addItems(layer_list)
        layout.addWidget(instance.inputCapaReporte)

        # Caja de grupo para los checkboxes de columnas
        instance.columnGroupBoxReporte = QGroupBox("Seleccione las columnas:")
        instance.columnLayoutReporte = QVBoxLayout()
        instance.columnGroupBoxReporte.setLayout(instance.columnLayoutReporte)

         # Añadir un ScrollArea para manejar muchas columnas
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollWidget = QWidget()
        scrollWidget.setLayout(instance.columnLayoutReporte)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea)

        instance.inputCapaReporte.currentIndexChanged.connect(lambda: actualizar_columnas(instance))

        # Añadir un botón de cierre
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(lambda: generar_reporte_pdf(instance))
        buttonBox.rejected.connect(instance.ventana_reporte.reject)
        layout.addWidget(buttonBox)

        # Configurar el layout en la ventana de diálogo
        instance.ventana_reporte.setLayout(layout)

        # Conectar el evento de cierre de la ventana
        instance.ventana_reporte.finished.connect(lambda: reset_ventana_reporte(instance))

        # Mostrar la ventana
        instance.ventana_reporte.show()