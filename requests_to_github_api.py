import requests

# Función para obtener el porcentaje de lenguajes usados en el repositorio
def obtain_language_percentages(username, reponame):
    url = f"https://api.github.com/repos/{username}/{reponame}/languages"
    response = requests.get(url, headers = {"Authorization": "Bearer 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"})
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
    response = requests.get(url, headers = {"Authorization": "Bearer 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"})
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

# # Función para obtener los contribuyentes de un repositorio
# def obtain_repository_contributors(username, reponame):
#     contributors=[]
#     url = f"https://api.github.com/repos/{username}/{reponame}/contributors"
#     response = requests.get(url, headers = {"Authorization": "Bearer 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"})
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
#     response = requests.get(url, headers = {"Authorization": "Bearer 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"})
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