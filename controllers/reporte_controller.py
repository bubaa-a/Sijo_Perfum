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
            
            # Ventas
            query_ventas = "SELECT COUNT(*), SUM(total) FROM ventas"
            resultado_ventas = self.db.ejecutar_consulta(query_ventas)[0]
            total_ventas = resultado_ventas[0]
            ingresos_totales = resultado_ventas[1] if resultado_ventas[1] else 0
            
            # Ganancia total
            query_ganancia = """
                SELECT SUM(dv.subtotal - (p.precio_compra * dv.cantidad))
                FROM detalle_ventas dv
                JOIN productos p ON dv.producto_id = p.id
            """
            resultado_ganancia = self.db.ejecutar_consulta(query_ganancia)
            ganancia_total = resultado_ganancia[0][0] if resultado_ganancia[0][0] else 0
            
            return {
                'total_productos': total_productos,
                'productos_stock_bajo': productos_stock_bajo,
                'valor_inventario': valor_inventario,
                'total_clientes': total_clientes,
                'total_ventas': total_ventas,
                'ingresos_totales': ingresos_totales,
                'ganancia_total': ganancia_total,
                'margen_ganancia': (ganancia_total / ingresos_totales * 100) if ingresos_totales > 0 else 0
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