from perceval.backends.core.github import GitHub
from urllib.parse import urlparse
def obtener_issues_personal(repo_owner, repo_name):
    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)

    return github_repo



def obtener_issues_url(url_repo):
    # Parsea la URL para obtener el propietario y el nombre del repositorio
    parsed_url = urlparse(url_repo)
    path_parts = parsed_url.path.strip('/').split('/')

    #Define el propietario y el nombre del repositorio
    owner, repo_name = path_parts

    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=owner, repository=repo_name)

    return github_repo

