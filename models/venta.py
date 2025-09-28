"""
Modelo para gestión de ventas
"""
from config.database import DatabaseManager
from datetime import datetime

class Venta:
    def __init__(self, cliente_id=None, observaciones=""):
        self.id = None
        self.cliente_id = cliente_id
        self.total = 0.0
        self.fecha_venta = None
        self.observaciones = observaciones
        self.detalles = []  # Lista de DetalleVenta
        self.db = DatabaseManager()
    
    def agregar_detalle(self, producto_id, cantidad, precio_unitario):
        """Agregar un detalle de venta"""
        detalle = DetalleVenta(
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        self.detalles.append(detalle)
        self.calcular_total()
    
    def calcular_total(self):
        """Calcular el total de la venta"""
        self.total = sum(detalle.subtotal for detalle in self.detalles)
    
    def guardar(self):
        """Guardar venta y sus detalles en la base de datos"""
        try:
            # Iniciar transacción
            conn = self.db.conectar()
            cursor = conn.cursor()
            
            # Guardar venta principal
            query_venta = '''
                INSERT INTO ventas (cliente_id, total, observaciones)
                VALUES (?, ?, ?)
            '''
            cursor.execute(query_venta, (self.cliente_id, self.total, self.observaciones))
            self.id = cursor.lastrowid
            
            # Guardar detalles de venta
            for detalle in self.detalles:
                detalle.venta_id = self.id
                query_detalle = '''
                    INSERT INTO detalle_ventas 
                    (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                '''
                cursor.execute(query_detalle, (
                    detalle.venta_id,
                    detalle.producto_id,
                    detalle.cantidad,
                    detalle.precio_unitario,
                    detalle.subtotal
                ))
                
                # Actualizar stock del producto
                query_stock = '''
                    UPDATE productos 
                    SET stock = stock - ? 
                    WHERE id = ?
                '''
                cursor.execute(query_stock, (detalle.cantidad, detalle.producto_id))
            
            conn.commit()
            self.db.cerrar_conexion()
            return True
            
        except Exception as e:
            print(f"Error al guardar venta: {str(e)}")
            if conn:
                conn.rollback()
                self.db.cerrar_conexion()
            return False
    
    @staticmethod
    def obtener_todas():
        """Obtener todas las ventas"""
        db = DatabaseManager()
        query = '''
            SELECT v.id, v.cliente_id, v.total, v.fecha_venta, v.observaciones,
                   c.nombre, c.apellido
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.fecha_venta DESC
        '''
        resultados = db.ejecutar_consulta(query)
        
        ventas = []
        if resultados:
            for fila in resultados:
                venta = Venta()
                venta.id = fila[0]
                venta.cliente_id = fila[1]
                venta.total = fila[2]
                venta.fecha_venta = fila[3]
                venta.observaciones = fila[4]
                venta.cliente_nombre = f"{fila[5] or ''} {fila[6] or ''}".strip()
                ventas.append(venta)
        
        return ventas
    
    @staticmethod
    def obtener_por_id(venta_id):
        """Obtener venta por ID con sus detalles"""
        db = DatabaseManager()
        
        # Obtener venta principal
        query_venta = '''
            SELECT v.id, v.cliente_id, v.total, v.fecha_venta, v.observaciones,
                   c.nombre, c.apellido
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        '''
        resultado = db.ejecutar_consulta(query_venta, (venta_id,))
        
        if not resultado:
            return None
        
        fila = resultado[0]
        venta = Venta()
        venta.id = fila[0]
        venta.cliente_id = fila[1]
        venta.total = fila[2]
        venta.fecha_venta = fila[3]
        venta.observaciones = fila[4]
        venta.cliente_nombre = f"{fila[5] or ''} {fila[6] or ''}".strip()
        
        # Obtener detalles
        query_detalles = '''
            SELECT dv.id, dv.producto_id, dv.cantidad, dv.precio_unitario, dv.subtotal,
                   p.nombre
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        '''
        detalles = db.ejecutar_consulta(query_detalles, (venta_id,))
        
        if detalles:
            for detalle_fila in detalles:
                detalle = DetalleVenta()
                detalle.id = detalle_fila[0]
                detalle.venta_id = venta.id
                detalle.producto_id = detalle_fila[1]
                detalle.cantidad = detalle_fila[2]
                detalle.precio_unitario = detalle_fila[3]
                detalle.subtotal = detalle_fila[4]
                detalle.producto_nombre = detalle_fila[5]
                venta.detalles.append(detalle)
        
        return venta
    
    @staticmethod
    def obtener_ventas_por_fecha(fecha_inicio, fecha_fin):
        """Obtener ventas en un rango de fechas"""
        db = DatabaseManager()
        query = '''
            SELECT v.id, v.cliente_id, v.total, v.fecha_venta, v.observaciones,
                   c.nombre, c.apellido
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE DATE(v.fecha_venta) BETWEEN ? AND ?
            ORDER BY v.fecha_venta DESC
        '''
        resultados = db.ejecutar_consulta(query, (fecha_inicio, fecha_fin))
        
        ventas = []
        if resultados:
            for fila in resultados:
                venta = Venta()
                venta.id = fila[0]
                venta.cliente_id = fila[1]
                venta.total = fila[2]
                venta.fecha_venta = fila[3]
                venta.observaciones = fila[4]
                venta.cliente_nombre = f"{fila[5] or ''} {fila[6] or ''}".strip()
                ventas.append(venta)
        
        return ventas
    
    def calcular_ganancia_total(self):
        """Calcular la ganancia total de la venta"""
        ganancia = 0
        for detalle in self.detalles:
            ganancia += detalle.calcular_ganancia()
        return ganancia

    def eliminar(self):
        """Eliminar venta y sus detalles"""
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            # Primero eliminar los detalles de venta
            cursor.execute("DELETE FROM detalle_ventas WHERE venta_id = ?", (self.id,))

            # Luego eliminar la venta principal
            cursor.execute("DELETE FROM ventas WHERE id = ?", (self.id,))

            # Confirmar los cambios
            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"Error al eliminar venta: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False

class DetalleVenta:
    def __init__(self, venta_id=None, producto_id=None, cantidad=0, precio_unitario=0.0):
        self.id = None
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario
        self.producto_nombre = ""
        self.producto_precio_compra = 0.0
    
    def calcular_subtotal(self):
        """Calcular subtotal del detalle"""
        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal
    
    def calcular_ganancia(self):
        """Calcular ganancia del detalle"""
        if self.producto_precio_compra > 0:
            ganancia_unitaria = self.precio_unitario - self.producto_precio_compra
            return ganancia_unitaria * self.cantidad
        return 0