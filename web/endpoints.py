from flask import Blueprint,render_template, request
from utils import obtain_repo_data, obtain_users, obtain_files_extension, obtain_emails, obtain_users_files, counter_ext, define_expertise

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
            repository_data = obtain_repo_data(f"https://github.com/{username}/{reponame}.git", f"/tmp/{reponame}.git")
            return render_template("userrepoResult.html",info=repository_data)
    else:
        return "Error al procesar la petición"

# Define la ruta para que el usuario vea algo de información sobre la página web y el proyecto 
@endpoint.route('/info', methods=['GET'])
def info():
      return render_template("info.html")