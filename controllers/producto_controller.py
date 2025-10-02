"""
Controlador para la lógica de negocio de productos
"""
from models.producto import Producto
from tkinter import messagebox

class ProductoController:
    def __init__(self):
        """Inicializar el controlador de productos"""
        pass
    
    def crear_producto(self, datos):
        """
        Crear un nuevo producto
        datos: diccionario con los datos del producto
        """
        try:
            # Validar datos
            errores = self.validar_datos_producto(datos)
            if errores:
                messagebox.showerror("Error de validación", "\n".join(errores))
                return False
            
            # Crear el producto
            producto = Producto(
                nombre=datos['nombre'],
                descripcion=datos['descripcion'],
                precio_compra=float(datos['precio_compra']),
                precio_venta=float(datos['precio_venta']),
                stock=int(datos['stock']),
                stock_minimo=int(datos['stock_minimo']),
                categoria=datos['categoria'],
                marca=datos.get('marca', ''),
                tipo=datos.get('tipo', ''),
                proveedor=datos.get('proveedor', '')
            )
            
            # Guardar en la base de datos
            if producto.guardar():
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' creado correctamente")
                return True
            else:
                messagebox.showerror("Error", "No se pudo guardar el producto")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear producto: {str(e)}")
            return False
    
    def obtener_todos_productos(self):
        """Obtener lista de todos los productos"""
        try:
            return Producto.obtener_todos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {str(e)}")
            return []

    def obtener_producto_por_id(self, producto_id):
        """Obtener un producto por su ID"""
        try:
            return Producto.buscar_por_id(producto_id)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener producto: {str(e)}")
            return None

    def actualizar_producto(self, producto_id, datos):
        """Actualizar un producto existente"""
        try:
            # Buscar el producto
            producto = Producto.buscar_por_id(producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return False
            
            # Validar datos
            errores = self.validar_datos_producto(datos)
            if errores:
                messagebox.showerror("Error de validación", "\n".join(errores))
                return False
            
            # Actualizar datos
            producto.nombre = datos['nombre']
            producto.descripcion = datos['descripcion']
            producto.precio_compra = float(datos['precio_compra'])
            producto.precio_venta = float(datos['precio_venta'])
            producto.stock = int(datos['stock'])
            producto.stock_minimo = int(datos['stock_minimo'])
            producto.categoria = datos['categoria']
            producto.marca = datos.get('marca', '')
            producto.tipo = datos.get('tipo', '')
            producto.proveedor = datos.get('proveedor', '')
            
            # Guardar cambios
            if producto.actualizar():
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' actualizado correctamente")
                return True
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {str(e)}")
            return False
    
    def eliminar_producto(self, producto_id):
        """Eliminar un producto"""
        try:
            producto = Producto.buscar_por_id(producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return False
            
            # Confirmar eliminación
            respuesta = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro de eliminar el producto '{producto.nombre}'?"
            )
            
            if respuesta:
                if producto.eliminar():
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    return True
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el producto")
                    return False
            
            return False
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
            return False
    
    def buscar_productos(self, termino):
        """Buscar productos por nombre o categoría"""
        try:
            productos = self.obtener_todos_productos()
            termino = termino.lower()
            
            productos_filtrados = [
                p for p in productos 
                if termino in p.nombre.lower() or termino in p.categoria.lower()
            ]
            
            return productos_filtrados
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar productos: {str(e)}")
            return []
    
    def obtener_productos_bajo_stock(self):
        """Obtener productos que necesitan reabastecimiento"""
        try:
            productos = self.obtener_todos_productos()
            return [p for p in productos if p.necesita_restock()]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos bajo stock: {str(e)}")
            return []
    
    def validar_datos_producto(self, datos):
        """Validar los datos del producto"""
        errores = []
        
        # Validar nombre
        if not datos.get('nombre', '').strip():
            errores.append("El nombre del producto es obligatorio")
        
        # Validar precios
        try:
            precio_compra = float(datos.get('precio_compra', 0))
            if precio_compra < 0:
                errores.append("El precio de compra debe ser mayor o igual a 0")
        except ValueError:
            errores.append("El precio de compra debe ser un número válido")
        
        try:
            precio_venta = float(datos.get('precio_venta', 0))
            if precio_venta < 0:
                errores.append("El precio de venta debe ser mayor o igual a 0")
        except ValueError:
            errores.append("El precio de venta debe ser un número válido")
        
        # Validar que precio de venta sea mayor que precio de compra
        try:
            if float(datos.get('precio_venta', 0)) <= float(datos.get('precio_compra', 0)):
                errores.append("El precio de venta debe ser mayor que el precio de compra")
        except ValueError:
            pass  # Ya se validó arriba
        
        # Validar stock
        try:
            stock = int(datos.get('stock', 0))
            if stock < 0:
                errores.append("El stock debe ser mayor o igual a 0")
        except ValueError:
            errores.append("El stock debe ser un número entero válido")
        
        # Validar stock mínimo
        try:
            stock_minimo = int(datos.get('stock_minimo', 0))
            if stock_minimo < 0:
                errores.append("El stock mínimo debe ser mayor o igual a 0")
        except ValueError:
            errores.append("El stock mínimo debe ser un número entero válido")
        
        return errores
    
    def obtener_estadisticas_productos(self):
        """Obtener estadísticas generales de productos"""
        try:
            productos = self.obtener_todos_productos()
            
            total_productos = len(productos)
            valor_inventario = sum(p.precio_compra * p.stock for p in productos)
            productos_bajo_stock = len(self.obtener_productos_bajo_stock())
            ganancia_potencial = sum(p.calcular_ganancia() * p.stock for p in productos)
            
            return {
                'total_productos': total_productos,
                'valor_inventario': valor_inventario,
                'productos_bajo_stock': productos_bajo_stock,
                'ganancia_potencial': ganancia_potencial
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas: {str(e)}")
            return {
                'total_productos': 0,
                'valor_inventario': 0,
                'productos_bajo_stock': 0,
                'ganancia_potencial': 0
            }

    def generar_skus_faltantes(self):
        """Generar SKUs para productos existentes que no los tengan"""
        try:
            from models.producto import Producto
            productos = Producto.obtener_todos()
            productos_actualizados = 0

            for producto in productos:
                if not producto.sku:  # Si no tiene SKU
                    # Generar SKU para el producto
                    producto.sku = producto.generar_sku_unico()

                    # Actualizar en la base de datos
                    if producto.actualizar():
                        productos_actualizados += 1
                        print(f"DEBUG: SKU generado para '{producto.nombre}': {producto.sku}")

            if productos_actualizados > 0:
                messagebox.showinfo("Éxito", f"Se generaron SKUs para {productos_actualizados} productos")
            else:
                messagebox.showinfo("Información", "Todos los productos ya tienen SKU asignado")

            return productos_actualizados

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar SKUs: {str(e)}")
            return 0