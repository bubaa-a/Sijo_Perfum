"""
Modelo para gestión de productos
"""
from config.database import DatabaseManager

class Producto:
    def __init__(self, nombre="", descripcion="", precio_compra=0.0, 
                 precio_venta=0.0, stock=0, stock_minimo=5, categoria=""):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.categoria = categoria
        self.activo = True
        self.db = DatabaseManager()
    
    def guardar(self):
        """Guardar producto en la base de datos"""
        query = '''
            INSERT INTO productos 
            (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        parametros = (
            self.nombre, self.descripcion, self.precio_compra,
            self.precio_venta, self.stock, self.stock_minimo, self.categoria
        )
        
        resultado = self.db.ejecutar_consulta(query, parametros)
        return resultado is not None
    
    def actualizar(self):
        """Actualizar producto existente"""
        if not self.id:
            return False
        
        query = '''
            UPDATE productos SET
            nombre=?, descripcion=?, precio_compra=?, precio_venta=?,
            stock=?, stock_minimo=?, categoria=?
            WHERE id=?
        '''
        parametros = (
            self.nombre, self.descripcion, self.precio_compra,
            self.precio_venta, self.stock, self.stock_minimo,
            self.categoria, self.id
        )
        
        resultado = self.db.ejecutar_consulta(query, parametros)
        return resultado is not None
    
    def eliminar(self):
        """Eliminar producto (marcar como inactivo)"""
        if not self.id:
            return False
        
        query = "UPDATE productos SET activo=0 WHERE id=?"
        resultado = self.db.ejecutar_consulta(query, (self.id,))
        return resultado is not None
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los productos activos"""
        db = DatabaseManager()
        query = "SELECT * FROM productos WHERE activo=1 ORDER BY nombre"
        resultados = db.ejecutar_consulta(query)
        
        productos = []
        if resultados:
            for fila in resultados:
                producto = Producto()
                producto.id = fila[0]
                producto.nombre = fila[1]
                producto.descripcion = fila[2]
                producto.precio_compra = fila[3]
                producto.precio_venta = fila[4]
                producto.stock = fila[5]
                producto.stock_minimo = fila[6]
                producto.categoria = fila[7]
                productos.append(producto)
        
        return productos
    
    @staticmethod
    def buscar_por_id(producto_id):
        """Buscar producto por ID"""
        db = DatabaseManager()
        query = "SELECT * FROM productos WHERE id=? AND activo=1"
        resultado = db.ejecutar_consulta(query, (producto_id,))
        
        if resultado and len(resultado) > 0:
            fila = resultado[0]
            producto = Producto()
            producto.id = fila[0]
            producto.nombre = fila[1]
            producto.descripcion = fila[2]
            producto.precio_compra = fila[3]
            producto.precio_venta = fila[4]
            producto.stock = fila[5]
            producto.stock_minimo = fila[6]
            producto.categoria = fila[7]
            return producto
        
        return None
    
    def calcular_ganancia(self):
        """Calcular ganancia por unidad"""
        return self.precio_venta - self.precio_compra
    
    def calcular_margen(self):
        """Calcular margen de ganancia en porcentaje"""
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0
    
    def necesita_restock(self):
        """Verificar si el producto necesita reabastecimiento"""
        return self.stock <= self.stock_minimo
    
    def __str__(self):
        """Representación en string del producto"""
        return f"{self.nombre} - Stock: {self.stock} - Precio: ${self.precio_venta}"