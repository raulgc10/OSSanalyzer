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

# Función para hacer el conteo de las extensiones de cada usuario
def counter_ext(dict_counter):

    inverted_extensions = {value: key for key, value in extensiones.items()}
    keys_counter = {}

    for key, lista in dict_counter.items():
        ext_counter = {}
        for elemento in lista:
            if elemento in inverted_extensions:
                extension = inverted_extensions[elemento]
                if extension in ext_counter:
                    ext_counter[extension] += 1
                else:
                    ext_counter[extension] = 1
        keys_counter[key] = ext_counter
    
    new_dict = {}
    for user, extension in keys_counter.items():
        new_dict[user] = {}
        for ext, number in extension.items():
            if ext in extensiones:
                new_dict[user][extensiones[ext]] = number

    keys_counter.clear()
    keys_counter.update(new_dict)
    
    return keys_counter

# Función para definir la extensión en la que más ha trabajado cada usuario
def define_expertise(num_counter):
    final_dict={}
    for user, ext_number in num_counter.items():
        new_dict={}
        # Verificar si el diccionario de datos no está vacío
        if ext_number:
            # Obtener el tipo de archivo con el mayor conteo y su conteo
            archivo_max = max(ext_number, key=ext_number.get)
            conteo_max = ext_number[archivo_max]
            new_dict[archivo_max] = conteo_max
            final_dict[user]=new_dict
        else:
            final_dict[user]={}
    return final_dict

# Función para dar formato al json con el que se forma la página        
def dict_to_json(dictionary):
    new_json = {"data": dictionary}
    final_json = json.dumps(new_json, ensure_ascii=False)
    return final_json
    

config_load()
repo = obtain_repo_data("https://github.com/chaoss/grimoirelab-perceval.git", "/tmp/perceval.git")
users = obtain_users(repo)
changes = obtain_users_files(repo, users)

ext = obtain_files_extension(changes)
nume = counter_ext(ext)
aa = define_expertise(nume)
print (dict_to_json(aa))
