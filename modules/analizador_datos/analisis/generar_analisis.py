from .capa_transform import capa_a_dataframe
from .generar_graficos import generar_graficos
from ..reset_ventana import reset_ventana_analizador

def generar_analisis(instance):
    capa = str(instance.inputCapaAnalisis.currentText())

    # Obtener las columnas seleccionadas de los checkboxes
    columnas_seleccionadas = []
    for i in range(instance.columnLayout.count()):
        checkbox = instance.columnLayout.itemAt(i).widget()
        if checkbox.isChecked():
            print(checkbox.text())
            columnas_seleccionadas.append(checkbox.text())

    if capa and columnas_seleccionadas:
        df = capa_a_dataframe(capa, columnas_seleccionadas)

        # Verificar el DataFrame y hacer análisis, por ejemplo:
        if df is not None:
            print(df.describe())    # Estadísticas descriptivas

            df = df.dropna()

            generar_graficos(df)

    instance.ventana_analizador.accept()
    reset_ventana_analizador(instance)