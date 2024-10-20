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
    for key, value in ext_dict.items():
        for i in range(len(value)):
            for ext, lang in extensiones.items():
                if value[i].endswith(ext):
                    value[i] = lang
    return ext_dict

# Función para hacer el conteo de las extensiones de cada usuario
def counter_ext(dict_counter):
    keys_counter = {}

    for key, lista in dict_counter.items():
        ext_counter = {}
        for elemento in lista:
            if elemento in extensiones.values():
                extension = elemento
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
    
    
    return keys_counter

def obtain_all_files(dictionary):
    # Crear un nuevo diccionario para almacenar los valores únicos
    unique_data = {}

    # Iterar sobre las claves del diccionario original
    for key, value in dictionary.items():
        # Eliminar duplicados y convertir la lista a un conjunto
        unique_files = list(set(value))
        # Actualizar el nuevo diccionario
        unique_data[key] = unique_files

    print(unique_data)
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

def obtain_min_languages(dictionary):
    global minlanguages
    minlanguages = []

    for lang, percentage in dictionary.items():
        if percentage < 5:
            minlanguages.append(lang)
    return minlanguages

# Función para obtener la cantidad de commits totales realizados sobre ficheros de lenguajes minoritarios 
def obtain_total_commits_min_languages(dictionary):
    
    total_commits_min_languages = {}

    for user, totalcommits in dictionary.items():
        for lang, num in totalcommits.items():
            if lang in minlanguages:
                if lang in total_commits_min_languages:
                    total_commits_min_languages[lang] += num
                else:
                    total_commits_min_languages[lang] = num
    
    return total_commits_min_languages

# Función para obtener los commits de cada usuario por lenguaje minoritario
def top_contribuyentes_por_lenguaje(contribuciones, lenguajes_minoritarios, top_n=3):

    top_contribuyentes = {}
    
    for lenguaje in lenguajes_minoritarios:

        contribs_lenguaje = [(usuario, lenguajes.get(lenguaje, 0)) for usuario, lenguajes in contribuciones.items() if lenguaje in lenguajes]
        contribs_lenguaje.sort(key=lambda x: x[1], reverse=True)
        top_contribuyentes[lenguaje] = contribs_lenguaje[:top_n]
    
    top_contribuyentes_modificados = {}

    for lang, top in top_contribuyentes.items():
        if top == []:
            pass
        else:
            top_contribuyentes_modificados[lang] = top

    return top_contribuyentes_modificados

