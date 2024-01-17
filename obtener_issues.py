from perceval.backends.core.github import GitHub
from urllib.parse import urlparse
def obtener_issues_personal(repo_owner, repo_name):

    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)

    # Itera sobre los issues y muestra información básica
    for issue in github_repo.fetch():
        print(f"Título: {issue['data']['title']}")
        print(f"Estado: {issue['data']['state']}")
        print(f"URL: {issue['data']['reactions']}")
        print("------")


def obtener_issues_url(url_repo):
    # Parsea la URL para obtener el propietario y el nombre del repositorio
    parsed_url = urlparse(url_repo)
    path_parts = parsed_url.path.strip('/').split('/')

    if len(path_parts) != 2:
        print("La URL del repositorio no es válida.")
        return

    owner, repo_name = path_parts

    # Credenciales de autenticación de GitHub (token de acceso)
    token = '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'  # Reemplaza con tu token de acceso a GitHub

    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=owner, repository=repo_name)

    # Itera sobre los issues y muestra información básica
    for issue in github_repo.fetch():
        print(f"Título: {issue['data']['title']}")
        print(f"Estado: {issue['data']['state']}")
        print(f"URL: {issue['data']['html_url']}")
        print("------")


# Proporciona la URL completa del repositorio de GitHub
url_repositorio = 'https://github.com/raulgc10/OSSanalyzer'

# Llama a la función para obtener issues
obtener_issues_url(url_repositorio)