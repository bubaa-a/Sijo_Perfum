"""
Script para generar el ejecutable del Sistema de Inventario Pro
"""
import os
import subprocess
import sys

def build_executable():
    """Crear el ejecutable con PyInstaller"""

    print("Iniciando creacion del ejecutable...")
    print("=" * 50)

    # Configuración para PyInstaller
    command = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (solo GUI)
        "--name=SistemaInventarioPro",  # Nombre del ejecutable
        "--distpath=.",                 # Crear en directorio actual
        "--workpath=temp_build",        # Directorio temporal
        "--specpath=temp_build",        # Archivo spec temporal
        "main.py"                       # Archivo principal
    ]

    try:
        print("Ejecutando PyInstaller...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        print("Ejecutable creado exitosamente!")
        print("Ubicacion: SistemaInventarioPro.exe")
        print("=" * 50)
        print("Listo para usar!")

    except subprocess.CalledProcessError as e:
        print(f"Error al crear ejecutable: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")

    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    build_executable()