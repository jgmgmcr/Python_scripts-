import os
import zipfile
import tarfile
import rarfile


ruta='D:\PRUEBA'

##### Comprimir archivos

def zipdir(path, ziph):
    # ziph es la referencia al archivo zip
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
            except Exception as e:
                print(f"Error al agregar el archivo {file} al zip: {e}")

def comprimir(directory):
    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)):
            try:
                with zipfile.ZipFile(os.path.join(directory,f'{folder}.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipdir(os.path.join(directory, folder), zipf)
            except Exception as e:
                print(f"Error al crear el archivo zip para {folder}: {e}")

#comprimir(ruta) 

"""
Las funciones main(directory) y zipdir(path, ziph) trabajan juntas para lograr el objetivo de comprimir los directorios, pero cada una tiene un propósito distinto:

zipdir(path, ziph): Esta función se encarga de comprimir todos los archivos en un directorio dado en un archivo .zip. No se preocupa por subdirectorios o la creación del archivo .zip, solo agrega archivos a un archivo .zip existente.
main(directory): Esta función es la que recorre los subdirectorios en un directorio dado, crea un archivo .zip para cada uno y llama a zipdir(path, ziph) para agregar los archivos al .zip.
Por lo tanto, aunque ambas funciones están relacionadas y trabajan juntas, no son similares en términos de lo que hacen. Cada una tiene un papel específico en el proceso de compresión de directorios. 
"""

##### Descomprimir

def descomprimir(directory):
    for item in os.listdir(directory):
        if item.endswith('.zip') or item.endswith('.tar') or item.endswith('.rar'):
            file_path = os.path.join(directory, item)
            extract_path = os.path.join(directory, os.path.splitext(item)[0])
            if not os.path.exists(extract_path):
                try:
                    if item.endswith('.zip'):
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_path)
                    elif item.endswith('.tar'):
                        with tarfile.open(file_path, 'r') as tar_ref:
                            tar_ref.extractall(extract_path)
                    elif item.endswith('.rar'):
                        with rarfile.RarFile(file_path, 'r') as rar_ref:
                            rar_ref.extractall(extract_path)
                except Exception as e:
                    print(f"Error al descomprimir el archivo {item}: {e}")
            else:
                print(f"El directorio {extract_path} ya existe, se omite la descompresión.")

descomprimir(ruta)
