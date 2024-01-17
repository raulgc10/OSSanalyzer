from flask import Flask

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define una ruta (endpoint) y la función que manejará las solicitudes en esa ruta
@app.route('/repository_info', methods=['GET', 'POST', 'OPTIONS'])
def mi_funcion():
    return '¡Hola desde mi endpoint!'

# Ejecuta la aplicación en el puerto 5000
if __name__ == '__main__':
    app.run(debug=True)