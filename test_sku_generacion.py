"""
Script de prueba para verificar la generación automática de SKU
y el ordenamiento alfabético en combobox
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.producto import Producto
from controllers.producto_controller import ProductoController

def mostrar_productos_existentes():
    """Mostrar productos existentes y sus SKUs"""
    print("\n=== PRODUCTOS EXISTENTES ===")
    productos = Producto.obtener_todos()

    if not productos:
        print("No hay productos en la base de datos")
        return

    for producto in productos:
        sku_display = producto.sku if producto.sku else "SIN SKU"
        print(f"ID: {producto.id} | SKU: {sku_display} | Marca: {producto.marca} | Nombre: {producto.nombre}")

def test_generar_sku():
    """Probar la generación de SKU"""
    print("\n=== PRUEBA GENERACION SKU ===")

    # Crear un producto de prueba
    producto_test = Producto(
        nombre="Producto Test SKU",
        descripcion="Producto para probar SKU",
        precio_compra=100,
        precio_venta=150,
        stock=10,
        marca="Samsung",
        categoria="Electrónicos"
    )

    # Generar SKU
    sku_generado = producto_test.generar_sku_unico()
    print(f"SKU generado para Samsung: {sku_generado}")

    # Probar con otra marca
    producto_test2 = Producto(
        nombre="Producto Sin Marca",
        descripcion="Producto sin marca",
        precio_compra=50,
        precio_venta=75,
        stock=5,
        marca="",  # Sin marca
        categoria="General"
    )

    sku_generado2 = producto_test2.generar_sku_unico()
    print(f"SKU generado sin marca: {sku_generado2}")

    # Probar con marca corta
    producto_test3 = Producto(
        nombre="Producto Marca Corta",
        descripcion="Producto con marca muy corta",
        precio_compra=75,
        precio_venta=100,
        stock=8,
        marca="LG",  # Marca corta
        categoria="Electrónicos"
    )

    sku_generado3 = producto_test3.generar_sku_unico()
    print(f"SKU generado para marca corta LG: {sku_generado3}")

def test_generar_skus_faltantes():
    """Probar la generación masiva de SKUs para productos existentes"""
    print("\n=== GENERACION MASIVA DE SKUs ===")

    controller = ProductoController()
    productos_actualizados = controller.generar_skus_faltantes()

    print(f"Productos actualizados con SKU: {productos_actualizados}")

def test_combobox_format():
    """Probar el formato para combobox"""
    print("\n=== FORMATO PARA COMBOBOX ===")

    productos_combobox = Producto.obtener_para_combobox()

    print("Formato de combobox (primeros 5):")
    for i, (producto_id, texto) in enumerate(productos_combobox[:5]):
        print(f"ID: {producto_id} | Texto: {texto}")

def test_ordenamiento_alfabetico():
    """Verificar que los productos estén ordenados alfabéticamente"""
    print("\n=== VERIFICACION ORDEN ALFABETICO ===")

    productos = Producto.obtener_todos()
    nombres = [p.nombre for p in productos]

    print("Primeros 10 productos (orden alfabético):")
    for i, nombre in enumerate(nombres[:10]):
        print(f"{i+1}. {nombre}")

    # Verificar si está ordenado
    nombres_ordenados = sorted(nombres)
    esta_ordenado = nombres == nombres_ordenados

    print(f"\nLista ordenada alfabéticamente: {'SI' if esta_ordenado else 'NO'}")

def main():
    """Función principal de pruebas"""
    print("PRUEBA COMPLETA - GENERACION SKU Y ORDEN ALFABETICO")
    print("="*60)

    # 1. Mostrar estado inicial
    mostrar_productos_existentes()

    # 2. Probar generación de SKU individual
    test_generar_sku()

    # 3. Generar SKUs para productos existentes
    test_generar_skus_faltantes()

    # 4. Mostrar estado después de generar SKUs
    print("\n=== PRODUCTOS DESPUES DE GENERAR SKUs ===")
    mostrar_productos_existentes()

    # 5. Probar formato de combobox
    test_combobox_format()

    # 6. Verificar ordenamiento alfabético
    test_ordenamiento_alfabetico()

    print("\n=== PRUEBA COMPLETADA ===")
    print("Revisar que:")
    print("1. Todos los productos tengan SKU único")
    print("2. SKU siga formato: MARCA + 3 números (ej: SAM123)")
    print("3. Productos estén ordenados alfabéticamente")
    print("4. Combobox muestre formato: ID - SKU - Nombre (Stock: X)")

if __name__ == "__main__":
    main()