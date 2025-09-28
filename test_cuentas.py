"""
Archivo para probar y crear las tablas de cuentas corrientes
"""
from config.database import DatabaseManager

def verificar_y_crear_tablas():
    """Verificar y crear tablas de cuentas corrientes"""
    try:
        db = DatabaseManager()
        conn = db.conectar()
        cursor = conn.cursor()
        
        # Crear tabla de cuentas corrientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas_corrientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                saldo_total REAL DEFAULT 0,
                saldo_pendiente REAL DEFAULT 0,
                fecha_ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activa BOOLEAN DEFAULT 1,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')
        
        # Crear tabla de movimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos_cuenta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                monto REAL NOT NULL,
                descripcion TEXT,
                venta_id INTEGER,
                fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (venta_id) REFERENCES ventas(id)
            )
        ''')
        
        # Crear tabla de abonos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS abonos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                monto_abono REAL NOT NULL,
                metodo_pago TEXT DEFAULT 'Efectivo',
                descripcion TEXT,
                recibo_numero TEXT,
                fecha_abono TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_registro TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')
        
        conn.commit()
        db.cerrar_conexion()
        
        print("OK - Tablas de cuentas corrientes creadas correctamente")
        
        # Crear cuentas para todos los clientes existentes
        crear_cuentas_para_clientes_existentes()
        
    except Exception as e:
        print(f"ERROR al crear tablas: {str(e)}")

def crear_cuentas_para_clientes_existentes():
    """Crear cuentas corrientes para todos los clientes existentes"""
    try:
        from models.cliente import Cliente
        from models.cuenta_corriente import CuentaCorriente
        
        clientes = Cliente.obtener_todos()
        cuentas_creadas = 0
        
        print(f"Encontrados {len(clientes)} clientes")
        
        for cliente in clientes:
            if CuentaCorriente.crear_cuenta_si_no_existe(cliente.id):
                cuentas_creadas += 1
                print(f"OK - Cuenta creada para: {cliente.nombre} {cliente.apellido}")
        
        print(f"OK - Se crearon {cuentas_creadas} cuentas corrientes")
        
        # Agregar deuda de prueba a algunos clientes
        if len(clientes) > 0:
            agregar_deudas_de_prueba(clientes[:3])  # Primeros 3 clientes
        
    except Exception as e:
        print(f"ERROR al crear cuentas: {str(e)}")

def agregar_deudas_de_prueba(clientes):
    """Agregar deudas de prueba para testing"""
    try:
        from models.cuenta_corriente import CuentaCorriente
        
        deudas_prueba = [50000, 75000, 100000]
        
        for i, cliente in enumerate(clientes):
            if i < len(deudas_prueba):
                cuenta = CuentaCorriente(cliente.id)
                monto = deudas_prueba[i]
                if cuenta.agregar_deuda(monto, f"Venta de prueba {i+1}"):
                    print(f"OK - Deuda de ${monto:,} agregada a {cliente.nombre} {cliente.apellido}")
        
    except Exception as e:
        print(f"ERROR al agregar deudas de prueba: {str(e)}")

def mostrar_resumen():
    """Mostrar resumen de las cuentas creadas"""
    try:
        from controllers.cuenta_controller import CuentaController
        
        controller = CuentaController()
        resumen = controller.obtener_resumen_cuentas()
        
        print("\n" + "="*50)
        print("RESUMEN DE CUENTAS CORRIENTES")
        print("="*50)
        print(f"Total clientes con cuentas: {resumen['total_clientes_deuda']}")
        print(f"Total deuda pendiente: ${resumen['total_deuda_pendiente']:,.0f}")
        print(f"Total deuda acumulada: ${resumen['total_deuda_acumulada']:,.0f}")
        print("="*50)
        
        if resumen['cuentas']:
            print("\nCLIENTES CON DEUDA:")
            for cuenta in resumen['cuentas']:
                nombre = f"{cuenta[1]} {cuenta[2]}"
                saldo = cuenta[4]
                print(f"- {nombre}: ${saldo:,.0f}")
        
    except Exception as e:
        print(f"ERROR al mostrar resumen: {str(e)}")

if __name__ == "__main__":
    print("CONFIGURANDO CUENTAS CORRIENTES...")
    print("-" * 40)
    verificar_y_crear_tablas()
    mostrar_resumen()
    print("-" * 40)
    print("LISTO! Ahora puedes usar las cuentas corrientes.")
    print("Ejecuta: python main.py")