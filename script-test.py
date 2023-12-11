from perceval.backends.core.github import GitHub

def obtener_issues(repo_owner, repo_name):

    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)

    # Itera sobre los issues y muestra información básica
    for issue in github_repo.fetch():
        print(f"Título: {issue['data']['title']}")
        print(f"Estado: {issue['data']['state']}")
        print(f"URL: {issue['data']['reactions']}")
        print("------")

# Proporciona el nombre del propietario del repositorio y el nombre del repositorio
propietario = 'raulgc10'
nombre_repo = 'OSSanalyzer'
tokenuser = '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'
# Llama a la función para obtener issues
obtener_issues(propietario, nombre_repo)