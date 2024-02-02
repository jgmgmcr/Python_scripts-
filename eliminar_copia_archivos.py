# Listar archivos y archivos finalizando en "- copia" y eliminar estos últimos.

import os
import sys
import re

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
#ruta = 'D:\D_lahis\Videos\Youtube''\\'
ruta = 'D_el_path_que_sea''\\'
tipo_archivo = '.mp3'
marca_de_copia = " (1)"
#marca_de_copia = " - copia"

# Nombre del archivo de salida
archivo_originales = os.path.join(ruta+'archivos_originales.txt')
archivo_copia = os.path.join(ruta,'archivos_copia.txt')

# Hacer una lista con el nombre de los archivos originales y otra de lso archivos copia:
# Abre el archivo de salida en modo de escritura
with open(archivo_originales, 'w', encoding='utf-8') as fo, open(archivo_copia, 'w', encoding='utf-8') as fc:
    # Itera sobre los archivos en la ruta especificada
    for archivo in os.listdir(ruta):
        # lista archivos con copia
        if archivo.endswith(tipo_archivo) and re.match(r'^.*' + re.escape(marca_de_copia) + re.escape(tipo_archivo) + r'$', archivo):
            #print (archivo)
            # Escribe el nombre del archivo en el archivo de salida
            fc.write(archivo + '\n')
        # lista archivos sin copia
        elif archivo.endswith(tipo_archivo) and not re.match(r'^.*' + re.escape(marca_de_copia) + re.escape(tipo_archivo) + r'$',   archivo):
            #print(archivo)
            # Escribe el nombre del archivo en el archivo de salida
            fo.write(archivo + '\n')
    

# Contar archivos
# Abre el archivo de salida en modo de lectura con codificación UTF-8
with open(archivo_originales, 'r', encoding='utf-8') as fo, open(archivo_copia, 'r', encoding='utf-8') as fc:
    # Lee todas las líneas de los archivos y elimina los espacios en blanco al final
    archivos_originales = [line.rstrip() for line in fo]
    archivos_copia = [line.rstrip() for line in fc]

    # contar líneas en el archivo de originales
    line_count_originales = len(archivos_originales)
    print(f"Son {line_count_originales} los archivos originales")

    # contar líneas en el archivo de copias
    line_count_copia = len(archivos_copia)
    print(f"Son {line_count_copia} los archivos con la marca de copia")




# Compara ambas listas y elimina los archivos copia
# Abre el archivo de salida en modo de escritura
with open(archivo_originales, 'r', encoding='utf-8') as fo, open(archivo_copia, 'r', encoding='utf-8') as fc:
    # Lee las líneas de los archivos de entrada y elimina los espacios en blanco al final
    archivos_originales = [line.rstrip() for line in fo]
    #print(archivos_originales)
    archivos_copia = [line.rstrip() for line in fc]
    #print(archivos_copia)

    # contador
    cont = 0
    # Itera sobre los archivos copia
    for archivo in archivos_copia:
        #print(archivo)
        archivo_a_comparar = archivo.replace(marca_de_copia, "")
        #print(archivo_a_comparar)
        # Verifica si el archivo copia tiene una versión en los archivos originales
        if archivo_a_comparar in archivos_originales:
            # Ruta del archivo que deseas eliminar
            ruta_archivo = os.path.join(ruta, archivo)
            #print(f"Ruta del archivo a eliminar: {ruta_archivo}")
            # Verifica si el archivo existe antes de intentar eliminarlo
            if os.path.exists(ruta_archivo):
                # Elimina el archivo
                os.remove(ruta_archivo)
                print(f"El archivo {ruta_archivo} se ha eliminado exitosamente.")
                cont += 1
            else:
                print(f"El archivo {ruta_archivo} no existe en la ruta especificada.")
    print (f"Se han eliminado {cont} archivos copia")



# Eliminar los archivos de las listas creadas
archivos_a_eliminar = [archivo_originales, archivo_copia]

for archivo in archivos_a_eliminar:
    #print(archivo)
    if os.path.exists(archivo):
        os.remove(archivo)
        print(f"El listado de archivos en '{archivo}' se ha eliminado exitosamente.")
    else:
        print(f"El listado de archivos en '{archivo}' no existe en la ruta especificada.")


