from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QComboBox, QGroupBox, QScrollArea, QWidget

from qgis.core import (
    QgsProject,  #para importar las capas de Qgis
)

from .reset_ventana import reset_ventana_analizador
from .columnas.actualizar_columnas import actualizar_columnas
from .analisis.generar_analisis import generar_analisis

def mostrar_ventana_analizador(instance):
    # Verificar si la ventana ya existe y, si no, crearla
    if not instance.ventana_analizador:
        # Crear un nuevo diálogo como ventana de consulta
        instance.ventana_analizador = QDialog()
        instance.ventana_analizador.setWindowTitle("Analizador de datos")
        instance.ventana_analizador.resize(500, 600)  # Ancho 500, Alto 600

        # Crear un diseño para la ventana
        layout = QVBoxLayout()

        # Añadir una etiqueta
        label = QLabel("Seleccione capa a analizar:")
        layout.addWidget(label)

        # ComboBox para seleccionar la capa
        instance.inputCapaAnalisis = QComboBox()
        layers = QgsProject.instance().mapLayers().values()

        layer_list = []

        for layer in layers:
            layer_list.append(layer.name())
        instance.inputCapaAnalisis.addItems(layer_list)
        layout.addWidget(instance.inputCapaAnalisis)

        # Caja de grupo para los checkboxes de columnas
        instance.columnGroupBox = QGroupBox("Seleccione columnas a analizar:")
        instance.columnLayout = QVBoxLayout()
        instance.columnGroupBox.setLayout(instance.columnLayout)

         # Añadir un ScrollArea para manejar muchas columnas
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollWidget = QWidget()
        scrollWidget.setLayout(instance.columnLayout)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea)

        instance.inputCapaAnalisis.currentIndexChanged.connect(lambda: actualizar_columnas(instance))

        # Añadir un botón de cierre
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(lambda: generar_analisis(instance))
        buttonBox.rejected.connect(instance.ventana_analizador.reject)
        layout.addWidget(buttonBox)

        # Configurar el layout en la ventana de diálogo
        instance.ventana_analizador.setLayout(layout)

        # Conectar el evento de cierre de la ventana
        instance.ventana_analizador.finished.connect(lambda: reset_ventana_analizador(instance))

        # Mostrar la ventana
        instance.ventana_analizador.show()