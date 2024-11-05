import json

def guardar_consultas(instance):
    consultas = { "consultas": instance.consultas}
    with open(instance.json_file, 'w') as f:
        json.dump(consultas, f, indent=4)