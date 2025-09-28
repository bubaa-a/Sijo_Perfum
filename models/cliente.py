"""
Modelo para gestión de clientes
"""
from config.database import DatabaseManager

class Cliente:
    def __init__(self, nombre="", apellido="", telefono="", email="", 
                 direccion="", ciudad=""):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.ciudad = ciudad
        self.activo = True
        self.db = DatabaseManager()
    
    def guardar(self):
        """Guardar cliente en la base de datos con validación"""
        try:
            query = '''
                INSERT INTO clientes 
                (nombre, apellido, telefono, email, direccion, ciudad)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            parametros = (
                self.nombre, self.apellido, self.telefono,
                self.email, self.direccion, self.ciudad
            )
        
            print(f"MODEL DEBUG: Ejecutando query con parámetros: {parametros}")
        
            resultado = self.db.ejecutar_consulta(query, parametros)
        
            if resultado is not None:
                print("MODEL DEBUG: Cliente guardado exitosamente")
                return True
            else:
                print("MODEL ERROR: No se pudo guardar el cliente")
                return False
            
        except Exception as e:
            print(f"MODEL ERROR: {str(e)}")
            return False
    
    def actualizar(self):
        """Actualizar cliente existente"""
        if not self.id:
            return False
        
        query = '''
            UPDATE clientes SET
            nombre=?, apellido=?, telefono=?, email=?,
            direccion=?, ciudad=?
            WHERE id=?
        '''
        parametros = (
            self.nombre, self.apellido, self.telefono,
            self.email, self.direccion, self.ciudad, self.id
        )
        
        resultado = self.db.ejecutar_consulta(query, parametros)
        return resultado is not None
    
    def eliminar(self):
        """Eliminar cliente y limpiar datos relacionados"""
        try:
            # Eliminar registros relacionados primero
        
            # 1. Actualizar ventas para quitar referencia al cliente
            query_ventas = "UPDATE ventas SET cliente_id = NULL WHERE cliente_id = ?"
            self.db.ejecutar_consulta(query_ventas, (self.id,))
        
            # 2. Eliminar cuenta corriente
            query_cuenta = "DELETE FROM cuentas_corrientes WHERE cliente_id = ?"
            self.db.ejecutar_consulta(query_cuenta, (self.id,))
        
            # 3. Eliminar movimientos de cuenta
            query_movimientos = "DELETE FROM movimientos_cuenta WHERE cliente_id = ?"
            self.db.ejecutar_consulta(query_movimientos, (self.id,))
        
            # 4. Eliminar abonos
            query_abonos = "DELETE FROM abonos WHERE cliente_id = ?"
            self.db.ejecutar_consulta(query_abonos, (self.id,))
        
            # 5. Finalmente eliminar el cliente
            query_cliente = "DELETE FROM clientes WHERE id = ?"
            resultado = self.db.ejecutar_consulta(query_cliente, (self.id,))
        
            return resultado is not None
        
        except Exception as e:
            print(f"Error al eliminar cliente: {str(e)}")
            return False
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los clientes activos"""
        db = DatabaseManager()
        query = "SELECT * FROM clientes WHERE activo=1 ORDER BY nombre, apellido"
        resultados = db.ejecutar_consulta(query)
        
        clientes = []
        if resultados:
            for fila in resultados:
                cliente = Cliente()
                cliente.id = fila[0]
                cliente.nombre = fila[1]
                cliente.apellido = fila[2]
                cliente.telefono = fila[3]
                cliente.email = fila[4]
                cliente.direccion = fila[5]
                cliente.ciudad = fila[6]
                clientes.append(cliente)
        
        return clientes
    
    @staticmethod
    def buscar_por_id(cliente_id):
        """Buscar cliente por ID"""
        db = DatabaseManager()
        query = "SELECT * FROM clientes WHERE id=? AND activo=1"
        resultado = db.ejecutar_consulta(query, (cliente_id,))
        
        if resultado and len(resultado) > 0:
            fila = resultado[0]
            cliente = Cliente()
            cliente.id = fila[0]
            cliente.nombre = fila[1]
            cliente.apellido = fila[2]
            cliente.telefono = fila[3]
            cliente.email = fila[4]
            cliente.direccion = fila[5]
            cliente.ciudad = fila[6]
            return cliente
        
        return None
    
    @staticmethod
    def buscar_por_nombre(termino):
        """Buscar clientes por nombre o apellido"""
        db = DatabaseManager()
        query = '''
            SELECT * FROM clientes 
            WHERE (nombre LIKE ? OR apellido LIKE ?) AND activo=1
            ORDER BY nombre, apellido
        '''
        termino_busqueda = f"%{termino}%"
        resultados = db.ejecutar_consulta(query, (termino_busqueda, termino_busqueda))
        
        clientes = []
        if resultados:
            for fila in resultados:
                cliente = Cliente()
                cliente.id = fila[0]
                cliente.nombre = fila[1]
                cliente.apellido = fila[2]
                cliente.telefono = fila[3]
                cliente.email = fila[4]
                cliente.direccion = fila[5]
                cliente.ciudad = fila[6]
                clientes.append(cliente)
        
        return clientes
    
    def nombre_completo(self):
        """Obtener nombre completo del cliente"""
        return f"{self.nombre} {self.apellido}".strip()
    
    def obtener_historial_compras(self):
        """Obtener historial de compras del cliente"""
        if not self.id:
            return []
        
        query = '''
            SELECT v.id, v.total, v.fecha_venta, v.observaciones
            FROM ventas v
            WHERE v.cliente_id = ?
            ORDER BY v.fecha_venta DESC
        '''
        
        resultados = self.db.ejecutar_consulta(query, (self.id,))
        return resultados or []
    
    def calcular_total_compras(self):
        """Calcular total de compras del cliente"""
        if not self.id:
            return 0
        
        query = '''
            SELECT SUM(total) FROM ventas 
            WHERE cliente_id = ?
        '''
        
        resultado = self.db.ejecutar_consulta(query, (self.id,))
        if resultado and resultado[0][0]:
            return resultado[0][0]
        return 0
    
    def __str__(self):
        """Representación en string del cliente"""
        return f"{self.nombre_completo()} - {self.telefono}"