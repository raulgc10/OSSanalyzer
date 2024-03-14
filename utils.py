from perceval.backends.core.github import GitHub
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