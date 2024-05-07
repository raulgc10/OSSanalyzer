import requests

def obtain_language_percentages(username, reponame):
    url = f"https://api.github.com/repos/{username}/{reponame}/languages"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        total_bytes = sum(data.values())
        porcentajes = {language: (bytes / total_bytes) * 100 for language, bytes in data.items()}
        porcentajes_truncados = {lenguaje: round(porcentaje, 2) for lenguaje, porcentaje in porcentajes.items()}
        return porcentajes_truncados
    else:
        print(f"No se pudo obtener la información. Código de estado: {response.status_code}")
        return None

def obtener_numero_archivos(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    response = requests.get(url)
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
        return counter_files
    else:
        print(f"No se pudo obtener la información. Código de estado: {response.status_code}")
        return None

    
print(obtener_numero_archivos("raulgc10","OSSAnalyzer"))