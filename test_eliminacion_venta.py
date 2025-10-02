"""
Script de prueba para verificar la eliminación correcta de ventas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.venta import Venta
from models.producto import Producto
from models.cliente import Cliente
from models.cuenta_corriente import CuentaCorriente
from controllers.venta_controller import VentaController

def mostrar_estado_base_datos():
    """Mostrar estado actual de la base de datos"""
    print("\n" + "="*60)
    print("ESTADO ACTUAL DE LA BASE DE DATOS")
    print("="*60)

    # Ventas
    ventas = Venta.obtener_todas()
    print(f"\nVENTAS ({len(ventas)}):")
    for venta in ventas:
        print(f"  - Venta #{venta.id}: Cliente {venta.cliente_id}, Total: ${venta.total:,.0f}")

    # Productos (solo mostrar algunos campos clave)
    productos = Producto.obtener_todos()
    print(f"\nPRODUCTOS ({len(productos)}):")
    for producto in productos[:5]:  # Solo mostrar los primeros 5
        print(f"  - {producto.nombre}: Stock {producto.stock}")

    # Cuentas corrientes
    cuentas = CuentaCorriente.obtener_todas_las_cuentas()
    print(f"\nCUENTAS CORRIENTES ({len(cuentas)}):")
    for cuenta in cuentas:
        cliente_id, nombre, apellido, saldo_total, saldo_pendiente, fecha = cuenta
        print(f"  - {nombre} {apellido}: Total ${saldo_total:,.0f}, Pendiente ${saldo_pendiente:,.0f}")

def test_eliminacion_venta():
    """Probar la eliminación de una venta"""
    print("\nINICIANDO PRUEBA DE ELIMINACION")
    print("="*60)

    # Mostrar estado inicial
    print("\nESTADO INICIAL:")
    mostrar_estado_base_datos()

    # Buscar una venta para eliminar
    ventas = Venta.obtener_todas()
    if not ventas:
        print("\nNo hay ventas para probar la eliminacion")
        return

    venta_a_eliminar = ventas[0]  # Tomar la primera venta
    print(f"\nSELECCIONADA PARA ELIMINACION:")
    print(f"   Venta #{venta_a_eliminar.id}")
    print(f"   Cliente: {venta_a_eliminar.cliente_id}")
    print(f"   Total: ${venta_a_eliminar.total:,.0f}")

    # Obtener detalles completos de la venta
    venta_completa = Venta.obtener_por_id(venta_a_eliminar.id)
    if not venta_completa:
        print("No se pudo obtener la venta completa")
        return

    print(f"\nDETALLES DE LA VENTA:")
    for detalle in venta_completa.detalles:
        print(f"   - Producto {detalle.producto_id}: {detalle.cantidad} unidades")

    # Usar el controlador para eliminar
    controller = VentaController()
    print(f"\nELIMINANDO VENTA...")

    # Nota: Como estamos en modo de prueba, vamos a llamar directamente
    # al método eliminar_completa() para evitar los diálogos de confirmación
    resultado = venta_completa.eliminar_completa()

    if resultado:
        print("Venta eliminada exitosamente")

        # Limpiar cuenta vacía si es necesario
        if venta_completa.cliente_id:
            from controllers.cuenta_controller import CuentaController
            cuenta_controller = CuentaController()
            cuenta_controller.limpiar_cuenta_vacia(venta_completa.cliente_id)
            print("Limpieza de cuenta corriente ejecutada")

        print("\nESTADO FINAL:")
        mostrar_estado_base_datos()

    else:
        print("Error al eliminar la venta")

if __name__ == "__main__":
    print("SCRIPT DE PRUEBA - ELIMINACION DE VENTAS")
    test_eliminacion_venta()
    print("\nPrueba completada")