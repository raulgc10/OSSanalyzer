from flask import Blueprint,render_template, request, session
from utils import obtain_repo_data, obtain_users, obtain_files_extension, obtain_emails, obtain_users_files, counter_ext, define_expertise, dict_to_json
from requests_to_github_api import obtain_language_percentages, obtain_num_files
import json
import matplotlib.pyplot as plt
import io
import base64
from .models import Repository
from . import db

endpoint = Blueprint("endpoint", __name__)

# Define la ruta principal en la que se darán diferentes opciones al usuario 
@endpoint.route('/', methods=['GET'])
def mainpage():


    user = session.get('user')
    return render_template("mainpage.html", user=user)

# Ruta de ejemplo para probar
@endpoint.route('/userrepo', methods=['GET','POST']) 
def userrepo():
    user = session.get('user')
    if request.method == 'GET':
            return render_template("userrepoForm.html", user=user)
    elif request.method == 'POST':
            username = request.form['username']
            reponame = request.form['repo']
            repository_in_db = db.session.query(Repository).filter_by(owner_name=username, repository_name=reponame).first()
            if not repository_in_db:
                repo = obtain_repo_data(f"https://github.com/{username}/{reponame}.git", f"/tmp/{reponame}.git")
                users = obtain_users(repo)
                changes = obtain_users_files(repo, users)
                ext = obtain_files_extension(changes)
                nume = counter_ext(ext)
                aa = define_expertise(nume)
                repository_data = dict_to_json(nume)
                data = json.loads(repository_data)
                files_data = data["data"]
                languages_percentage = obtain_language_percentages(username, reponame)
                total_files = obtain_num_files(username, reponame)

                new_Repo = Repository(owner_name=username, repository_name=reponame, usernames = users, repo_data = data, lg_percent = languages_percentage, num_files = total_files)
                db.session.add(new_Repo)
                db.session.commit()
            else:
                files_data = repository_in_db.repo_data["data"]
                languages_percentage = repository_in_db.lg_percent
                total_files = repository_in_db.num_files
            # Crear la gráfica con matplotlib
            fig, ax = plt.subplots()
            ax.pie(languages_percentage.values(), labels=languages_percentage.keys(), autopct='%1.1f%%', startangle=0)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Porcentaje de uso de lenguajes')
            
            # Guardar la imagen en un buffer de memoria
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Convertir la imagen en base64 para incrustarla en HTML
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()  # Cerrar la figura
            return render_template("userrepoResult.html", user = user, NombreUser = username, image=image_base64, NombreRepo = reponame, personas=files_data, langPercentages = languages_percentage, totalFiles = total_files)
    else:
        return "Error al procesar la petición"

# Define la ruta para que el usuario vea algo de información sobre la página web y el proyecto 
@endpoint.route('/info', methods=['GET'])
def info():
    user = session.get('user')
    return render_template("info.html", user=user)