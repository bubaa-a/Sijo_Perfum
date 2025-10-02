"""
Modelo para gestión de productos
"""
import random
import string
from config.database import DatabaseManager

class Producto:
    def __init__(self, nombre="", descripcion="", precio_compra=0.0,
                 precio_venta=0.0, stock=0, stock_minimo=5, categoria="",
                 marca="", tipo="", proveedor="", sku=""):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.categoria = categoria
        self.marca = marca
        self.tipo = tipo
        self.proveedor = proveedor
        self.sku = sku
        self.activo = True
        self.db = DatabaseManager()

    def generar_sku_unico(self):
        """Generar SKU único basado en marca + 3 números aleatorios"""
        if not self.marca:
            prefijo = "GEN"  # Prefijo genérico si no hay marca
        else:
            # Tomar las primeras 3 letras de la marca y convertir a mayúsculas
            prefijo = self.marca[:3].upper().replace(" ", "")
            # Si la marca es muy corta, rellenar con X
            while len(prefijo) < 3:
                prefijo += "X"

        # Generar SKU único verificando que no exista
        max_intentos = 100
        for _ in range(max_intentos):
            # Generar 3 números aleatorios
            numeros = ''.join([str(random.randint(0, 9)) for _ in range(3)])
            sku_candidato = f"{prefijo}{numeros}"

            # Verificar si el SKU ya existe
            if not self.sku_existe(sku_candidato):
                return sku_candidato

        # Si después de 100 intentos no encontramos uno único, agregar letras adicionales
        letras = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        return f"{prefijo}{numeros}{letras}"

    def sku_existe(self, sku):
        """Verificar si un SKU ya existe en la base de datos"""
        query = "SELECT COUNT(*) FROM productos WHERE sku = ? AND activo = 1"
        resultado = self.db.ejecutar_consulta(query, (sku,))
        return resultado and resultado[0][0] > 0

    def guardar(self):
        """Guardar producto en la base de datos"""
        # Generar SKU automáticamente si no se ha asignado uno
        if not self.sku:
            self.sku = self.generar_sku_unico()

        query = '''
            INSERT INTO productos
            (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, categoria, marca, tipo, proveedor, sku)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        parametros = (
            self.nombre, self.descripcion, self.precio_compra,
            self.precio_venta, self.stock, self.stock_minimo, self.categoria,
            self.marca, self.tipo, self.proveedor, self.sku
        )

        resultado = self.db.ejecutar_consulta(query, parametros)
        if resultado is not None:
            print(f"DEBUG: Producto guardado con SKU: {self.sku}")
        return resultado is not None
    
    def actualizar(self):
        """Actualizar producto existente"""
        if not self.id:
            return False

        # Si no tiene SKU, generar uno nuevo
        if not self.sku:
            self.sku = self.generar_sku_unico()

        query = '''
            UPDATE productos SET
            nombre=?, descripcion=?, precio_compra=?, precio_venta=?,
            stock=?, stock_minimo=?, categoria=?, marca=?, tipo=?, proveedor=?, sku=?
            WHERE id=?
        '''
        parametros = (
            self.nombre, self.descripcion, self.precio_compra,
            self.precio_venta, self.stock, self.stock_minimo,
            self.categoria, self.marca, self.tipo, self.proveedor, self.sku, self.id
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
        """Obtener todos los productos activos ordenados alfabéticamente"""
        db = DatabaseManager()
        query = "SELECT * FROM productos WHERE activo=1 ORDER BY nombre ASC"
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
                # Nuevos campos (pueden ser None en productos existentes)
                producto.marca = str(fila[10]) if len(fila) > 10 and fila[10] is not None else ""
                producto.tipo = str(fila[11]) if len(fila) > 11 and fila[11] is not None else ""
                producto.proveedor = str(fila[12]) if len(fila) > 12 and fila[12] is not None else ""
                producto.sku = str(fila[13]) if len(fila) > 13 and fila[13] is not None else ""
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
            # Nuevos campos (pueden ser None en productos existentes)
            producto.marca = str(fila[10]) if len(fila) > 10 and fila[10] is not None else ""
            producto.tipo = str(fila[11]) if len(fila) > 11 and fila[11] is not None else ""
            producto.proveedor = str(fila[12]) if len(fila) > 12 and fila[12] is not None else ""
            producto.sku = str(fila[13]) if len(fila) > 13 and fila[13] is not None else ""
            return producto

        return None

    @staticmethod
    def obtener_para_combobox():
        """Obtener productos para combobox ordenados alfabéticamente"""
        productos = Producto.obtener_todos()
        # Formatear para combobox: "SKU - Nombre (Stock: X)"
        productos_combobox = []
        for producto in productos:
            sku_display = producto.sku if producto.sku else "SIN-SKU"
            texto = f"{sku_display} - {producto.nombre} (Stock: {producto.stock})"
            productos_combobox.append((producto.id, texto))

        # Ordenar por el texto del combobox (que ya incluye SKU y nombre)
        productos_combobox.sort(key=lambda x: x[1])
        return productos_combobox
    
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