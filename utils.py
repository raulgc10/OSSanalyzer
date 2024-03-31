from perceval.backends.core.git import Git
import json

# Función para cargar la configuración del programa que viene de un fichero de configuración en formato JSON
def config_load(config_file):
    with open(config_file, "r") as file:
        configs = json.load(file)
    return configs

# Función para obtener los datos de un repositorio Git
def obtain_repo_data(repo_url,repo_dir):
    repo_data = Git(uri=repo_url, gitpath=repo_dir)
    return repo_data

# Función para obtener una lista con los usuarios que han trabajado en el repositorio
def obtain_users(repo):
    users=[]
    for commit in repo.fetch():
        if commit["data"]["Author"].split("<")[0] not in users:
            users.append(commit["data"]["Author"].split("<")[0])
        else:
            pass
    return users

# Función para obtener una lista con los emails de los usuarios que han trabajado en el repositorio
def obtain_emails(repo):
    emails=[]
    for commit in repo.fetch():
        if (commit["data"]["Author"].split("<")[1]).split(">")[0] not in emails:
            emails.append((commit["data"]["Author"].split("<")[1]).split(">")[0])
        else:
            pass
    return emails

# Función para obtener un diccionario de listas con los archivos en los que ha trabajado cada usuario que ha participado en el proyecto
def obtain_users_files(repo,users):
    changes = {}
    for user in users:
        changes[user] = []
    for commit in repo.fetch():  
            for user in users:  
                for file in commit["data"]["files"]:
                    if (commit["data"]["Author"].split("<")[0] == user):
                        if file["file"] not in changes[user]:
                            changes[user].append(file["file"])
                        else:
                            pass
                    else:
                        pass
    return changes

# TODO def obtain_files_extension(changes):

repo = obtain_repo_data("https://github.com/chaoss/grimoirelab-perceval.git", "/tmp/perceval.git")
users = obtain_users(repo)
obtain_users_files(repo, users)
