import requests
import os
import json
import math

# Obtener la ruta del archivo JSON en la subcarpeta 'config'
ruta_config = os.path.join(os.path.dirname(__file__), 'config', 'OSSAnalyzerconfig.json')

# Abrir y leer el archivo JSON
with open(ruta_config, 'r') as config_file:
    config_data = json.load(config_file)

# Obtener un campo específico (por ejemplo, el nombre del autor)
github_token = config_data.get('git_token')

headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
}

# Función para obtener el porcentaje de lenguajes usados en el repositorio
def obtain_language_percentages(username, reponame):
    url = f"https://api.github.com/repos/{username}/{reponame}/languages"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_bytes = sum(data.values())
        porcentajes = {language: (bytes / total_bytes) * 100 for language, bytes in data.items()}
        porcentajes_truncados = {lenguaje: round(porcentaje, 2) for lenguaje, porcentaje in porcentajes.items()}
        return porcentajes_truncados
    else:
        return response.status_code

# Función para obtener el número de archivos totales de un repositorio 
def obtain_num_files(username, reponame):
    url = f"https://api.github.com/repos/{username}/{reponame}/contents"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        counter_files = 0
        for file in data:
            if file["type"] == "file":
                counter_files += 1
            elif file["type"] == "dir":
                base_url = file["_links"]["git"]
                response_dir = requests.get(f"{base_url}?recursive=30")
                if response_dir.status_code == 200:
                    data_dir = response_dir.json()
                    for file_dir in data_dir["tree"]:
                        if file_dir["type"] == "blob":
                            counter_files +=1
                else:
                    return response_dir.status_code
        return counter_files
    else:
        return response.status_code

# Función para obtener los repositorios de los que un usuario es propietario
def obtain_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        dictrepos = {}
        for repo in data:
            dictrepos[repo["name"]] = repo["language"]
        return dictrepos
    else:
        return response.status_code

def obtain_used_languages_on_repo(username, repo):
    extension_to_language = config_data.get("extensiones", {})
    url = f"https://api.github.com/repos/{username}/{repo}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        default_branch = data.get('default_branch')
    else:
        return response.status_code

    branch_url = f'https://api.github.com/repos/{username}/{repo}/branches/{default_branch}'
    branch_response = requests.get(branch_url, headers=headers)

    if branch_response.status_code == 200:
        branch_data = branch_response.json()
        sha = branch_data['commit']['sha']

    tree_url = f'https://api.github.com/repos/{username}/{repo}/git/trees/{sha}?recursive=3000'
    response = requests.get(tree_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        files = data.get('tree', [])
    else:
        return response.status_code
    
    # Contador de lenguajes
    language_count = {}

    # Analizar la extensión de cada archivo para identificar el lenguaje
    for file in files:
        file_path = file['path']
        file_extension = os.path.splitext(file_path)[1]  # Obtener la extensión del archivo

        # Si la extensión está en nuestro diccionario de lenguajes
        if file_extension in extension_to_language:
            language = extension_to_language[file_extension]
            if language in language_count:
                language_count[language] += 1
            else:
                language_count[language] = 1

    # Calcular el porcentaje de cada lenguaje en función del número de archivos
    total_files = sum(language_count.values())
    dict_perc = {}
    if total_files > 0:

        for language, count in language_count.items():
            percentage = round(count / total_files * 100,2)
            dict_perc[language] = percentage
        
        return dict_perc

    else:
        return "No se detectaron lenguajes en el repositorio."
# # Función para obtener los contribuyentes de un repositorio
# def obtain_repository_contributors(username, reponame):
#     contributors=[]
#     url = f"https://api.github.com/repos/{username}/{reponame}/contributors"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         for contributor in data:
#             contributors.append(contributor["login"])
#         # La API de github proporciona únicamente 30 por defecto
#         while 'next' in response.links.keys():
#             next_url = response.links["next"]["url"]
#             response = requests.get(next_url)
#             if response.status_code == 200:
#                 data = response.json()
#                 for contributor in data:
#                     contributors.append(contributor["login"])
#             else:
#                 return response.status_code
        
#         return contributors
#     else:
#         return response.status_code

# # Función para obtener los contribuyentes de un repositorio
# def obtain_repository_contributors_avatars(username, reponame):
#     avatar_dict={}
#     url = f"https://api.github.com/repos/{username}/{reponame}/contributors"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         for contributor in data:
#             avatar_dict[contributor["login"]] = contributor["avatar_url"]
#         # La API de github proporciona únicamente 30 por defecto
#         while 'next' in response.links.keys():
#             next_url = response.links["next"]["url"]
#             response = requests.get(next_url)
#             if response.status_code == 200:
#                 data = response.json()
#                 for contributor in data:
#                     avatar_dict[contributor["login"]] = contributor["avatar_url"]
#             else:
#                 return response.status_code
        
#         return avatar_dict
#     else:
#         return response.status_code
# print(obtain_repository_contributors_avatars("chaoss", "grimoirelab-perceval"))