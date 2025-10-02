"""
Script de prueba para verificar que la ventana de productos
muestre correctamente los SKUs y tenga encabezados visibles
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.producto import Producto

def test_productos_con_sku():
    """Verificar que los productos tengan SKU"""
    print("=== VERIFICACION DE PRODUCTOS CON SKU ===")

    productos = Producto.obtener_todos()
    print(f"Total productos encontrados: {len(productos)}")

    for producto in productos:
        sku = getattr(producto, 'sku', 'NO-DEFINIDO')
        print(f"ID: {producto.id} | SKU: {sku} | Nombre: {producto.nombre} | Marca: {producto.marca}")

    # Verificar que todos tengan SKU
    productos_sin_sku = [p for p in productos if not getattr(p, 'sku', None)]

    if productos_sin_sku:
        print(f"\nADVERTENCIA: {len(productos_sin_sku)} productos sin SKU")
        print("Ejecute la funcion 'Generar SKUs' desde la interfaz")
    else:
        print("\nTodos los productos tienen SKU asignado")

def test_formato_tabla():
    """Simular el formato que se mostrará en la tabla"""
    print("\n=== SIMULACION FORMATO TABLA ===")

    productos = Producto.obtener_todos()

    # Encabezados
    print("ID".ljust(5) + "SKU".ljust(10) + "Nombre".ljust(25) +
          "Marca".ljust(15) + "Stock".ljust(8) + "Estado".ljust(15))
    print("-" * 80)

    for producto in productos:
        sku_display = getattr(producto, 'sku', 'SIN-SKU')

        # Determinar estado
        if producto.stock <= 0:
            estado = "Agotado"
        elif producto.necesita_restock():
            estado = "Stock Bajo"
        else:
            estado = "Disponible"

        print(f"{str(producto.id).ljust(5)}{sku_display.ljust(10)}{producto.nombre[:24].ljust(25)}"
              f"{(producto.marca or '').ljust(15)}{str(producto.stock).ljust(8)}{estado.ljust(15)}")

if __name__ == "__main__":
    print("PRUEBA DE VENTANA DE PRODUCTOS MEJORADA")
    print("="*50)

    test_productos_con_sku()
    test_formato_tabla()

    print("\nLa ventana de productos deberia mostrar:")
    print("1. Columna SKU visible")
    print("2. Encabezados de columnas claros")
    print("3. Productos ordenados alfabeticamente")
    print("4. Colores segun estado del stock")
    print("5. Boton 'Generar SKUs' disponible")