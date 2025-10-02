"""
Controlador para la lógica de reportes y análisis
"""
from config.database import DatabaseManager
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

class ReporteController:
    def __init__(self):
        """Inicializar el controlador de reportes"""
        self.db = DatabaseManager()
    
    def obtener_resumen_general(self):
        """Obtener resumen general del negocio"""
        try:
            # Productos
            query_productos = "SELECT COUNT(*) FROM productos WHERE activo=1"
            total_productos = self.db.ejecutar_consulta(query_productos)[0][0]

            query_stock_bajo = """
                SELECT COUNT(*) FROM productos
                WHERE activo=1 AND stock <= stock_minimo
            """
            productos_stock_bajo = self.db.ejecutar_consulta(query_stock_bajo)[0][0]

            query_valor_inventario = """
                SELECT SUM(precio_compra * stock) FROM productos WHERE activo=1
            """
            resultado = self.db.ejecutar_consulta(query_valor_inventario)
            valor_inventario = resultado[0][0] if resultado[0][0] else 0

            # Clientes
            query_clientes = "SELECT COUNT(*) FROM clientes WHERE activo=1"
            total_clientes = self.db.ejecutar_consulta(query_clientes)[0][0]

            # Clientes con compras
            query_clientes_compras = """
                SELECT COUNT(DISTINCT cliente_id) FROM ventas
                WHERE cliente_id IS NOT NULL
            """
            resultado_clientes_compras = self.db.ejecutar_consulta(query_clientes_compras)
            clientes_con_compras = resultado_clientes_compras[0][0] if resultado_clientes_compras[0][0] else 0

            # Ventas del mes actual
            query_ventas_mes = """
                SELECT COUNT(*), SUM(total) FROM ventas
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now')
            """
            resultado_ventas_mes = self.db.ejecutar_consulta(query_ventas_mes)[0]
            cantidad_ventas_mes = resultado_ventas_mes[0] if resultado_ventas_mes[0] else 0
            ventas_mes = resultado_ventas_mes[1] if resultado_ventas_mes[1] else 0

            # Deuda pendiente
            query_deuda = """
                SELECT SUM(saldo_pendiente), COUNT(*) FROM cuentas_corrientes
                WHERE activa = 1 AND saldo_pendiente > 0
            """
            resultado_deuda = self.db.ejecutar_consulta(query_deuda)[0]
            deuda_pendiente = resultado_deuda[0] if resultado_deuda[0] else 0
            clientes_con_deuda = resultado_deuda[1] if resultado_deuda[1] else 0

            return {
                'total_productos': total_productos,
                'valor_inventario': valor_inventario,
                'total_clientes': total_clientes,
                'clientes_con_compras': clientes_con_compras,
                'ventas_mes': ventas_mes,
                'cantidad_ventas_mes': cantidad_ventas_mes,
                'deuda_pendiente': deuda_pendiente,
                'clientes_con_deuda': clientes_con_deuda
            }

        except Exception as e:
            print(f"Error al obtener resumen general: {str(e)}")
            return {}
    
    def obtener_ventas_por_periodo(self, dias=30):
        """Obtener ventas de los últimos N días"""
        try:
            fecha_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
            
            query = """
                SELECT DATE(fecha_venta) as fecha, COUNT(*) as cantidad, SUM(total) as total
                FROM ventas
                WHERE DATE(fecha_venta) BETWEEN ? AND ?
                GROUP BY DATE(fecha_venta)
                ORDER BY fecha_venta
            """
            
            resultados = self.db.ejecutar_consulta(query, (fecha_inicio, fecha_fin))
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener ventas por período: {str(e)}")
            return []
    
    def obtener_productos_mas_vendidos(self, limite=10):
        """Obtener los productos más vendidos"""
        try:
            query = """
                SELECT p.nombre, SUM(dv.cantidad) as total_vendido, 
                       SUM(dv.subtotal) as ingresos,
                       SUM(dv.subtotal - (p.precio_compra * dv.cantidad)) as ganancia
                FROM detalle_ventas dv
                JOIN productos p ON dv.producto_id = p.id
                GROUP BY dv.producto_id, p.nombre
                ORDER BY total_vendido DESC
                LIMIT ?
            """
            
            resultados = self.db.ejecutar_consulta(query, (limite,))
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener productos más vendidos: {str(e)}")
            return []
    
    def obtener_mejores_clientes(self, limite=10):
        """Obtener los mejores clientes por compras"""
        try:
            query = """
                SELECT c.nombre, c.apellido, COUNT(v.id) as total_compras, 
                       SUM(v.total) as total_gastado
                FROM clientes c
                JOIN ventas v ON c.id = v.cliente_id
                WHERE c.activo = 1
                GROUP BY c.id, c.nombre, c.apellido
                ORDER BY total_gastado DESC
                LIMIT ?
            """
            
            resultados = self.db.ejecutar_consulta(query, (limite,))
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener mejores clientes: {str(e)}")
            return []
    
    def obtener_inventario_critico(self):
        """Obtener productos con stock crítico"""
        try:
            query = """
                SELECT nombre, stock, stock_minimo, 
                       (precio_venta * stock) as valor_stock,
                       categoria
                FROM productos
                WHERE activo = 1 AND stock <= stock_minimo
                ORDER BY stock ASC
            """
            
            resultados = self.db.ejecutar_consulta(query)
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener inventario crítico: {str(e)}")
            return []
    
    def obtener_analisis_categorias(self):
        """Obtener análisis por categorías de productos"""
        try:
            query = """
                SELECT p.categoria, 
                       COUNT(p.id) as total_productos,
                       SUM(p.stock) as stock_total,
                       SUM(p.precio_compra * p.stock) as valor_inventario,
                       COALESCE(SUM(dv.cantidad), 0) as total_vendido,
                       COALESCE(SUM(dv.subtotal), 0) as ingresos_categoria
                FROM productos p
                LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
                WHERE p.activo = 1
                GROUP BY p.categoria
                ORDER BY ingresos_categoria DESC
            """
            
            resultados = self.db.ejecutar_consulta(query)
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener análisis por categorías: {str(e)}")
            return []
    
    def obtener_estadisticas_mensuales(self, meses=12):
        """Obtener estadísticas de los últimos meses"""
        try:
            query = """
                SELECT strftime('%Y-%m', fecha_venta) as mes,
                       COUNT(*) as total_ventas,
                       SUM(total) as ingresos,
                       AVG(total) as ticket_promedio
                FROM ventas
                WHERE fecha_venta >= date('now', '-{} months')
                GROUP BY strftime('%Y-%m', fecha_venta)
                ORDER BY mes
            """.format(meses)
            
            resultados = self.db.ejecutar_consulta(query)
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener estadísticas mensuales: {str(e)}")
            return []
    
    def obtener_rentabilidad_productos(self):
        """Obtener análisis de rentabilidad por producto"""
        try:
            query = """
                SELECT p.nombre, p.precio_compra, p.precio_venta,
                       (p.precio_venta - p.precio_compra) as ganancia_unitaria,
                       ((p.precio_venta - p.precio_compra) / p.precio_compra * 100) as margen_porcentaje,
                       p.stock,
                       COALESCE(SUM(dv.cantidad), 0) as total_vendido,
                       COALESCE(SUM(dv.subtotal - (p.precio_compra * dv.cantidad)), 0) as ganancia_total
                FROM productos p
                LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
                WHERE p.activo = 1
                GROUP BY p.id, p.nombre, p.precio_compra, p.precio_venta, p.stock
                ORDER BY ganancia_total DESC
            """
            
            resultados = self.db.ejecutar_consulta(query)
            return resultados or []
            
        except Exception as e:
            print(f"Error al obtener rentabilidad de productos: {str(e)}")
            return []
    
    def exportar_reporte_csv(self, datos, nombre_archivo, headers):
        """Exportar datos a CSV"""
        try:
            import csv
            from tkinter import filedialog
            
            # Solicitar ubicación de guardado
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialvalue=nombre_archivo
            )
            
            if archivo:
                with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Escribir headers
                    writer.writerow(headers)
                    
                    # Escribir datos
                    for fila in datos:
                        writer.writerow(fila)
                
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{archivo}")
                return True
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
        
        return False
    
    def obtener_ventas_por_mes(self, meses=12):
        """Obtener ventas agrupadas por mes"""
        try:
            query = """
                SELECT strftime('%Y-%m', fecha_venta) as mes,
                       SUM(total) as total_ventas,
                       COUNT(*) as cantidad_ventas
                FROM ventas
                WHERE fecha_venta >= date('now', '-{} months')
                GROUP BY strftime('%Y-%m', fecha_venta)
                ORDER BY mes DESC
            """.format(meses)

            resultados = self.db.ejecutar_consulta(query)
            return resultados or []

        except Exception as e:
            print(f"Error al obtener ventas por mes: {str(e)}")
            return []

    def obtener_resumen_productos(self):
        """Obtener resumen de productos"""
        try:
            # Total productos
            query_total = "SELECT COUNT(*) FROM productos WHERE activo=1"
            total_productos = self.db.ejecutar_consulta(query_total)[0][0]

            # Valor total inventario
            query_valor = "SELECT SUM(precio_compra * stock) FROM productos WHERE activo=1"
            resultado_valor = self.db.ejecutar_consulta(query_valor)
            valor_total = resultado_valor[0][0] if resultado_valor[0][0] else 0

            # Productos bajo stock
            query_bajo_stock = """
                SELECT COUNT(*) FROM productos
                WHERE activo=1 AND stock <= stock_minimo
            """
            productos_bajo_stock = self.db.ejecutar_consulta(query_bajo_stock)[0][0]

            return {
                'total_productos': total_productos,
                'valor_total': valor_total,
                'productos_bajo_stock': productos_bajo_stock
            }

        except Exception as e:
            print(f"Error al obtener resumen de productos: {str(e)}")
            return {}

    def obtener_productos_bajo_stock(self):
        """Obtener productos con stock bajo"""
        try:
            query = """
                SELECT nombre, stock, stock_minimo, categoria
                FROM productos
                WHERE activo = 1 AND stock <= stock_minimo
                ORDER BY stock ASC
            """

            resultados = self.db.ejecutar_consulta(query)
            return resultados or []

        except Exception as e:
            print(f"Error al obtener productos bajo stock: {str(e)}")
            return []

    def obtener_resumen_clientes(self):
        """Obtener resumen de clientes"""
        try:
            # Total clientes
            query_total = "SELECT COUNT(*) FROM clientes WHERE activo=1"
            total_clientes = self.db.ejecutar_consulta(query_total)[0][0]

            # Clientes activos (con compras)
            query_activos = """
                SELECT COUNT(DISTINCT cliente_id) FROM ventas
                WHERE cliente_id IS NOT NULL
            """
            clientes_activos = self.db.ejecutar_consulta(query_activos)[0][0]

            # Mayor compra individual
            query_mayor = "SELECT MAX(total) FROM ventas"
            resultado_mayor = self.db.ejecutar_consulta(query_mayor)
            mayor_compra = resultado_mayor[0][0] if resultado_mayor[0][0] else 0

            return {
                'total_clientes': total_clientes,
                'clientes_activos': clientes_activos,
                'mayor_compra': mayor_compra
            }

        except Exception as e:
            print(f"Error al obtener resumen de clientes: {str(e)}")
            return {}

    def obtener_top_clientes(self, limite=10):
        """Obtener top clientes por compras con números de recibo"""
        try:
            query = """
                SELECT c.nombre, c.apellido, SUM(v.total) as total_compras,
                       MAX(v.fecha_venta) as ultima_compra,
                       (SELECT v2.numero_recibo
                        FROM ventas v2
                        WHERE v2.cliente_id = c.id
                        ORDER BY v2.fecha_venta DESC LIMIT 1) as ultimo_recibo_venta,
                       (SELECT a.recibo_numero
                        FROM abonos a
                        WHERE a.cliente_id = c.id
                        ORDER BY a.fecha_abono DESC LIMIT 1) as ultimo_recibo_abono
                FROM clientes c
                JOIN ventas v ON c.id = v.cliente_id
                WHERE c.activo = 1
                GROUP BY c.id, c.nombre, c.apellido
                ORDER BY total_compras DESC
                LIMIT ?
            """

            resultados = self.db.ejecutar_consulta(query, (limite,))
            return resultados or []

        except Exception as e:
            print(f"Error al obtener top clientes: {str(e)}")
            return []

    def obtener_resumen_financiero(self):
        """Obtener resumen financiero"""
        try:
            # Ingresos del mes actual
            query_mes = """
                SELECT SUM(total) FROM ventas
                WHERE strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now')
            """
            resultado_mes = self.db.ejecutar_consulta(query_mes)
            ingresos_mes = resultado_mes[0][0] if resultado_mes[0][0] else 0

            # Cuentas por cobrar
            query_cobrar = """
                SELECT SUM(saldo_pendiente) FROM cuentas_corrientes
                WHERE activa = 1 AND saldo_pendiente > 0
            """
            resultado_cobrar = self.db.ejecutar_consulta(query_cobrar)
            cuentas_cobrar = resultado_cobrar[0][0] if resultado_cobrar[0][0] else 0

            # Promedio de venta
            query_promedio = "SELECT AVG(total) FROM ventas"
            resultado_promedio = self.db.ejecutar_consulta(query_promedio)
            promedio_venta = resultado_promedio[0][0] if resultado_promedio[0][0] else 0

            return {
                'ingresos_mes': ingresos_mes,
                'cuentas_cobrar': cuentas_cobrar,
                'promedio_venta': promedio_venta
            }

        except Exception as e:
            print(f"Error al obtener resumen financiero: {str(e)}")
            return {}

    def obtener_cuentas_por_cobrar(self):
        """Obtener cuentas por cobrar detalladas"""
        try:
            query = """
                SELECT cc.id, c.nombre, c.apellido, cc.saldo_total, cc.saldo_pendiente
                FROM cuentas_corrientes cc
                JOIN clientes c ON cc.cliente_id = c.id
                WHERE cc.activa = 1 AND cc.saldo_pendiente > 0
                ORDER BY cc.saldo_pendiente DESC
            """

            resultados = self.db.ejecutar_consulta(query)
            return resultados or []

        except Exception as e:
            print(f"Error al obtener cuentas por cobrar: {str(e)}")
            return []

    def obtener_ventas_por_rango_fecha(self, fecha_inicio, fecha_fin):
        """Obtener ventas en un rango de fechas"""
        try:
            query = """
                SELECT v.numero_recibo, v.fecha_venta, c.nombre, c.apellido,
                       COUNT(dv.id) as cantidad_productos, v.total
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN detalle_ventas dv ON v.id = dv.venta_id
                WHERE DATE(v.fecha_venta) BETWEEN ? AND ?
                GROUP BY v.id
                ORDER BY v.fecha_venta DESC
            """

            resultados = self.db.ejecutar_consulta(query, (fecha_inicio, fecha_fin))
            return resultados or []

        except Exception as e:
            print(f"Error al obtener ventas por rango: {str(e)}")
            return []

    def obtener_ventas_recientes(self, limite=50):
        """Obtener ventas recientes"""
        try:
            query = """
                SELECT v.numero_recibo, v.fecha_venta, c.nombre, c.apellido,
                       COUNT(dv.id) as cantidad_productos, v.total
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN detalle_ventas dv ON v.id = dv.venta_id
                GROUP BY v.id
                ORDER BY v.fecha_venta DESC
                LIMIT ?
            """

            resultados = self.db.ejecutar_consulta(query, (limite,))
            return resultados or []

        except Exception as e:
            print(f"Error al obtener ventas recientes: {str(e)}")
            return []

    def generar_reporte_completo(self):
        """Generar reporte completo del negocio"""
        try:
            reporte = {
                'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'resumen_general': self.obtener_resumen_general(),
                'productos_mas_vendidos': self.obtener_productos_mas_vendidos(5),
                'mejores_clientes': self.obtener_mejores_clientes(5),
                'inventario_critico': self.obtener_inventario_critico(),
                'analisis_categorias': self.obtener_analisis_categorias(),
                'ventas_ultimos_30_dias': self.obtener_ventas_por_periodo(30)
            }

            return reporte

        except Exception as e:
            print(f"Error al generar reporte completo: {str(e)}")
            return {}