"""
Controlador para la lógica de negocio de ventas
"""
from models.venta import Venta, DetalleVenta
from models.producto import Producto
from models.cliente import Cliente
from tkinter import messagebox
from datetime import datetime, timedelta

class VentaController:
    def __init__(self):
        """Inicializar el controlador de ventas"""
        pass
    
    def crear_venta(self, cliente_id, detalles_venta, observaciones=""):
        """
        Crear una nueva venta
        detalles_venta: lista de diccionarios con producto_id, cantidad, precio_unitario
        """
        try:
            # Validar datos
            errores = self.validar_venta(cliente_id, detalles_venta)
            if errores:
                messagebox.showerror("Error de validación", "\n".join(errores))
                return False
            
            # Crear la venta
            venta = Venta(cliente_id=cliente_id, observaciones=observaciones)
            
            # Agregar detalles
            for detalle in detalles_venta:
                venta.agregar_detalle(
                    producto_id=detalle['producto_id'],
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario']
                )
            
            # Guardar en la base de datos
            if venta.guardar():
                if cliente_id:
                    from controllers.cuenta_controller import CuentaController
                    cuenta_controller = CuentaController()
                    cuenta_controller.agregar_venta_a_cuenta(cliente_id, venta.total, "Venta", venta.id)
                messagebox.showinfo("Éxito", f"Venta registrada correctamente\nTotal: ${venta.total:,.0f}")
                return True
            else:
                messagebox.showerror("Error", "No se pudo guardar la venta")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear venta: {str(e)}")
            return False
    
    def obtener_todas_ventas(self):
        """Obtener lista de todas las ventas"""
        try:
            return Venta.obtener_todas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ventas: {str(e)}")
            return []
    
    def obtener_venta_por_id(self, venta_id):
        """Obtener venta por ID"""
        try:
            return Venta.obtener_por_id(venta_id)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener venta: {str(e)}")
            return None
    
    def validar_venta(self, cliente_id, detalles_venta):
        """Validar los datos de la venta"""
        errores = []
        
        # Validar que hay detalles
        if not detalles_venta:
            errores.append("Debe agregar al menos un producto a la venta")
        
        # Validar cada detalle
        for i, detalle in enumerate(detalles_venta):
            producto_id = detalle.get('producto_id')
            cantidad = detalle.get('cantidad', 0)
            precio_unitario = detalle.get('precio_unitario', 0)
            
            # Validar producto existe
            producto = Producto.buscar_por_id(producto_id)
            if not producto:
                errores.append(f"Producto en línea {i+1} no encontrado")
                continue
            
            # Validar cantidad
            try:
                cantidad = int(cantidad)
                if cantidad <= 0:
                    errores.append(f"Cantidad en línea {i+1} debe ser mayor a 0")
                elif cantidad > producto.stock:
                    errores.append(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
            except ValueError:
                errores.append(f"Cantidad en línea {i+1} debe ser un número entero")
            
            # Validar precio
            try:
                precio_unitario = float(precio_unitario)
                if precio_unitario <= 0:
                    errores.append(f"Precio en línea {i+1} debe ser mayor a 0")
            except ValueError:
                errores.append(f"Precio en línea {i+1} debe ser un número válido")
        
        return errores
    
    def obtener_productos_disponibles(self):
        """Obtener productos con stock disponible"""
        try:
            productos = Producto.obtener_todos()
            return [p for p in productos if p.stock > 0]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {str(e)}")
            return []
    
    def obtener_clientes_activos(self):
        """Obtener clientes activos"""
        try:
            return Cliente.obtener_todos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener clientes: {str(e)}")
            return []
    
    def obtener_estadisticas_ventas(self):
        """Obtener estadísticas generales de ventas"""
        try:
            ventas = self.obtener_todas_ventas()
            
            # Estadísticas básicas
            total_ventas = len(ventas)
            ingresos_totales = sum(v.total for v in ventas)
            
            # Ventas de hoy
            hoy = datetime.now().strftime('%Y-%m-%d')
            ventas_hoy = Venta.obtener_ventas_por_fecha(hoy, hoy)
            ventas_hoy_count = len(ventas_hoy)
            ingresos_hoy = sum(v.total for v in ventas_hoy)
            
            # Ventas del mes
            primer_dia_mes = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            ultimo_dia_mes = datetime.now().strftime('%Y-%m-%d')
            ventas_mes = Venta.obtener_ventas_por_fecha(primer_dia_mes, ultimo_dia_mes)
            ingresos_mes = sum(v.total for v in ventas_mes)
            
            # Calcular ganancia (necesitamos los detalles)
            ganancia_total = 0
            for venta in ventas:
                venta_completa = self.obtener_venta_por_id(venta.id)
                if venta_completa:
                    ganancia_total += venta_completa.calcular_ganancia_total()
            
            return {
                'total_ventas': total_ventas,
                'ingresos_totales': ingresos_totales,
                'ventas_hoy': ventas_hoy_count,
                'ingresos_hoy': ingresos_hoy,
                'ingresos_mes': ingresos_mes,
                'ganancia_total': ganancia_total
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {str(e)}")
            return {
                'total_ventas': 0,
                'ingresos_totales': 0,
                'ventas_hoy': 0,
                'ingresos_hoy': 0,
                'ingresos_mes': 0,
                'ganancia_total': 0
            }
    
    def buscar_ventas(self, termino):
        """Buscar ventas por cliente o ID"""
        try:
            ventas = self.obtener_todas_ventas()
            termino = termino.lower()
            
            ventas_filtradas = [
                v for v in ventas 
                if (termino in str(v.id) or 
                    termino in v.cliente_nombre.lower() if hasattr(v, 'cliente_nombre') else False)
            ]
            
            return ventas_filtradas
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar ventas: {str(e)}")
            return []

    def eliminar_venta(self, venta_id):
        """Eliminar una venta por ID"""
        try:
            # Buscar la venta
            venta = Venta.obtener_por_id(venta_id)
            if not venta:
                messagebox.showerror("Error", "Venta no encontrada")
                return False

            # Eliminar la venta
            if venta.eliminar():
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar la venta")
                return False

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar venta: {str(e)}")
            return False

    def obtener_ventas_por_periodo(self, dias):
        """Obtener ventas de los últimos N días"""
        try:
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
            fecha_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')

            return Venta.obtener_ventas_por_fecha(fecha_inicio, fecha_fin)

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ventas por período: {str(e)}")
            return []