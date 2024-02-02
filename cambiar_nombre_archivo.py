# Cambia el nombre del tipo de archivos que se especifique por otro nombre indicado
# evitando los archivos que no hay que tocar

import os
import re

# Ruta del directorio que deseas listar
ruta = 'D:\D_el_path_que_sea'
tipo_archivo = '.mkv'
nombre_a_poner = "python.mkv"

# Itera sobre los archivos en la ruta especificada
for archivo in os.listdir(ruta):
    # Verifica si el archivo es un archivo .mkv y cumple con el modelo
    if archivo.endswith(tipo_archivo) and re.match(r'^\d+-.*\.mkv$', archivo):
        # Usa una expresión regular para extraer el número del archivo
        numero = re.findall(r'^(\d+)-', archivo)[0]
        # Crea el nuevo nombre del archivo
        nuevo_nombre = f'{numero}_{nombre_a_poner}'
        # Renombra el archivo
        os.rename(os.path.join(ruta, archivo), os.path.join(ruta, nuevo_nombre))
        



