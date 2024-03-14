from flask import Blueprint,render_template, request
from utils import obtener_issues_personal

endpoint = Blueprint("endpoint", __name__)

# Define la ruta principal en la que se darán diferentes opciones al usuario 
@endpoint.route('/', methods=['GET'])
def mainpage():
    return render_template("mainpage.html")

# Ruta de ejemplo para probar
@endpoint.route('/userrepo', methods=['GET','POST']) 
def userrepo():
    if request.method == 'GET':
            return render_template("userrepoForm.html")
    elif request.method == 'POST':
            username = request.form['username']
            reponame = request.form['repo']
            repository_data = obtener_issues_personal(username, reponame)
            return render_template("userrepoResult.html",info=repository_data)
    else:
        return "Error al procesar la petición"

# Define la ruta para que el usuario vea algo de información sobre la página web y el proyecto 
@endpoint.route('/info', methods=['GET'])
def info():
      return render_template("info.html")