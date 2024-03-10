from flask import Blueprint,render_template, request
from utils import obtener_issues_personal

endpoint = Blueprint("endpoint", __name__)

# Define la ruta principal en la que se darán diferentes opciones al usuario para obtener los datos de los repositorios de github
@endpoint.route('/', methods=['GET'])
def mainpage():
    return render_template("mainpage.html")

@endpoint.route('/userrepo', methods=['GET','POST']) 
def userrepo():
    if request.method == 'GET':
            return render_template("formulario.html")
    elif request.method == 'POST':
            username = request.form['username']
            reponame = request.form['repo']
            repository_data = obtener_issues_personal(username, reponame)
            return render_template("userrepoResult.html",info=repository_data)
    else:
        return "Error al procesar la petición"

