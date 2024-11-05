import os
import json

def cargar_consultas(instance):
    """Carga las consultas desde un archivo JSON y las agrega al comboBox"""
    if os.path.exists(instance.json_file):
        with open(instance.json_file, 'r') as f:
            datos = json.load(f)
    else:
        datos = {"consultas": []}

    instance.consultas = []
    instance.consultas = datos.get('consultas', [])