from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit, QComboBox, QPushButton

from qgis.core import (
    QgsProject,  #para importar las capas de Qgis
)

from .reset_ventana import reset_ventana_consulta
from .columnas.cargar import cargar_columnas
from .generar import generar_consulta
from .selector_color import open_color_selector

def mostrar_ventana(instance):
    # Verificar si la ventana ya existe y, si no, crearla
    if not instance.ventana_consulta:
        # Crear un nuevo diálogo como ventana de consulta
        instance.ventana_consulta = QDialog()
        instance.ventana_consulta.setWindowTitle("Consulta Personalizada")

        # Crear un diseño para la ventana
        layout = QVBoxLayout()

        # Añadir una etiqueta
        label = QLabel("Ingresa el nómbre de la consulta personalizada:")
        layout.addWidget(label)

        instance.inputNombreConsulta = QLineEdit()
        instance.inputNombreConsulta.setAlignment(Qt.AlignLeft)
        instance.inputNombreConsulta.setFont(QFont("Arial",18))
        layout.addWidget(instance.inputNombreConsulta)

        # Añadir una etiqueta
        label = QLabel("Seleccione capa:")
        layout.addWidget(label)

        # ComboBox para seleccionar la capa
        instance.inputCapaConsulta = QComboBox()
        layers = QgsProject.instance().mapLayers().values()

        layer_list = []

        for layer in layers:
            layer_list.append(layer.name())
        instance.inputCapaConsulta.addItems(layer_list)
        layout.addWidget(instance.inputCapaConsulta)

        # Añadir una etiqueta
        label = QLabel("Seleccione columna:")
        layout.addWidget(label)

        # ComboBox para seleccionar la columna de la capa elegida
        instance.inputColumnaConsulta = QComboBox()
        cargar_columnas(instance)
        layout.addWidget(instance.inputColumnaConsulta)

        # Conectar el cambio de selección de capa al método que carga las columnas
        instance.inputCapaConsulta.currentIndexChanged.connect(lambda: cargar_columnas(instance))

        # Añadir una etiqueta
        label = QLabel("Seleccione el operador:")
        layout.addWidget(label)

        # ComboBox para seleccionar el operador
        instance.inputOperadorConsulta = QComboBox()
        instance.inputOperadorConsulta.clear()
        instance.inputOperadorConsulta.addItems(['=', '<', '>', '<=', '>='])
        layout.addWidget(instance.inputOperadorConsulta)

        # Añadir una etiqueta
        label = QLabel("Escriba el valor de comparación:")
        layout.addWidget(label)

        instance.inputUnidadConsulta = QLineEdit()
        instance.inputUnidadConsulta.setAlignment(Qt.AlignLeft)
        layout.addWidget(instance.inputUnidadConsulta)

        # Añadir una etiqueta
        label = QLabel("Seleccione un color para esta consulta:")
        layout.addWidget(label)

        # Añadir un botón para abrir el diálogo de color
        color_button = QPushButton("Color")
        layout.addWidget(color_button)

        color_button.clicked.connect(lambda: open_color_selector(instance, color_button))

        # Añadir un botón de cierre
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(lambda: generar_consulta(instance))
        buttonBox.rejected.connect(instance.ventana_consulta.reject)
        layout.addWidget(buttonBox)

        # Configurar el layout en la ventana de diálogo
        instance.ventana_consulta.setLayout(layout)

        # Conectar el evento de cierre de la ventana
        instance.ventana_consulta.finished.connect(lambda: reset_ventana_consulta(instance))

        # Mostrar la ventana
        instance.ventana_consulta.show()