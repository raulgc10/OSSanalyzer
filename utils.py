from perceval.backends.core.git import Git
import json

# Función para obtener los datos de los repositorios
def obtener_issues_personal(repo_owner, repo_name):
    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)
    repository_fetch = github_repo.fetch()
    for data in repository_fetch:
        return data

# Función para cargar la configuración del programa que viene de un fichero de configuración en formato JSON
def config_load(config_file):
    with open(config_file, "r") as file:
        configs = json.load(file)
    return configs

# url for the git repo to analyze
repo_url = 'http://github.com/grimoirelab/perceval.git'
# directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'

def obtain_repo_data(repo_url,repo_dir):
    repo_data = Git(uri=repo_url, gitpath=repo_dir)
    return repo_data

def obtain_users(repo):
    users=[]
    for commit in repo.fetch():
        if commit["data"]["Author"].split("<")[0] not in users:
            users.append(commit["data"]["Author"].split("<")[0])
        else:
            pass
    return users


def obtain_emails(repo):
    emails=[]
    for commit in repo.fetch():
        if (commit["data"]["Author"].split("<")[1]).split(">")[0] not in emails:
            emails.append((commit["data"]["Author"].split("<")[1]).split(">")[0])
        else:
            pass
    return emails

def obtain_users_files(repo,users):
    changes = {}
    for user in users:
        changes[user] = []
    for commit in repo.fetch():  
            for user in users:  
                if (commit["data"]["Author"].split("<")[0] == user):
                    if commit["data"]["files"][0]["file"] not in changes[user]:
                        changes[user].append(commit["data"]["files"][0]["file"])
                    else:
                        pass
                else:
                    pass
    print (changes)

repo = obtain_repo_data("http://github.com/grimoirelab/perceval.git", "/tmp/perceval.git")
users = obtain_users(repo)
obtain_users_files(repo, users)

