from flask import Blueprint,render_template, request, session
from utils import obtain_repo_data, obtain_users, obtain_files_extension, obtain_emails, obtain_users_files, counter_ext, define_expertise, dict_to_json, obtain_total_commits_min_languages, top_contribuyentes_por_lenguaje, obtain_min_languages, obtain_lan
from requests_to_github_api import obtain_language_percentages, obtain_num_files, obtain_user_repos, obtain_used_languages_on_repo, obtain_last_commit, obtain_default_branch
import json
import matplotlib.pyplot as plt
import io
import base64
from .models import Repository, UserExpertise, Languages
from . import db
import utils

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
            default_branch = obtain_default_branch(username, reponame)
            last_commit = obtain_last_commit(username, reponame, default_branch)
            repository_in_db = db.session.query(Repository).filter_by(owner_name=username, repository_name=reponame).first()
            if not repository_in_db or repository_in_db.last_commit != last_commit:
                repo = obtain_repo_data(f"https://github.com/{username}/{reponame}.git", f"/tmp/{reponame}.git")
                users = obtain_users(repo)
                changes = obtain_users_files(repo, users)
                ext = obtain_files_extension(changes)
                nume = counter_ext(ext)
                repository_data = dict_to_json(nume)
                data = json.loads(repository_data)
                files_data = data["data"]
                languages_percentage = obtain_used_languages_on_repo(username, reponame)
                total_files = obtain_num_files(username, reponame)
                minoritary_languages = obtain_min_languages(languages_percentage)
                total_commits_on_min_languages = obtain_total_commits_min_languages(nume)
                top_contribuyentes_minoritarios = top_contribuyentes_por_lenguaje(nume, utils.minlanguages, top_n=100000)
                
                new_Repo = Repository(owner_name=username, repository_name=reponame, usernames = users, repo_data = data, lg_percent = languages_percentage, num_files = total_files, min_languages = minoritary_languages, default_branch = default_branch, last_commit = last_commit,total_commits_on_min_languages = total_commits_on_min_languages, min_languages_experts = top_contribuyentes_minoritarios)
                db.session.add(new_Repo)
                db.session.commit()
                for i in users:
                    user_in_db = db.session.query(UserExpertise).filter_by(user=i).first()
                    if not user_in_db:
                        repo_contrib = []
                        repo_contrib.append(reponame)
                        commits_min_languages_per_repo = {}
                        commits_min_languages_per_repo[reponame] = files_data[i]
                        new_User = UserExpertise(user=i, repositories_contribution=repo_contrib, commits_min_languages_per_repo = commits_min_languages_per_repo)
                        db.session.add(new_User)
                        db.session.commit()
                    else:
                        # Si el usuario ya existe, modificar los atributos del registro existente
                        repo_contrib = user_in_db.repositories_contribution.copy()  # Copiar para trabajar sobre ello
                        commits_min_languages_per_repo = user_in_db.commits_min_languages_per_repo.copy()  # Copiar para evitar modificar directamente
                        
                        # Asegurarse de no añadir duplicados en repositorios
                        if reponame not in repo_contrib:
                            repo_contrib.append(reponame)

                        # Actualizar los commits por lenguajes del repositorio
                        commits_min_languages_per_repo[reponame] = files_data[user_in_db.user]

                        # Asignar los valores modificados de nuevo a la base de datos (reemplazar directamente)
                        user_in_db.repositories_contribution = repo_contrib
                        user_in_db.commits_min_languages_per_repo = commits_min_languages_per_repo

                        # Marcar el objeto como modificado explícitamente y confirmar los cambios
                        db.session.commit()
                        
                lan_dict = obtain_lan(nume)

                for language, landata in lan_dict.items():
                    lan_num_commits = landata[0]  # Total de commits nuevos
                    lan_users = landata[1]  # Lista de usuarios nuevos
                    lan_num_users = landata[2]  # Número de usuarios únicos nuevos

                    # Buscar si el lenguaje ya existe en la base de datos
                    lenguaje_existente = Languages.query.filter_by(lan_name=language).first()

                    if lenguaje_existente:
                        # Si ya existe, actualizar los campos sumando los valores actuales con los nuevos
                        lenguaje_existente.lan_num_commits += lan_num_commits  # Sumar commits
                        lenguaje_existente.lan_num_users += lan_num_users  # Sumar usuarios
                        # Agregar los usuarios nuevos sin duplicar
                        lenguaje_existente.lan_users = list(set(lenguaje_existente.lan_users + lan_users))  # Usamos set para evitar duplicados
                    else:
                        # Si no existe, crear una nueva instancia y agregarla
                        nuevo_lenguaje = Languages(
                            lan_name=language,        # Nombre del lenguaje
                            lan_num_users=lan_num_users,  # Número total de usuarios
                            lan_users=lan_users,      # Lista de usuarios que han usado el lenguaje
                            lan_num_commits=lan_num_commits  # Total de commits
                        )
                        db.session.add(nuevo_lenguaje)
                
                # Confirmar los cambios en la base de datos
                db.session.commit()
            else:
                files_data = repository_in_db.repo_data["data"]
                languages_percentage = repository_in_db.lg_percent
                total_files = repository_in_db.num_files
                total_commits_on_min_languages = repository_in_db.total_commits_on_min_languages
                top_contribuyentes_minoritarios = repository_in_db.min_languages_experts
                    
            # Crear la gráfica con matplotlib
            fig, ax = plt.subplots(figsize=(14, 10))  # Aumentar el tamaño de la figura
            total = sum(languages_percentage.values())
            labels_with_percentage = [f'{key} - {value / total * 100:.1f}%' for key, value in languages_percentage.items()]
            # Crear el gráfico circular sin las etiquetas
            wedges, texts = ax.pie(
                languages_percentage.values(),
                startangle=90,  # Cambiar el ángulo de inicio para equilibrar la disposición
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}  # Añadir separación entre los sectores
            )

            # Añadir una leyenda
            ax.legend(
                wedges, labels_with_percentage,
                loc="center left",  # Ubicación de la leyenda
                bbox_to_anchor=(0.85, 0, 0.5, 1), # Posicionar la leyenda fuera del gráfico
                frameon=False,
                fontsize='x-large'
            )

            # Asegurarse de que el gráfico sea un círculo
            ax.axis('equal')

            # Añadir título
            ax.set_title('Porcentaje de uso de lenguajes')

            # Guardar la imagen en un buffer de memoria
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convertir la imagen en base64 para incrustarla en HTML
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()  # Cerrar la figura
            return render_template("userrepoResult.html", user = user, NombreUser = username, image=image_base64, NombreRepo = reponame, personas=files_data, langPercentages = languages_percentage, totalFiles = total_files, total_commits_min_languages = total_commits_on_min_languages, topcontributors = top_contribuyentes_minoritarios)
    else:
        return "Error al procesar la petición"

@endpoint.route('/usersearch', methods=['GET','POST']) 
def usersearch():
    user = session.get('user')
    if request.method == 'GET':
        return render_template("usersearchForm.html", user=user)
    elif request.method == 'POST':
        username = request.form['username']
        dict_user_repos = obtain_user_repos(username)

        return render_template("usersearchResult.html", user=user, username=username, dictuserrepos = dict_user_repos)

@endpoint.route('/perfil', methods=['GET'])
def perfil():
    user = session.get('user')
    user_to_search_on_db = request.args.get('username')
    usuariodb = db.session.query(User).filter(User.username == user_to_search_on_db).first()
    gitname = usuariodb.gitname
    dict_user_repos = obtain_user_repos(gitname)
    return render_template("perfil.html", user=user, username=gitname, dictuserrepos=dict_user_repos)
# Define la ruta para que el usuario vea algo de información sobre la página web y el proyecto 
@endpoint.route('/info', methods=['GET'])
def info():
    user = session.get('user')
    return render_template("info.html", user=user)