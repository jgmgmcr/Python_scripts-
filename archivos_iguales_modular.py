# Copiar los archivos únicos que hay en 2 directorios.

import os
import sys
import shutil

"""
import ctypes
# Verificar si el script se está ejecutando como administrador en Windows
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
"""

# Establecer la codificación de salida a UTF-8 al leer los directorios y archivos
sys.stdout.reconfigure(encoding='utf-8')

# Ruta del directorio que deseas listar
ruta_A = 'D:\prueba\A''\\'
ruta_B = 'D:\prueba\B''\\'
#ruta_B = 'E:\\'

# Nombre del archivo de salida
archivo_ruta_A = os.path.join(ruta_A+'archivos_ruta_A.txt')
archivo_ruta_B = os.path.join(ruta_B,'archivos_ruta_B.txt')
archivo_unicos = os.path.join(ruta_B+'archivos_ruta_unicos.txt')

# Emparejar rutas y archivos
dic_rutas_archivos = {ruta_A:archivo_ruta_A, ruta_B:archivo_ruta_B}

# Listar los contenidos (los archivos) de ambas rutas en ambos archivos
def listar_archivos():
    for key in dic_rutas_archivos:
        with open(dic_rutas_archivos[key], 'w', encoding='utf-8') as f:
            for archivo in os.listdir(key):
                if os.path.isfile(os.path.join(key,archivo)):
                    f.write(archivo + '\n')

# Recuento de archivos
def contar_archivos():
    for key in dic_rutas_archivos:
        with open(dic_rutas_archivos[key], 'r', encoding='utf-8') as fc:
            # Lee todas las líneas de los archivos y elimina los espacios en blanco al final
            archivos_sin_espacio_final = [line.rstrip() for line in fc]
            # contar líneas en el archivo de originales
            line_count_archivos = len(archivos_sin_espacio_final)
            print(f"Son {line_count_archivos} los archivos en {key}")

# Compara ambos archivos lista y crea archivo de unicos
def comparacion_archivos_lista():
    with open(archivo_ruta_A, 'r', encoding='utf-8') as fa, open(archivo_ruta_B, 'r', encoding='utf-8') as fb, open(archivo_unicos, 'w', encoding='utf-8') as fu:
        # Lee todas las líneas de los archivos y elimina los espacios en blanco al final
        archivos_A_sin_espacio_final = [line.rstrip() for line in fa]
        archivos_B_sin_espacio_final = [line.rstrip() for line in fb]

        # contador
        cont = 0
        # Itera sobre los archivos B
        for archivo in archivos_B_sin_espacio_final:
            # Verifica si el archivo copia tiene una versión en los archivos originales
            if archivo not in archivos_A_sin_espacio_final:
                # Ruta del archivo que deseas comparar
                ruta_archivo = os.path.join(ruta_B, archivo)
                # Verifica si el archivo existe antes de intentar eliminarlo
                if os.path.exists(ruta_archivo):
                    fu.write(ruta_archivo + '\n')
                    print(f"El archivo {ruta_archivo} es un archivo único.")
                    cont +=1
                else:
                    print(f"El archivo {ruta_archivo} no existe en la ruta especificada.")
        print (f"Hay {cont} archivos únicos")

# Copia los archivos de B a A --NECESARIO PERMISOS: Abrir Visual Studio Code como Admin
def copia_archivos_unicos():
    ruta_F = ruta_A.replace('\\','/')
    ruta_F = ruta_F.replace('//','/')
    with open(archivo_unicos, 'r', encoding='utf-8') as fu:
        # Lee todas las líneas de los archivos y elimina los espacios en blanco al final
        archivos_U_sin_espacio_final = [line.rstrip() for line in fu]
        for archivo in archivos_U_sin_espacio_final:
            shutil.copyfile(archivo, ruta_F)

# copia los archivos en el directorio de este script:
def copia_archivos_dir_scrip():
    # Obtener la ruta del directorio del script
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    
    # Crear la nueva carpeta en el directorio del script
    nueva_carpeta = os.path.join(directorio_script, "Nueva_carpeta_archivos_unicos")
    os.makedirs(nueva_carpeta, exist_ok=True)
    
    # Leer el archivo de texto con las rutas de los archivos
    with open(archivo_unicos, 'r', encoding='utf-8') as fu:
        # Lee todas las líneas de los archivos y elimina los espacios en blanco al final
        archivos_U_sin_espacio_final = [line.rstrip() for line in fu]
        
        # Copiar los archivos a la nueva carpeta
        for archivo in archivos_U_sin_espacio_final:
            nombre_archivo = os.path.basename(archivo)
            ruta_destino = os.path.join(nueva_carpeta, nombre_archivo)
            shutil.copyfile(archivo, ruta_destino)

# Eliminar los archivos de las listas creadas
def eliminar_archivos_lista():
    for key in dic_rutas_archivos:
        if os.path.exists(dic_rutas_archivos[key]):
            os.remove(dic_rutas_archivos[key])
            print(f"El listado de archivos en '{dic_rutas_archivos[key]}' se ha eliminado exitosamente.")
        else:
            print(f"El listado de archivos en '{dic_rutas_archivos[key]}' no existe en la ruta especificada")


## Ejecuciones
#listar_archivos()
#contar_archivos()
#comparacion_archivos_lista()
##copia_archivos_unicos()  ####   ERROR DE PERMISOS
#copia_archivos_dir_scrip()
#eliminar_archivos_lista()


