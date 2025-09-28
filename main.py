"""
Archivo principal del Sistema de Gestión Empresarial
Punto de entrada de la aplicación
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        # Verificar módulos necesarios
        import sqlite3
        import tkinter.ttk
        return True
    except ImportError as e:
        messagebox.showerror("Error de dependencias", 
                           f"Falta instalar: {str(e)}\nContacte al administrador del sistema")
        return False

def main():
    """Función principal"""
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    try:
        # Importar y ejecutar la aplicación
        from views.ventana_principal import VentanaPrincipal
        
        # Crear y ejecutar la aplicación
        app = VentanaPrincipal()
        app.ejecutar()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", 
                           f"Error al iniciar la aplicación:\n{str(e)}\n\nContacte al soporte técnico")
        sys.exit(1)

if __name__ == "__main__":
    print("Iniciando Sistema de Gestion Empresarial Pro...")
    print("Cargando modulos...")
    main()
    print("Sistema cerrado correctamente")