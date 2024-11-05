import pandas as pd
from qgis.core import QgsProject

def capa_a_dataframe(nombre_capa, columnas_seleccionadas):
    # Obtener la capa del proyecto
    capa = QgsProject.instance().mapLayersByName(nombre_capa)[0]

    # Verificar si la capa tiene datos
    if not capa or capa.featureCount() == 0:
        print(f"La capa '{nombre_capa}' no tiene datos o no se encontró.")
        return None

    # Extraer datos de los atributos de la capa
    data = []
    for feature in capa.getFeatures():
        data.append(feature.attributes())

    # Obtener nombres de todas las columnas
    columnas = [field.name() for field in capa.fields()]

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data, columns=columnas)

    # Filtrar el DataFrame para incluir solo las columnas seleccionadas
    if columnas_seleccionadas:
        df = df[columnas_seleccionadas]

    return df
