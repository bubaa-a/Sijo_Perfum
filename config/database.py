"""
Configuración y gestión de la base de datos
"""
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="inventario.db"):
        """Inicializar el gestor de base de datos"""
        self.db_name = db_name
        self.connection = None
        self.crear_tablas()
    
    def conectar(self):
        """Crear conexión a la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            return self.connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
    def cerrar_conexion(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def crear_tablas(self):
        """Crear todas las tablas necesarias"""
        conn = self.conectar()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER DEFAULT 5,
                categoria TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                ciudad TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                total REAL NOT NULL,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observaciones TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')
        
        # Tabla de detalles de venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        # Tabla de cuentas corrientes
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
        
        # Tabla de movimientos de cuenta
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
        
        # Tabla de abonos/pagos
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
        self.cerrar_conexion()
        print(" Base de datos y tablas creadas correctamente")
    
    def ejecutar_consulta(self, query, parametros=None):
        """Ejecutar una consulta SQL"""
        conn = self.conectar()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            
            # Si es una consulta de inserción, actualización o eliminación
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
                resultado = cursor.rowcount
            else:
                # Si es una consulta de selección
                resultado = cursor.fetchall()
            
            return resultado
        
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None
        
        finally:
            self.cerrar_conexion()