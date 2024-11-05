from qgis.PyQt.QtWidgets import QColorDialog

def open_color_selector(instance, button):
        color = QColorDialog.getColor()
        if color.isValid():
            instance.selectedColor = color.name()  # Guarda el color seleccionado
            button.setStyleSheet(f"background-color: {color.name()};")  # Muestra el color seleccionado en el botón