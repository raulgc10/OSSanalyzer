from perceval.backends.core.git import Git
from collections import Counter
import json
import os

# Función para cargar la configuración del programa que viene de un fichero de configuración en formato JSON
def config_load(config_file):
    with open(config_file, "r") as file:
        configs = json.load(file)
    return configs

# Función para obtener los datos de un repositorio Git
def obtain_repo_data(repo_url,repo_dir):
    repo_data = Git(uri=repo_url, gitpath=repo_dir)
    return repo_data

# Función para obtener una lista con los usuarios que han trabajado en el repositorio
def obtain_users(repo):
    users=[]
    for commit in repo.fetch():
        if commit["data"]["Author"].split("<")[0] not in users:
            users.append(commit["data"]["Author"].split("<")[0])
        else:
            pass
    return users

# Función para obtener una lista con los emails de los usuarios que han trabajado en el repositorio
def obtain_emails(repo):
    emails=[]
    for commit in repo.fetch():
        if (commit["data"]["Author"].split("<")[1]).split(">")[0] not in emails:
            emails.append((commit["data"]["Author"].split("<")[1]).split(">")[0])
        else:
            pass
    return emails

# Función para obtener un diccionario de listas con los archivos en los que ha trabajado cada usuario que ha participado en el proyecto
def obtain_users_files(repo,users):
    file_dict = {}
    for user in users:
        file_dict[user] = []
    for commit in repo.fetch():  
            for user in users:  
                for file in commit["data"]["files"]:
                    if (commit["data"]["Author"].split("<")[0] == user):
                        if file["file"] not in file_dict[user]:
                            file_dict[user].append(file["file"])
                        else:
                            pass
                    else:
                        pass
    return file_dict

# Función para obtener las extensiones de los archivos que ha modificado cada usuario
def obtain_files_extension(ext_dict):

    with open(os.path.join("config", "OSSAnalyzerconfig.json"), "r") as file:
        data = json.load(file)
        extensiones = data.get("extensiones", {})
    
    for value in ext_dict.values():
        for i in range(len(value)):
            for key, new_value in extensiones.items():
                if key in value[i]:
                    value[i] = new_value
    return ext_dict

def counter_ext(dict_counter):

    with open(os.path.join("config", "OSSAnalyzerconfig.json"), "r") as file:
        data = json.load(file)
        extensiones = data.get("extensiones", {})
    extensiones_invertido = {valor: clave for clave, valor in extensiones.items()}
    # Creamos un nuevo diccionario para almacenar los contadores por cada clave
    contadores_por_key = {}

    # Iteramos sobre las claves y valores del diccionario
    for key, lista in dict_counter.items():
        # Creamos un diccionario vacío para contar las ocurrencias de cada extensión
        contador_extensiones = {}
        # Iteramos sobre los elementos de la lista
        for elemento in lista:
            # Verificamos si el valor del elemento coincide con alguna clave en el diccionario invertido
            if elemento in extensiones_invertido:
                # Obtenemos la extensión correspondiente al valor del elemento
                extension = extensiones_invertido[elemento]
                # Si la extensión ya está en el contador, incrementamos su conteo, de lo contrario, lo inicializamos en 1
                if extension in contador_extensiones:
                    contador_extensiones[extension] += 1
                else:
                    contador_extensiones[extension] = 1
        # Almacenamos el contador de extensiones en el nuevo diccionario
        contadores_por_key[key] = contador_extensiones
        
    print (contadores_por_key)
            
repo = obtain_repo_data("https://github.com/TypesettingTools/Aegisub-Motion.git", "/tmp/aegisub-motion.git")
users = obtain_users(repo)
changes = obtain_users_files(repo, users)

ext = obtain_files_extension(changes)
counter_ext(ext)