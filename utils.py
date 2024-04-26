from perceval.backends.core.git import Git
from collections import Counter
import json
import os

# Función para cargar la configuración del programa que viene de un fichero de configuración en formato JSON
def config_load():
    global data
    global extensiones
    with open(os.path.join("config", "OSSAnalyzerconfig.json"), "r") as file:
        data = json.load(file)
        extensiones = data.get("extensiones", {})
    return data, extensiones

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

    
    
    for value in ext_dict.values():
        for i in range(len(value)):
            for key, new_value in extensiones.items():
                if key in value[i]:
                    value[i] = new_value
    return ext_dict

def counter_ext(dict_counter):

    inverted_extensions = {value: key for key, value in extensiones.items()}
    # Creamos un nuevo diccionario para almacenar los contadores por cada clave
    keys_counter = {}

    # Iteramos sobre las claves y valores del diccionario
    for key, lista in dict_counter.items():
        # Creamos un diccionario vacío para contar las ocurrencias de cada extensión
        ext_counter = {}
        # Iteramos sobre los elementos de la lista
        for elemento in lista:
            # Verificamos si el valor del elemento coincide con alguna clave en el diccionario invertido
            if elemento in inverted_extensions:
                # Obtenemos la extensión correspondiente al valor del elemento
                extension = inverted_extensions[elemento]
                # Si la extensión ya está en el contador, incrementamos su conteo, de lo contrario, lo inicializamos en 1
                if extension in ext_counter:
                    ext_counter[extension] += 1
                else:
                    ext_counter[extension] = 1
        # Almacenamos el contador de extensiones en el nuevo diccionario
        keys_counter[key] = ext_counter
    
    # Crear un nuevo diccionario para almacenar las actualizaciones
    new_dict = {}
    # Actualizar los valores del diccionario 'archivos' con los valores del diccionario 'extensiones'
    for user, extension in keys_counter.items():
        new_dict[user] = {}
        for ext, number in extension.items():
            if ext in extensiones:
                new_dict[user][extensiones[ext]] = number

    # Actualizar el diccionario 'archivos' con los valores actualizados
    keys_counter.clear()
    keys_counter.update(new_dict)
    
    return keys_counter


config_load()
repo = obtain_repo_data("https://github.com/chaoss/grimoirelab-perceval.git", "/tmp/perceval.git")
users = obtain_users(repo)
changes = obtain_users_files(repo, users)

ext = obtain_files_extension(changes)
dict_number = counter_ext(ext)
