"""
Script de prueba completo para verificar que los clientes no aparezcan
en la ventana de cuentas corrientes después de eliminar sus ventas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.venta import Venta
from models.producto import Producto
from models.cliente import Cliente
from models.cuenta_corriente import CuentaCorriente
from controllers.venta_controller import VentaController
from controllers.cliente_controller import ClienteController
from controllers.producto_controller import ProductoController

def crear_datos_prueba():
    """Crear datos de prueba para la demostración"""
    print("\n=== CREANDO DATOS DE PRUEBA ===")

    # Crear un cliente
    cliente_controller = ClienteController()
    datos_cliente = {
        'nombre': "Juan Carlos",
        'apellido': "Pérez",
        'telefono': "123456789",
        'email': "juan@test.com",
        'direccion': "Calle Test 123",
        'ciudad': "Ciudad Test"
    }
    cliente_id = cliente_controller.crear_cliente(datos_cliente)

    if cliente_id:
        print(f"Cliente creado con ID: {cliente_id}")
    else:
        # Si no se pudo crear, buscar uno existente
        clientes = Cliente.obtener_todos()
        if clientes:
            cliente_id = clientes[0].id
            print(f"Usando cliente existente con ID: {cliente_id}")
        else:
            print("No se pudo crear ni encontrar cliente")
            return None, None

    # Crear un producto
    producto_controller = ProductoController()
    datos_producto = {
        'nombre': "Producto Test",
        'descripcion': "Producto para prueba",
        'precio_compra': 1000,
        'precio_venta': 1500,
        'stock': 10,
        'stock_minimo': 2,
        'categoria': "Test"
    }
    producto_id = producto_controller.crear_producto(datos_producto)

    if producto_id:
        print(f"Producto creado con ID: {producto_id}")
    else:
        # Si no se pudo crear, buscar uno existente
        productos = Producto.obtener_todos()
        if productos:
            producto_id = productos[0].id
            print(f"Usando producto existente con ID: {producto_id}")
        else:
            print("No se pudo crear ni encontrar producto")
            return None, None

    return cliente_id, producto_id

def crear_venta_prueba(cliente_id, producto_id):
    """Crear una venta de prueba"""
    print("\n=== CREANDO VENTA DE PRUEBA ===")

    venta_controller = VentaController()

    # Detalles de la venta
    detalles_venta = [{
        'producto_id': producto_id,
        'cantidad': 2,
        'precio_unitario': 1500
    }]

    # Crear la venta
    resultado = venta_controller.crear_venta(
        cliente_id=cliente_id,
        detalles_venta=detalles_venta,
        observaciones="Venta de prueba para eliminación"
    )

    if resultado:
        # Obtener la venta recién creada
        ventas = Venta.obtener_todas()
        if ventas:
            venta_id = ventas[0].id  # La más reciente debería ser la primera
            print(f"Venta creada con ID: {venta_id}, Total: $3000")
            return venta_id

    print("No se pudo crear la venta")
    return None

def mostrar_estado_cuentas():
    """Mostrar el estado actual de las cuentas corrientes"""
    print("\n=== ESTADO CUENTAS CORRIENTES ===")

    cuentas = CuentaCorriente.obtener_todas_las_cuentas()
    print(f"Cuentas con saldo pendiente: {len(cuentas)}")

    for cuenta in cuentas:
        cliente_id, nombre, apellido, saldo_total, saldo_pendiente, fecha = cuenta
        print(f"  - {nombre} {apellido}: Pendiente ${saldo_pendiente:,.0f}")

def test_completo():
    """Prueba completa del flujo"""
    print("PRUEBA COMPLETA - ELIMINACION Y DESAPARICION DE CLIENTE")
    print("="*70)

    # 1. Crear datos de prueba
    cliente_id, producto_id = crear_datos_prueba()
    if not cliente_id or not producto_id:
        print("No se pudieron crear los datos de prueba")
        return

    # 2. Mostrar estado inicial
    print("\nESTADO INICIAL:")
    mostrar_estado_cuentas()

    # 3. Crear venta
    venta_id = crear_venta_prueba(cliente_id, producto_id)
    if not venta_id:
        print("No se pudo crear la venta de prueba")
        return

    # 4. Mostrar estado después de crear venta
    print("\nESTADO DESPUES DE CREAR VENTA:")
    mostrar_estado_cuentas()

    # 5. Eliminar la venta
    print("\n=== ELIMINANDO VENTA ===")
    venta = Venta.obtener_por_id(venta_id)
    if venta:
        resultado = venta.eliminar_completa()
        if resultado:
            print("Venta eliminada exitosamente")

            # Limpiar cuenta vacía
            from controllers.cuenta_controller import CuentaController
            cuenta_controller = CuentaController()
            cuenta_controller.limpiar_cuenta_vacia(cliente_id)
            print("Limpieza de cuenta ejecutada")
        else:
            print("Error al eliminar venta")
            return
    else:
        print("Venta no encontrada")
        return

    # 6. Mostrar estado final
    print("\nESTADO FINAL:")
    mostrar_estado_cuentas()

    # 7. Verificar resultado
    cuentas_finales = CuentaCorriente.obtener_todas_las_cuentas()
    cliente_encontrado = any(cuenta[0] == cliente_id for cuenta in cuentas_finales)

    if not cliente_encontrado:
        print("\nEXITO! El cliente NO aparece en cuentas corrientes")
        print("El cliente ha desaparecido correctamente de la lista")
    else:
        print("\nFALLO: El cliente aun aparece en cuentas corrientes")
        print("Necesita revision adicional")

if __name__ == "__main__":
    test_completo()
    print("\nPrueba completada")