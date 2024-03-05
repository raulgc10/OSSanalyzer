from perceval.backends.core.github import GitHub
import json

def obtener_issues_personal(repo_owner, repo_name):
    # Crea una instancia del backend de GitHub
    github_repo = GitHub(owner=repo_owner, repository=repo_name)
    repository_fetch = github_repo.fetch()
    for data in repository_fetch:
        return data
