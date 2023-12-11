from perceval.backends.core.github import GitHub

def obtener_issues(repo_owner, repo_name):
    # Credenciales de autenticación de GitHub (token de acceso)
    token = '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'  # Reemplaza con tu token de acceso a GitHub

    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)

    # Itera sobre los issues y muestra información básica
    for issue in github_repo.fetch():
        print(f"Título: {issue['data']['title']}")
        print(f"Estado: {issue['data']['state']}")
        print(f"URL: {issue['data']['html_url']}")
        print("------")

# Proporciona el nombre del propietario del repositorio y el nombre del repositorio
propietario = 'raulgc10'
nombre_repo = 'OSSanalyzer'

# Llama a la función para obtener issues
obtener_issues(propietario, nombre_repo)