# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction


# Importaciones necesarias para trabajar con QGIS y PyQt
from qgis.core import (
    QgsSingleSymbolRenderer,
    QgsProject,  #para importar las capas de Qgis
    QgsRuleBasedRenderer,  # Para aplicar simbología basada en reglas
    QgsSymbol  # Para definir los símbolos utilizados en la representación
)

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .capy_gis_dialog import capygisDialog

from .consultas.buscar import buscar_consulta
from .consultas.cargar import cargar_consultas
from .consultas.actualizar import actualizar_consultas
from .consultas.guardar import guardar_consultas
from .modules.generador_consulta.ventana_ingrese_consulta import mostrar_ventana
from .modules.analizador_datos.ventana_analizador import mostrar_ventana_analizador
from .modules.generador_reporte.ventana_reporte import mostrar_ventana_reporte
import os


class capygis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'capygis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Capygis')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        #### VARIABLES ######
        self.json_file = os.path.join(self.plugin_dir, 'consultas.json')

        self.ventana_consulta = None
        self.consultas = None

        self.inputNombreConsulta = None
        self.inputCapaConsulta = None
        self.inputColumnaConsulta = None
        self.inputOperadorConsulta = None
        self.inputUnidadConsulta = None
        self.selectedColor = None

        self.ventana_analizador = None

        self.inputCapaAnalisis = None
        self.columnLayout = None
        self.columnGroupBox = None

        self.ventana_reporte = None
        self.inputCapaReporte = None
        self.columnLayoutReporte = None
        self.columnGroupBoxReporte = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('capygis', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/capy_gis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Capygis'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Capygis'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = capygisDialog()


        # show the dialog
        self.dlg.show()

        cargar_consultas(self)
        actualizar_consultas(self)

        self.dlg.pushButton.clicked.connect(lambda: mostrar_ventana(self))
        self.dlg.pushButton_2.clicked.connect(lambda: mostrar_ventana_analizador(self))
        self.dlg.pushButton_3.clicked.connect(lambda: mostrar_ventana_reporte(self))

        if not self.dlg.buttonBox.receivers(self.dlg.buttonBox.accepted):
            self.dlg.buttonBox.accepted.connect(self.on_seleccionar_consulta)  # Close dialog on Ok

        self.dlg.buttonBox.rejected.connect(self.dlg.reject)

        # Run the dialog event loop
        self.dlg.exec_()
        # result = self.dlg.exec_()
        # See if OK was pressed
        # if result:
        #     # Do something useful here - delete the line containing pass and
        #     #inputLayer = str(self.dlg.comboBox.currentText())

        #     # for lyr in QgsProject.instance().mapLayers().values():
        #     #     if lyr.name() == inputLayer:
        #     #         inputLayer=lyr
        #     #         break

        #     self.on_seleccionar_consulta()

        #     pass

    def aplicar_estilos(self, capa, color, expresion):
        if capa and color:
            # Limpiar el renderizador actual si existe
            if isinstance(capa.renderer(), QgsRuleBasedRenderer):
                capa.setRenderer(QgsSingleSymbolRenderer(QgsSymbol.defaultSymbol(capa.geometryType())))  # O puedes usar otro renderizador predeterminado

            # Crear símbolo y regla para consumo bajo
            simbolo = QgsSymbol.defaultSymbol(capa.geometryType())

            simbolo.setColor(QColor(color))

            # Crear la regla
            regla = QgsRuleBasedRenderer.Rule(symbol=simbolo)
            regla.setFilterExpression(expresion)

            # Crear el renderizador basado en reglas
            root_rule = QgsRuleBasedRenderer.Rule(None)
            root_rule.appendChild(regla)

            # Aplicar el renderizador a la capa
            renderer = QgsRuleBasedRenderer(root_rule)
            capa.setRenderer(renderer)
            capa.triggerRepaint()

    def ejecutar_consulta(self, consulta):
        capa = None

        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == consulta['capa']:
                capa = lyr
                break

         # Determinar si la unidad es numérica o alfanumérica
        unidad = consulta['unidad']
        if isinstance(unidad, str) and not unidad.isnumeric():
            unidad = f"'{unidad}'"  # Agrega comillas simples si es una cadena

        expresion = f"\"{consulta['columna']}\" {consulta['operador']} {unidad}"

        # Aplicar colores según el consumo
        self.aplicar_estilos(capa, consulta['color'], expresion)


    def on_seleccionar_consulta(self):
        # Ejecutar la consulta según la opción seleccionada
        seleccion = self.dlg.comboBox.currentText()
        consulta = buscar_consulta(self, seleccion)

        if consulta:
            self.ejecutar_consulta(consulta)

        # if seleccion == "Consumo bajo":
        #     self.ejecutar_consulta('B', consumo_limite, capa)
        # elif seleccion == "Consumo alto":
        #     self.ejecutar_consulta('A', consumo_limite, capa)

        self.dlg.accept()
