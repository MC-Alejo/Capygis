import importlib
import subprocess
import pip

def instalar_pandas():
    try:
        importlib.import_module('pandas')
        print("Pandas ya está instalado.")
    except ImportError:
        print("Pandas no está instalado. Intentando instalarlo...")
        try:
            # Usar subprocess para ejecutar pip
            pip.main(['install', 'pandas'])
            print("Instalación completada. Por favor, reinicia QGIS para cargar el plugin.")
        except subprocess.CalledProcessError as e:
            print(f"Error instalando pandas: {e}")
            raise RuntimeError("La instalación automática de pandas falló. Intente instalar pandas manualmente.")

def instalar_matplotlib():
    try:
        importlib.import_module('matplotlib')
        print("matplotlib ya está instalado.")
    except ImportError:
        print("matplotlib no está instalado. Intentando instalarlo...")
        try:
            # Usar subprocess para ejecutar pip
            pip.main(['install', 'matplotlib'])
            print("Instalación completada. Por favor, reinicia QGIS para cargar el plugin.")
        except subprocess.CalledProcessError as e:
            print(f"Error instalando matplotlib: {e}")
            raise RuntimeError("La instalación automática de matplotlib falló. Intente instalar matplotlib manualmente.")

def instalar_seaborn():
    try:
        importlib.import_module('seaborn')
        print("seaborn ya está instalado.")
    except ImportError:
        print("seaborn no está instalado. Intentando instalarlo...")
        try:
            # Usar subprocess para ejecutar pip
            pip.main(['install', 'seaborn'])
            print("Instalación completada. Por favor, reinicia QGIS para cargar el plugin.")
        except subprocess.CalledProcessError as e:
            print(f"Error instalando seaborn: {e}")
            raise RuntimeError("La instalación automática de seaborn falló. Intente instalar seaborn manualmente.")

def instalar_reportlab():
    try:
        importlib.import_module('reportlab')
        print("reportlab ya está instalado.")
    except ImportError:
        print("reportlab no está instalado. Intentando instalarlo...")
        try:
            # Usar subprocess para ejecutar pip
            pip.main(['install', 'reportlab'])
            print("Instalación completada. Por favor, reinicia QGIS para cargar el plugin.")
        except subprocess.CalledProcessError as e:
            print(f"Error instalando reportlab: {e}")
            raise RuntimeError("La instalación automática de reportlab falló. Intente instalar reportlab manualmente.")


def verificar_e_instalar_librerias():
    try:
        instalar_pandas()
        instalar_matplotlib()
        instalar_seaborn()
        instalar_reportlab()
    except ImportError:
        print(f"Error instalando las librerias")