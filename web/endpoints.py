from flask import Blueprint,render_template, request
from utils import obtain_repo_data, obtain_users, obtain_files_extension, obtain_emails, obtain_users_files, counter_ext, define_expertise, dict_to_json
from requests_to_github_api import obtain_language_percentages, obtain_num_files, obtain_repository_contributors, obtain_repository_contributors_avatars
import json

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

            repo = obtain_repo_data(f"https://github.com/{username}/{reponame}.git", f"/tmp/{reponame}.git")
            users = obtain_users(repo)
            changes = obtain_users_files(repo, users)
            ext = obtain_files_extension(changes)
            nume = counter_ext(ext)
            aa = define_expertise(nume)
            repository_data = dict_to_json(nume)
            data = json.loads(repository_data)

            languages_percentage = obtain_language_percentages(username, reponame)
            total_files = obtain_num_files(username, reponame)
            avatars_full = obtain_repository_contributors_avatars(username, reponame)
            # Por si hay diferencias entre el diccionario con las imágenes y el diccionario de extensiones
            compare_keys = data.keys() & avatars_full.keys()
            avatars = {}
            for key in compare_keys:
                avatars[key] = avatars_full[key]
            return render_template("userrepoResult.html", NombreUser = username, NombreRepo = reponame, personas=data["data"], profileImg = avatars, langPercentages = languages_percentage, totalFiles = total_files)
    else:
        return "Error al procesar la petición"

# Define la ruta para que el usuario vea algo de información sobre la página web y el proyecto 
@endpoint.route('/info', methods=['GET'])
def info():
      return render_template("info.html")