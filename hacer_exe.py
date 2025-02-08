import os

def convertir_a_ejecutable(ruta_script, ruta_destino):
    # Asegúrate de que PyInstaller esté instalado
    # pyinstaller --version
    #pip install pyinstaller

    # Ejecuta PyInstaller
    comando = f"pyinstaller --onefile  --windowed {ruta_destino} {ruta_script}"
    os.system(comando)

# Uso
ruta_script = "D:\D_\x.py"
ruta_destino = "D:\D_\"
convertir_a_ejecutable(ruta_script, ruta_destino)
