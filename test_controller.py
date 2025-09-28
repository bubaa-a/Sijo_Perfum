"""
Probar el controller de cuentas corrientes
"""
from controllers.cuenta_controller import CuentaController
from models.cliente import Cliente

def probar_controller():
    try:
        print("Probando controller de cuentas...")
        
        # Obtener clientes
        clientes = Cliente.obtener_todos()
        print(f"Clientes encontrados: {len(clientes)}")
        
        for cliente in clientes:
            print(f"- {cliente.nombre} {cliente.apellido}")
        
        # Probar controller
        controller = CuentaController()
        
        # Obtener resumen
        resumen = controller.obtener_resumen_cuentas()
        print(f"\nResumen de cuentas:")
        print(f"- Total clientes con deuda: {resumen['total_clientes_deuda']}")
        print(f"- Total deuda pendiente: ${resumen['total_deuda_pendiente']:,.0f}")
        print(f"- Cuentas encontradas: {len(resumen['cuentas'])}")
        
        # Mostrar cuentas
        for cuenta in resumen['cuentas']:
            nombre = f"{cuenta[1]} {cuenta[2]}"
            saldo = cuenta[4]
            print(f"  - {nombre}: ${saldo:,.0f}")
        
        print("\nController funciona correctamente!")
        
    except Exception as e:
        print(f"ERROR en controller: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    probar_controller()