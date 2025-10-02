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

    def generar_numero_recibo(self):
        """Generar número de recibo automático basado en la fecha y cantidad de ventas"""
        try:
            from config.database import obtener_conexion
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Obtener el último ID de venta
            cursor.execute("SELECT MAX(id) FROM ventas")
            resultado = cursor.fetchone()
            ultimo_id = resultado[0] if resultado[0] else 0

            conn.close()

            # Generar número de recibo: formato REC-YYYYMMDD-XXXX
            fecha_actual = datetime.now().strftime("%Y%m%d")
            numero_secuencial = str(ultimo_id + 1).zfill(4)
            numero_recibo = f"REC-{fecha_actual}-{numero_secuencial}"

            return numero_recibo

        except Exception as e:
            print(f"Error al generar número de recibo: {str(e)}")
            # Generar un número básico en caso de error
            return f"REC-{datetime.now().strftime('%Y%m%d')}-0001"
    
    def crear_venta(self, cliente_id, detalles_venta, observaciones="", numero_recibo=""):
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
            venta = Venta(cliente_id=cliente_id, observaciones=observaciones, numero_recibo=numero_recibo)
            
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
            from config.database import DatabaseManager

            db = DatabaseManager()

            # Obtener fecha de hoy
            hoy = datetime.now().strftime('%Y-%m-%d')
            print(f"DEBUG: Consultando ventas para la fecha: {hoy}")

            # Consulta directa para ventas de hoy
            query_hoy = """
                SELECT COUNT(*) as cantidad, COALESCE(SUM(total), 0) as total
                FROM ventas
                WHERE DATE(fecha_venta) = ?
            """
            resultado_hoy = db.ejecutar_consulta(query_hoy, (hoy,))
            print(f"DEBUG: Resultado ventas hoy: {resultado_hoy}")

            ventas_hoy_count = resultado_hoy[0][0] if resultado_hoy and resultado_hoy[0] else 0
            ingresos_hoy = resultado_hoy[0][1] if resultado_hoy and resultado_hoy[0] else 0

            print(f"DEBUG: Ventas hoy count: {ventas_hoy_count}, Ingresos hoy: {ingresos_hoy}")

            # Estadísticas generales
            query_total = """
                SELECT COUNT(*) as cantidad, COALESCE(SUM(total), 0) as total
                FROM ventas
            """
            resultado_total = db.ejecutar_consulta(query_total)
            total_ventas = resultado_total[0][0] if resultado_total and resultado_total[0] else 0
            ingresos_totales = resultado_total[0][1] if resultado_total and resultado_total[0] else 0

            # Ventas del mes
            primer_dia_mes = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            query_mes = """
                SELECT COALESCE(SUM(total), 0)
                FROM ventas
                WHERE DATE(fecha_venta) BETWEEN ? AND ?
            """
            resultado_mes = db.ejecutar_consulta(query_mes, (primer_dia_mes, hoy))
            ingresos_mes = resultado_mes[0][0] if resultado_mes and resultado_mes[0] else 0

            return {
                'total_ventas': total_ventas,
                'ingresos_totales': ingresos_totales,
                'ventas_hoy': ventas_hoy_count,
                'ingresos_hoy': ingresos_hoy,
                'ingresos_mes': ingresos_mes,
                'ganancia_total': 0
            }

        except Exception as e:
            print(f"ERROR al obtener estadísticas: {str(e)}")
            import traceback
            traceback.print_exc()
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
        """Eliminar una venta por ID y revertir todos los movimientos"""
        try:
            # Buscar la venta completa con detalles
            venta = Venta.obtener_por_id(venta_id)
            if not venta:
                messagebox.showerror("Error", "Venta no encontrada")
                return False

            # Confirmar eliminación
            from tkinter import messagebox
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la venta #{venta_id}?\n\n"
                f"Cliente: {getattr(venta, 'cliente_nombre', 'N/A')}\n"
                f"Total: ${venta.total:,.0f}\n\n"
                "ATENCIÓN: Esto revertirá:\n"
                "• Los movimientos en cuenta corriente\n"
                "• El stock de productos vendidos\n\n"
                "Esta acción NO se puede deshacer."
            )

            if not respuesta:
                return False

            # Eliminar la venta (con reversión automática)
            if venta.eliminar_completa():
                # Limpiar cuenta corriente si quedó vacía
                if venta.cliente_id:
                    from controllers.cuenta_controller import CuentaController
                    cuenta_controller = CuentaController()
                    cuenta_controller.limpiar_cuenta_vacia(venta.cliente_id)

                messagebox.showinfo("Éxito", "Venta eliminada correctamente\n\nSe han revertido todos los movimientos asociados.")
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