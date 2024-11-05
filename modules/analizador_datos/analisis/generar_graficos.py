import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generar_graficos(df):
    """
    Función genérica para generar histogramas superpuestos para cualquier DataFrame.
    Detecta automáticamente columnas numéricas y genera histogramas para cada una.
    """
    # Detectar automáticamente las columnas numéricas (conversión si es necesaria)
    columnas_numericas = []
    for col in df.columns:
        try:
            # Intentar convertir la columna a numérico para asegurarse de que sea usable en el gráfico
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].dtype in ['float64', 'int64']:
                columnas_numericas.append(col)
        except ValueError:
            continue

    # Verificar si hay columnas numéricas después de la conversión
    if df.empty:
        print("No hay datos numéricos para graficar en esta capa.")
        return

    # Crear el gráfico con colores distintos para cada columna
    plt.figure(figsize=(10, 6))
    colores = sns.color_palette("husl", len(df.columns))

    # Graficar histogramas superpuestos
    for i, col in enumerate(df.columns):
        plt.hist(df[col], bins=30, density=True, alpha=0.5,
                 color=colores[i], edgecolor='black', label=col)

    plt.title("Histogramas Superpuestos de Variables Numéricas")
    plt.xlabel("Valores")
    plt.ylabel("Densidad")
    plt.legend()
    plt.tight_layout()
    plt.show()