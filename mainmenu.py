from flask import Flask, render_template
import obtener_issues
import logging
import json


# Función para cargar la configuración del programa que viene de un fichero de configuración en formato JSON
def configload(config_file):
    with open(config_file, "r") as file:
        configs = json.load(file)
    return configs


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
config = configload("config/OSSAnalyzerconfig.json")

# Cargamos el puerto y la config de logs
port = ip_port_load()[0]
ip = ip_port_load()[1]
logs = log_load()

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Crea logs del programa
logging.basicConfig(level=logs[0], filename=logs[1], format=logs[2])


# Define la ruta principal en la que se darán diferentes opciones al usuario para obtener los datos de los repositorios de github
@app.route('/', methods=['GET'])
def mainpage_html():
    app.logger.info("Página principal solicitada")
    return render_template("mainpage.html")

@app.route('/mainpage.js', methods=['GET'])
def mainpage_js():
    return render_template("mainpage.js")

@app.route('/mainpage.css', methods=['GET'])
def mainpage_css():
    return render_template("mainpage.css")
# Define una ruta (endpoint) y la función que manejará las solicitudes en esa ruta
# @app.route('/userrepo', methods=['GET', 'POST'])
#
# @app.route('/url', methods=['GET', 'POST'])

# Ejecuta la aplicación
if __name__ == '__main__':
    print(f"La aplicación se está ejecutando en {ip}:{port}")
    app.run(debug=True, port=port, host=ip)
