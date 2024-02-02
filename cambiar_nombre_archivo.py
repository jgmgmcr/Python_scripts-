"""Para listar los archivos de un directorio en Windows usando Python, puedes usar el módulo `os`. Aquí está el código que necesitas:"""
# evitando los archivos que no hay que tocar

import os
import re

# Ruta del directorio que deseas listar
ruta = 'D:\D_lahis\Videos\Youtube'
tipo_archivo = '.mkv'
nombre_a_poner = "python_tutorizado.mkv"

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
        













"""

#### SIN REGEX

```python"""
"""
import os

# Ruta del directorio que deseas listar
ruta = 'D:\D_lahis\Videos\Youtube'

# Lista los archivos y carpetas en la ruta especificada
for archivo in os.listdir(ruta):
    # Verifica si el archivo es un archivo .mkv
    if archivo.endswith('.mkv'):
        # Separa el nombre del archivo en dos partes
        nombre, extension = os.path.splitext(archivo)
        # Separa la primera parte del nombre del archivo en dos partes
        numero, texto = nombre.split('-', 1)
        # Crea el nuevo nombre del archivo
        nuevo_nombre = f'{numero}_python_tutorizado{extension}'
        # Renombra el archivo
        os.rename(os.path.join(ruta, archivo), os.path.join(ruta, nuevo_nombre))
"""
"""
```

En este ejemplo, la ruta del directorio que se desea listar es `C:/Users/Usuario/Documentos`. Asegúrate de cambiar la ruta a la que deseas listar.

Este código lista los archivos y carpetas en la ruta especificada y verifica si el archivo es un archivo `.mkv`. Si es así, separa el nombre del archivo en dos partes: el número y el texto. Luego, crea el nuevo nombre del archivo reemplazando la parte del texto por "hola" y renombra el archivo.

¡Espero que esto te ayude! 😊.

Origen: Conversación con Bing, 25/11/2023
(1) Script de cambio de nombre de archivos en python 3.5. https://es.stackoverflow.com/questions/16739/script-de-cambio-de-nombre-de-archivos-en-python-3-5.
(2) Python - Renombrar un archivo - decodigo.com. https://decodigo.com/python-renombrar-un-archivo.
(3) Cambiar el nombre de un archivo en Python - Techie Delight. https://www.techiedelight.com/es/how-to-rename-a-file-in-python/.
(4) Cómo listar los archivos de una carpeta: en Windows 10, 11 - CCM. https://es.ccm.net/ordenadores/windows/3108-windows-listar-los-archivos-contenidos-en-una-carpeta/.
(5) Cómo listar contenido de directorios en Windows usando la herramienta .... https://www.renel.pe/programacion/dos/dir-listar-contenido-de-directorios/.
(6) Como listar los archivos de un directorio en Windows?. https://tusconsejosrapidos.com/como-listar-los-archivos-de-un-directorio-en-windows/.
(7) Crea un listado con los archivos de una carpeta en Windows - SoftZone. https://www.softzone.es/windows/como-se-hace/crear-listado-todos-ficheros-carpeta/.
(8) Listar los archivos de una carpeta y subcarpetas: CMD, TXT. https://es.ccm.net/ordenadores/windows/2122-ms-dos-listar-el-contenido-de-un-directorio-en-un-archivo-de-texto/.
"""

"""
####  CON REGEX:

¡Buena pregunta! En efecto, podrías utilizar expresiones regulares (regex) para lograr el mismo resultado. Python tiene un módulo incorporado llamado `re` que te permite trabajar con expresiones regulares. Aquí hay un ejemplo de cómo podrías usarlo para cambiar el nombre de los archivos en un directorio de Windows:

```python"""
"""
import os
import re

# Ruta del directorio que deseas listar
ruta = 'D:\D_lahis\Videos\Youtube'

# Itera sobre los archivos en la ruta especificada
for archivo in os.listdir(ruta):
    # Verifica si el archivo es un archivo .mkv
    if archivo.endswith('.mkv'):
        # Usa una expresión regular para extraer el número del archivo
        numero = re.findall(r'^(\d+)-', archivo)[0]
        # Crea el nuevo nombre del archivo
        nuevo_nombre = f'{numero}_python_tutorizado.mkv'
        # Renombra el archivo
        os.rename(os.path.join(ruta, archivo), os.path.join(ruta, nuevo_nombre))

"""
"""
```

En este ejemplo, la ruta del directorio que se desea listar es `C:/Users/Usuario/Documentos`. Asegúrate de cambiar la ruta a la que deseas listar.

Este código utiliza una expresión regular para extraer el número del archivo. La expresión regular `^(\d+)-` busca una cadena que comience con uno o más dígitos seguidos de un guión. El número se captura en un grupo de captura y se accede mediante el índice `[0]`. Luego, se crea el nuevo nombre del archivo reemplazando la parte del texto por "hola" y renombra el archivo.

¡Espero que esto te ayude! 😊..

Origen: Conversación con Bing, 25/11/2023
(1) Regular Expression HOWTO — Python 3.12.0 documentation. https://docs.python.org/3/howto/regex.html.
(2) RegEx en Python de un vistazo - IONOS. https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/regex-en-python/.
(3) Python RegEx (With Examples) - Programiz. https://www.programiz.com/python-programming/regex.
(4) Python RegEx - W3Schools. https://www.w3schools.com/python/python_regex.asp.
(5) re — Operaciones con expresiones regulares - Python. https://docs.python.org/es/3/library/re.html.
(6) es.wikipedia.org. https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular.


"""