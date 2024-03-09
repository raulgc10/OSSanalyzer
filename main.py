from flask import Flask, render_template, request, jsonify
from utils import obtener_issues_personal, config_load
import logging
import json
from web import create_app


# Crea una instancia de la aplicación Flask
app = create_app()

# Función para obtener el puerto
def ip_port_load():
    app_port = config["mainconfig"]["port"]
    app_ip = config["mainconfig"]["ip"]
    return app_port, app_ip


# Función para obtener configuración de los logs
def log_load():
    log_level = config["log"]["level"]
    log_filename = config["log"]["filename"]
    log_format = config["log"]["format"]

    return log_level, log_filename, log_format


# Obtenemos el fichero de configuración
config = config_load("config/OSSAnalyzerconfig.json")

# Cargamos el puerto y la config de logs
port = ip_port_load()[0]
ip = ip_port_load()[1]
logs = log_load()

# Crea logs del programa
logging.basicConfig(level=logs[0], filename=logs[1], format=logs[2])

# Ejecuta la aplicación
if __name__ == '__main__':
    print(f"La aplicación se está ejecutando en {ip}:{port}")
    app.run(debug=True, port=port, host=ip)
