from flask import Flask
from utils import config_load
import logging                                
from web import create_app

# Crea una instancia de la aplicación Flask
app = create_app()


# Obtenemos el fichero de configuración
config = config_load()[0]

# Función para obtener el puerto
def port_load():
    app_port = config["mainconfig"]["port"]
    return app_port

def ip_load():
    app_ip = config["mainconfig"]["ip"]
    return app_ip
# Función para obtener configuración de los logs
def log_load():
    log_level = config["log"]["level"]
    log_filename = config["log"]["filename"]
    log_format = config["log"]["format"]

    return log_level, log_filename, log_format

# Cargamos el puerto y la config de logs
port = port_load()
ip = ip_load()
logs = log_load()

# Crea logs del programa
logging.basicConfig(level=logs[0], filename=logs[1], format=logs[2])

# Ejecuta la aplicación
if __name__ == '__main__':
    print(f"La aplicación se está ejecutando en {ip}:{port}")
    app.run(debug=False, port=port, host=ip)
