"""
Funciones auxiliares y utilidades
"""
import re
from datetime import datetime

def validar_email(email):
    """Validar formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Validar formato de teléfono chileno"""
    # Remover espacios y caracteres especiales
    telefono_limpio = re.sub(r'[^\d+]', '', telefono)
    
    # Patrones válidos para Chile
    patrones = [
        r'^\+56\d{8,9}$',  # +56XXXXXXXX
        r'^56\d{8,9}$',    # 56XXXXXXXX
        r'^\d{8,9}$'       # XXXXXXXX
    ]
    
    return any(re.match(patron, telefono_limpio) for patron in patrones)

def formatear_precio(precio):
    """Formatear precio como moneda chilena"""
    try:
        return f"${float(precio):,.0f}"
    except (ValueError, TypeError):
        return "$0"

def formatear_fecha(fecha):
    """Formatear fecha para mostrar"""
    if isinstance(fecha, str):
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return fecha
    
    return fecha.strftime('%d/%m/%Y %H:%M')

def calcular_porcentaje_ganancia(precio_compra, precio_venta):
    """Calcular porcentaje de ganancia"""
    try:
        if float(precio_compra) > 0:
            return ((float(precio_venta) - float(precio_compra)) / float(precio_compra)) * 100
        return 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def limpiar_numero(texto):
    """Limpiar texto y convertir a número"""
    try:
        # Remover caracteres no numéricos excepto punto y coma
        numero_limpio = re.sub(r'[^\d.,]', '', str(texto))
        # Reemplazar coma por punto
        numero_limpio = numero_limpio.replace(',', '.')
        return float(numero_limpio)
    except (ValueError, TypeError):
        return 0

def generar_codigo_producto(nombre, categoria=""):
    """Generar código automático para producto"""
    import random
    
    # Tomar primeras 3 letras del nombre
    codigo_nombre = re.sub(r'[^a-zA-Z]', '', nombre.upper())[:3]
    if len(codigo_nombre) < 3:
        codigo_nombre = codigo_nombre.ljust(3, 'X')
    
    # Tomar primeras 2 letras de categoría
    codigo_categoria = re.sub(r'[^a-zA-Z]', '', categoria.upper())[:2]
    if len(codigo_categoria) < 2:
        codigo_categoria = codigo_categoria.ljust(2, 'X')
    
    # Número aleatorio
    numero = random.randint(100, 999)
    
    return f"{codigo_nombre}-{codigo_categoria}-{numero}"

def exportar_a_csv(datos, nombre_archivo):
    """Exportar datos a archivo CSV"""
    import csv
    from tkinter import filedialog, messagebox
    
    try:
        # Solicitar ubicación de guardado
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialvalue=nombre_archivo
        )
        
        if archivo:
            with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
                if datos:
                    # Obtener headers de las claves del primer elemento
                    headers = datos[0].keys() if isinstance(datos[0], dict) else range(len(datos[0]))
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    
                    # Escribir headers
                    writer.writeheader()
                    
                    # Escribir datos
                    for fila in datos:
                        writer.writerow(fila)
            
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo}")
            return True
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    return False

def backup_base_datos():
    """Crear backup de la base de datos"""
    import shutil
    from tkinter import filedialog, messagebox
    from datetime import datetime
    
    try:
        # Generar nombre con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_backup = f"inventario_backup_{timestamp}.db"
        
        # Solicitar ubicación
        archivo_backup = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            initialvalue=nombre_backup
        )
        
        if archivo_backup:
            shutil.copy2("inventario.db", archivo_backup)
            messagebox.showinfo("Éxito", f"Backup creado correctamente:\n{archivo_backup}")
            return True
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear backup: {str(e)}")
    
    return False