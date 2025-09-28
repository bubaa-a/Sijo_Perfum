"""
Ventana para gestión de reportes con diseño mejorado
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.reporte_controller import ReporteController
from datetime import datetime, timedelta

class VentanaReportes:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ReporteController()
        self.ventana = None
        self.crear_ventana()
    
    def crear_ventana(self):
        """Crear ventana de reportes con diseño mejorado"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Reportes y Análisis")
        self.ventana.geometry("1500x900")
        self.ventana.configure(bg='#f8f9fa')
        
        # Hacer modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Crear interfaz
        self.crear_header()
        self.crear_panel_principal()
    
    def crear_header(self):
        """Crear header moderno"""
        header = tk.Frame(self.ventana, bg='#2c3e50', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Contenedor principal del header
        header_content = tk.Frame(header, bg='#2c3e50')
        header_content.pack(fill='both', expand=True, padx=30, pady=0)
        
        # Lado izquierdo - Título e ícono
        left_frame = tk.Frame(header_content, bg='#2c3e50')
        left_frame.pack(side='left', fill='y')
        
        # Título principal
        title_frame = tk.Frame(left_frame, bg='#2c3e50')
        title_frame.pack(side='left', pady=15)
        
        tk.Label(title_frame, text="📊", font=("Segoe UI", 24), 
                bg='#2c3e50', fg='#3498db').pack(side='left', padx=(0, 15))
        
        tk.Label(title_frame, text="REPORTES Y ANÁLISIS", 
                font=("Segoe UI", 20, "bold"), fg='white', bg='#2c3e50').pack(side='left')
        
        # Lado derecho - Botones
        right_frame = tk.Frame(header_content, bg='#2c3e50')
        right_frame.pack(side='right', fill='y')
        
        btn_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 10,
            'bd': 0
        }
        
        buttons_container = tk.Frame(right_frame, bg='#2c3e50')
        buttons_container.pack(pady=15)
        
        tk.Button(buttons_container, text="🔄 Actualizar", bg='#27ae60', fg='white',
                 command=self.actualizar_reportes, **btn_style).pack(side='left', padx=5)
        
        tk.Button(buttons_container, text="📤 Exportar", bg='#3498db', fg='white',
                 command=self.exportar_reportes, **btn_style).pack(side='left', padx=5)
        
        tk.Button(buttons_container, text="✖ Cerrar", bg='#e74c3c', fg='white',
                 command=self.cerrar_ventana, **btn_style).pack(side='left', padx=5)
    
    def crear_panel_principal(self):
        """Crear panel principal con diseño de cards"""
        main_container = tk.Frame(self.ventana, bg='#f8f9fa')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Crear pestañas con estilo moderno
        self.crear_pestanas_modernas(main_container)
    
    def crear_pestanas_modernas(self, parent):
        """Crear pestañas con diseño moderno"""
        # Configurar estilo de las pestañas
        style = ttk.Style()
        style.theme_use('clam')
        
        # Personalizar pestañas
        style.configure('Modern.TNotebook', 
                       background='#f8f9fa',
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background='#ecf0f1',
                       foreground='#2c3e50',
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#3498db'),
                           ('active', '#5dade2')],
                 foreground=[('selected', 'white'),
                           ('active', 'white')])
        
        # Crear notebook
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Pestañas
        self.crear_pestaña_dashboard()
        self.crear_pestaña_ventas()
        self.crear_pestaña_productos()
        self.crear_pestaña_clientes()
        self.crear_pestaña_financiero()
    
    def crear_pestaña_dashboard(self):
        """Crear pestaña de dashboard principal"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Dashboard")
        
        # Crear scroll
        canvas = tk.Canvas(frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cards de métricas principales
        self.crear_cards_metricas(scrollable_frame)
        
        # Gráficos principales
        self.crear_seccion_graficos(scrollable_frame)
        
        # Pack scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_cards_metricas(self, parent):
        """Crear cards con métricas principales"""
        metrics_frame = tk.Frame(parent, bg='#f8f9fa')
        metrics_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(metrics_frame, text="📈 Métricas Principales", 
                font=("Segoe UI", 16, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Contenedor de cards
        cards_container = tk.Frame(metrics_frame, bg='#f8f9fa')
        cards_container.pack(fill='x')
        
        # Obtener datos
        try:
            resumen = self.controller.obtener_resumen_general()
            
            # Definir métricas
            metricas = [
                {
                    'titulo': 'Ventas del Mes',
                    'valor': f"${resumen.get('ventas_mes', 0):,.0f}",
                    'color': '#3498db',
                    'icono': '💰',
                    'descripcion': f"{resumen.get('cantidad_ventas_mes', 0)} transacciones"
                },
                {
                    'titulo': 'Productos en Stock',
                    'valor': f"{resumen.get('total_productos', 0):,}",
                    'color': '#27ae60',
                    'icono': '📦',
                    'descripcion': f"Valor: ${resumen.get('valor_inventario', 0):,.0f}"
                },
                {
                    'titulo': 'Clientes Activos',
                    'valor': f"{resumen.get('total_clientes', 0):,}",
                    'color': '#9b59b6',
                    'icono': '👥',
                    'descripcion': f"{resumen.get('clientes_con_compras', 0)} con compras"
                },
                {
                    'titulo': 'Deuda Pendiente',
                    'valor': f"${resumen.get('deuda_pendiente', 0):,.0f}",
                    'color': '#e74c3c',
                    'icono': '⚠️',
                    'descripcion': f"{resumen.get('clientes_con_deuda', 0)} clientes"
                }
            ]
            
            # Crear cards
            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(cards_container, metrica, i)
                
        except Exception as e:
            error_label = tk.Label(cards_container, 
                                 text=f"Error al cargar métricas: {str(e)}", 
                                 bg='#f8f9fa', fg='#e74c3c', font=("Segoe UI", 12))
            error_label.pack(pady=20)
    
    def crear_card_metrica(self, parent, metrica, index):
        """Crear una card individual de métrica"""
        # Card container
        card = tk.Frame(parent, bg='white', relief='flat', bd=0)
        card.grid(row=0, column=index, padx=10, pady=10, sticky='ew')
        
        # Configurar grid
        parent.grid_columnconfigure(index, weight=1)
        
        # Sombra simulada
        shadow = tk.Frame(parent, bg='#ddd', height=2)
        shadow.grid(row=1, column=index, sticky='ew', padx=12)
        
        # Contenido de la card
        content_frame = tk.Frame(card, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header con ícono y color
        header_frame = tk.Frame(content_frame, bg=metrica['color'], height=5)
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Ícono y título
        title_frame = tk.Frame(content_frame, bg='white')
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text=metrica['icono'], 
                font=("Segoe UI", 20), bg='white').pack(side='left')
        
        tk.Label(title_frame, text=metrica['titulo'], 
                font=("Segoe UI", 12, "bold"), bg='white', fg='#7f8c8d').pack(side='left', padx=(10, 0))
        
        # Valor principal
        tk.Label(content_frame, text=metrica['valor'], 
                font=("Segoe UI", 24, "bold"), bg='white', fg=metrica['color']).pack(anchor='w', pady=(10, 0))
        
        # Descripción
        tk.Label(content_frame, text=metrica['descripcion'], 
                font=("Segoe UI", 10), bg='white', fg='#95a5a6').pack(anchor='w', pady=(5, 0))
    
    def crear_seccion_graficos(self, parent):
        """Crear sección de gráficos"""
        graficos_frame = tk.Frame(parent, bg='#f8f9fa')
        graficos_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(graficos_frame, text="📈 Análisis Visual", 
                font=("Segoe UI", 16, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Contenedor de gráficos
        charts_container = tk.Frame(graficos_frame, bg='#f8f9fa')
        charts_container.pack(fill='both', expand=True)
        
        # Gráfico de ventas por mes
        self.crear_grafico_ventas_mes(charts_container)
        
        # Gráfico de productos más vendidos
        self.crear_grafico_productos_vendidos(charts_container)
    
    def crear_grafico_ventas_mes(self, parent):
        """Crear gráfico de ventas por mes"""
        chart_frame = tk.LabelFrame(parent, text="💰 Ventas por Mes", 
                                   font=("Segoe UI", 12, "bold"), bg='white', fg='#2c3e50')
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Obtener datos
        try:
            datos_ventas = self.controller.obtener_ventas_por_mes()
            
            if datos_ventas:
                # Crear tabla con los datos
                tabla_frame = tk.Frame(chart_frame, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Headers
                headers = ['Mes', 'Ventas', 'Cantidad', 'Promedio']
                for i, header in enumerate(headers):
                    tk.Label(tabla_frame, text=header, font=("Segoe UI", 11, "bold"),
                            bg='#3498db', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')
                
                # Datos
                for i, fila in enumerate(datos_ventas, 1):
                    mes = fila[0]
                    ventas = fila[1]
                    cantidad = fila[2]
                    promedio = ventas / cantidad if cantidad > 0 else 0
                    
                    color_fila = '#ecf0f1' if i % 2 == 0 else 'white'
                    
                    tk.Label(tabla_frame, text=mes, bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_frame, text=f"${ventas:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(tabla_frame, text=f"{cantidad:,}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_frame, text=f"${promedio:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=3, sticky='ew')
                
                # Configurar columnas
                for i in range(4):
                    tabla_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(chart_frame, text="No hay datos de ventas disponibles", 
                        bg='white', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True)
                
        except Exception as e:
            tk.Label(chart_frame, text=f"Error al cargar datos: {str(e)}", 
                    bg='white', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)
    
    def crear_grafico_productos_vendidos(self, parent):
        """Crear gráfico de productos más vendidos"""
        chart_frame = tk.LabelFrame(parent, text="🏆 Productos Más Vendidos", 
                                   font=("Segoe UI", 12, "bold"), bg='white', fg='#2c3e50')
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            productos_vendidos = self.controller.obtener_productos_mas_vendidos(10)
            
            if productos_vendidos:
                # Crear tabla
                tabla_frame = tk.Frame(chart_frame, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Headers
                headers = ['#', 'Producto', 'Cantidad Vendida', 'Total Ventas']
                for i, header in enumerate(headers):
                    tk.Label(tabla_frame, text=header, font=("Segoe UI", 11, "bold"),
                            bg='#27ae60', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')
                
                # Datos
                for i, producto in enumerate(productos_vendidos, 1):
                    nombre = producto[0]
                    cantidad = producto[1]
                    total = producto[2]
                    
                    color_fila = '#ecf0f1' if i % 2 == 0 else 'white'
                    
                    tk.Label(tabla_frame, text=f"{i}", bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_frame, text=nombre, bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='w')
                    tk.Label(tabla_frame, text=f"{cantidad:,}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_frame, text=f"${total:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=3, sticky='ew')
                
                # Configurar columnas
                tabla_frame.grid_columnconfigure(1, weight=2)
                for i in [0, 2, 3]:
                    tabla_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(chart_frame, text="No hay datos de productos disponibles", 
                        bg='white', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True)
                
        except Exception as e:
            tk.Label(chart_frame, text=f"Error al cargar productos: {str(e)}", 
                    bg='white', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)
    
    def crear_pestaña_ventas(self):
        """Crear pestaña de reportes de ventas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💰 Ventas")
        
        # Contenido principal
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(main_content, text="📊 Análisis de Ventas", 
                font=("Segoe UI", 18, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Filtros de fecha
        self.crear_filtros_fecha(main_content)
        
        # Reportes de ventas
        self.crear_tabla_ventas_detallada(main_content)
    
    def crear_filtros_fecha(self, parent):
        """Crear filtros de fecha"""
        filtros_frame = tk.LabelFrame(parent, text="🗓️ Filtros de Fecha", 
                                     font=("Segoe UI", 12, "bold"), bg='white')
        filtros_frame.pack(fill='x', pady=(0, 20))
        
        content = tk.Frame(filtros_frame, bg='white')
        content.pack(fill='x', padx=20, pady=15)
        
        # Variables de fecha
        self.fecha_inicio_var = tk.StringVar()
        self.fecha_fin_var = tk.StringVar()
        
        # Fecha de inicio
        tk.Label(content, text="Desde:", font=("Segoe UI", 10, "bold"), 
                bg='white').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        fecha_inicio_entry = tk.Entry(content, textvariable=self.fecha_inicio_var, 
                                     font=("Segoe UI", 10), width=12)
        fecha_inicio_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Fecha fin
        tk.Label(content, text="Hasta:", font=("Segoe UI", 10, "bold"), 
                bg='white').grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        fecha_fin_entry = tk.Entry(content, textvariable=self.fecha_fin_var, 
                                  font=("Segoe UI", 10), width=12)
        fecha_fin_entry.grid(row=0, column=3, padx=(0, 20))
        
        # Botones de filtro rápido
        btn_style = {'font': ('Segoe UI', 9), 'relief': 'flat', 'cursor': 'hand2', 'padx': 10, 'pady': 5}
        
        tk.Button(content, text="Hoy", bg='#3498db', fg='white',
                 command=self.filtro_hoy, **btn_style).grid(row=0, column=4, padx=2)
        
        tk.Button(content, text="Esta Semana", bg='#27ae60', fg='white',
                 command=self.filtro_semana, **btn_style).grid(row=0, column=5, padx=2)
        
        tk.Button(content, text="Este Mes", bg='#9b59b6', fg='white',
                 command=self.filtro_mes, **btn_style).grid(row=0, column=6, padx=2)
        
        tk.Button(content, text="Aplicar Filtro", bg='#e67e22', fg='white',
                 command=self.aplicar_filtro_fecha, **btn_style).grid(row=0, column=7, padx=(20, 0))
        
        # Establecer fechas por defecto (este mes)
        self.filtro_mes()
    
    def crear_tabla_ventas_detallada(self, parent):
        """Crear tabla detallada de ventas"""
        tabla_frame = tk.LabelFrame(parent, text="📋 Ventas Detalladas", 
                                   font=("Segoe UI", 12, "bold"), bg='white')
        tabla_frame.pack(fill='both', expand=True)
        
        # Treeview para las ventas
        columns = ('fecha', 'cliente', 'productos', 'total')
        self.tree_ventas = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=15)
        
        # Configurar headers
        self.tree_ventas.heading('fecha', text='Fecha')
        self.tree_ventas.heading('cliente', text='Cliente')
        self.tree_ventas.heading('productos', text='Productos')
        self.tree_ventas.heading('total', text='Total')
        
        # Configurar columnas
        self.tree_ventas.column('fecha', width=120, anchor='center')
        self.tree_ventas.column('cliente', width=200, anchor='w')
        self.tree_ventas.column('productos', width=300, anchor='w')
        self.tree_ventas.column('total', width=120, anchor='e')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree_ventas.yview)
        h_scrollbar = ttk.Scrollbar(tabla_frame, orient='horizontal', command=self.tree_ventas.xview)
        self.tree_ventas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack
        self.tree_ventas.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        v_scrollbar.pack(side='right', fill='y')
        
        # Cargar datos iniciales
        self.cargar_ventas_tabla()
    
    def crear_pestaña_productos(self):
        """Crear pestaña de reportes de productos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Productos")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="📦 Análisis de Inventario", 
                font=("Segoe UI", 18, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Cards de productos
        self.crear_cards_productos(main_content)
        
        # Tabla de productos con bajo stock
        self.crear_tabla_bajo_stock(main_content)
    
    def crear_cards_productos(self, parent):
        """Crear cards de métricas de productos"""
        cards_frame = tk.Frame(parent, bg='#f8f9fa')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        try:
            # Obtener datos de productos
            resumen_productos = self.controller.obtener_resumen_productos()
            
            metricas_productos = [
                {
                    'titulo': 'Total Productos',
                    'valor': f"{resumen_productos.get('total_productos', 0):,}",
                    'color': '#3498db',
                    'icono': '📦',
                    'descripcion': 'En inventario'
                },
                {
                    'titulo': 'Valor Inventario',
                    'valor': f"${resumen_productos.get('valor_total', 0):,.0f}",
                    'color': '#27ae60',
                    'icono': '💎',
                    'descripcion': 'Valor total'
                },
                {
                    'titulo': 'Stock Bajo',
                    'valor': f"{resumen_productos.get('productos_bajo_stock', 0):,}",
                    'color': '#e74c3c',
                    'icono': '⚠️',
                    'descripción': 'Requieren atención'
                }
            ]
            
            for i, metrica in enumerate(metricas_productos):
                self.crear_card_metrica(cards_frame, metrica, i)
                
        except Exception as e:
            tk.Label(cards_frame, text=f"Error al cargar métricas de productos: {str(e)}", 
                    bg='#f8f9fa', fg='#e74c3c').pack()
    
    def crear_tabla_bajo_stock(self, parent):
        """Crear tabla de productos con bajo stock"""
        tabla_frame = tk.LabelFrame(parent, text="⚠️ Productos con Stock Bajo", 
                                   font=("Segoe UI", 12, "bold"), bg='white')
        tabla_frame.pack(fill='both', expand=True)
        
        try:
            productos_bajo_stock = self.controller.obtener_productos_bajo_stock()
            
            if productos_bajo_stock:
                # Headers
                headers_frame = tk.Frame(tabla_frame, bg='white')
                headers_frame.pack(fill='x', padx=20, pady=(20, 0))
                
                headers = ['Producto', 'Stock Actual', 'Stock Mínimo', 'Estado']
                colors = ['#e74c3c'] * 4
                
                for i, (header, color) in enumerate(zip(headers, colors)):
                    tk.Label(headers_frame, text=header, font=("Segoe UI", 11, "bold"),
                            bg=color, fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')
                
                # Configurar grid
                for i in range(len(headers)):
                    headers_frame.grid_columnconfigure(i, weight=1)
                
                # Datos
                data_frame = tk.Frame(tabla_frame, bg='white')
                data_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
                
                for i, producto in enumerate(productos_bajo_stock):
                    nombre = producto[0]
                    stock_actual = producto[1]
                    stock_minimo = producto[2]
                    estado = "CRÍTICO" if stock_actual == 0 else "BAJO"
                    
                    color_fila = '#ffebee' if estado == "CRÍTICO" else '#fff3e0'
                    
                    tk.Label(data_frame, text=nombre, bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(data_frame, text=f"{stock_actual:,}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(data_frame, text=f"{stock_minimo:,}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(data_frame, text=estado, bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8, 
                            fg='#c0392b' if estado == "CRÍTICO" else '#e67e22').grid(row=i, column=3, sticky='ew')
                
                # Configurar grid
                for i in range(4):
                    data_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(tabla_frame, text="✅ Todos los productos tienen stock suficiente", 
                        bg='white', fg='#27ae60', font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)
                
        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar productos: {str(e)}", 
                    bg='white', fg='#e74c3c').pack(expand=True)
    
    def crear_pestaña_clientes(self):
        """Crear pestaña de reportes de clientes"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Clientes")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="👥 Análisis de Clientes", 
                font=("Segoe UI", 18, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Métricas de clientes
        self.crear_metricas_clientes(main_content)
        
        # Top clientes
        self.crear_tabla_top_clientes(main_content)
    
    def crear_metricas_clientes(self, parent):
        """Crear métricas de clientes"""
        metrics_frame = tk.Frame(parent, bg='#f8f9fa')
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        try:
            resumen_clientes = self.controller.obtener_resumen_clientes()
            
            metricas = [
                {
                    'titulo': 'Total Clientes',
                    'valor': f"{resumen_clientes.get('total_clientes', 0):,}",
                    'color': '#9b59b6',
                    'icono': '👥',
                    'descripcion': 'Registrados'
                },
                {
                    'titulo': 'Clientes Activos',
                    'valor': f"{resumen_clientes.get('clientes_activos', 0):,}",
                    'color': '#27ae60',
                    'icono': '✅',
                    'descripcion': 'Con compras'
                },
                {
                    'titulo': 'Cliente Top',
                    'valor': f"${resumen_clientes.get('mayor_compra', 0):,.0f}",
                    'color': '#f39c12',
                    'icono': '🏆',
                    'descripcion': 'Mayor compra'
                }
            ]
            
            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(metrics_frame, metrica, i)
                
        except Exception as e:
            tk.Label(metrics_frame, text=f"Error al cargar métricas: {str(e)}", 
                    bg='#f8f9fa', fg='#e74c3c').pack()
    
    def crear_tabla_top_clientes(self, parent):
        """Crear tabla de top clientes"""
        tabla_frame = tk.LabelFrame(parent, text="🏆 Top 10 Clientes", 
                                   font=("Segoe UI", 12, "bold"), bg='white')
        tabla_frame.pack(fill='both', expand=True)
        
        try:
            top_clientes = self.controller.obtener_top_clientes(10)
            
            if top_clientes:
                # Headers
                headers_frame = tk.Frame(tabla_frame, bg='white')
                headers_frame.pack(fill='x', padx=20, pady=(20, 0))
                
                headers = ['#', 'Cliente', 'Total Compras', 'Última Compra']
                
                for i, header in enumerate(headers):
                    tk.Label(headers_frame, text=header, font=("Segoe UI", 11, "bold"),
                            bg='#f39c12', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')
                
                headers_frame.grid_columnconfigure(1, weight=2)
                for i in [0, 2, 3]:
                    headers_frame.grid_columnconfigure(i, weight=1)
                
                # Datos
                data_frame = tk.Frame(tabla_frame, bg='white')
                data_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
                
                for i, cliente in enumerate(top_clientes, 1):
                    nombre = f"{cliente[0]} {cliente[1]}"
                    total = cliente[2]
                    ultima_compra = cliente[3] if cliente[3] else "N/A"
                    
                    color_fila = '#fff8e1' if i <= 3 else ('#f8f9fa' if i % 2 == 0 else 'white')
                    
                    tk.Label(data_frame, text=f"{i}", bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i-1, column=0, sticky='ew')
                    tk.Label(data_frame, text=nombre, bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i-1, column=1, sticky='w')
                    tk.Label(data_frame, text=f"${total:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i-1, column=2, sticky='ew')
                    tk.Label(data_frame, text=ultima_compra[:10] if ultima_compra != "N/A" else "N/A", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i-1, column=3, sticky='ew')
                
                data_frame.grid_columnconfigure(1, weight=2)
                for i in [0, 2, 3]:
                    data_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(tabla_frame, text="No hay datos de clientes disponibles", 
                        bg='white', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True, pady=40)
                
        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar clientes: {str(e)}", 
                    bg='white', fg='#e74c3c').pack(expand=True)
    
    def crear_pestaña_financiero(self):
        """Crear pestaña de análisis financiero"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💹 Financiero")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="💹 Análisis Financiero", 
                font=("Segoe UI", 18, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Métricas financieras
        self.crear_metricas_financieras(main_content)
        
        # Análisis de cuentas por cobrar
        self.crear_analisis_cuentas_cobrar(main_content)
    
    def crear_metricas_financieras(self, parent):
        """Crear métricas financieras"""
        metrics_frame = tk.Frame(parent, bg='#f8f9fa')
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        try:
            resumen_financiero = self.controller.obtener_resumen_financiero()
            
            metricas = [
                {
                    'titulo': 'Ingresos del Mes',
                    'valor': f"${resumen_financiero.get('ingresos_mes', 0):,.0f}",
                    'color': '#27ae60',
                    'icono': '💰',
                    'descripcion': 'Ventas totales'
                },
                {
                    'titulo': 'Cuentas por Cobrar',
                    'valor': f"${resumen_financiero.get('cuentas_cobrar', 0):,.0f}",
                    'color': '#e74c3c',
                    'icono': '📋',
                    'descripcion': 'Pendiente de cobro'
                },
                {
                    'titulo': 'Promedio Venta',
                    'valor': f"${resumen_financiero.get('promedio_venta', 0):,.0f}",
                    'color': '#3498db',
                    'icono': '📊',
                    'descripcion': 'Por transacción'
                }
            ]
            
            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(metrics_frame, metrica, i)
                
        except Exception as e:
            tk.Label(metrics_frame, text=f"Error al cargar métricas financieras: {str(e)}", 
                    bg='#f8f9fa', fg='#e74c3c').pack()
    
    def crear_analisis_cuentas_cobrar(self, parent):
        """Crear análisis de cuentas por cobrar"""
        tabla_frame = tk.LabelFrame(parent, text="📋 Cuentas por Cobrar", 
                                   font=("Segoe UI", 12, "bold"), bg='white')
        tabla_frame.pack(fill='both', expand=True)
        
        try:
            cuentas_cobrar = self.controller.obtener_cuentas_por_cobrar()
            
            if cuentas_cobrar:
                # Headers
                headers_frame = tk.Frame(tabla_frame, bg='white')
                headers_frame.pack(fill='x', padx=20, pady=(20, 0))
                
                headers = ['Cliente', 'Deuda Total', 'Saldo Pendiente', 'Estado']
                
                for i, header in enumerate(headers):
                    tk.Label(headers_frame, text=header, font=("Segoe UI", 11, "bold"),
                            bg='#e74c3c', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')
                
                for i in range(len(headers)):
                    headers_frame.grid_columnconfigure(i, weight=1)
                
                # Datos
                data_frame = tk.Frame(tabla_frame, bg='white')
                data_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
                
                total_pendiente = 0
                for i, cuenta in enumerate(cuentas_cobrar):
                    cliente = f"{cuenta[1]} {cuenta[2]}"
                    deuda_total = cuenta[3]
                    saldo_pendiente = cuenta[4]
                    total_pendiente += saldo_pendiente
                    
                    if saldo_pendiente > 100000:
                        estado = "ALTA"
                        color_estado = '#c0392b'
                        color_fila = '#ffebee'
                    elif saldo_pendiente > 50000:
                        estado = "MEDIA"
                        color_estado = '#e67e22'
                        color_fila = '#fff3e0'
                    else:
                        estado = "BAJA"
                        color_estado = '#f39c12'
                        color_fila = '#fffef7'
                    
                    tk.Label(data_frame, text=cliente, bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='w')
                    tk.Label(data_frame, text=f"${deuda_total:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(data_frame, text=f"${saldo_pendiente:,.0f}", bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(data_frame, text=estado, bg=color_fila, 
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8, fg=color_estado).grid(row=i, column=3, sticky='ew')
                
                for i in range(4):
                    data_frame.grid_columnconfigure(i, weight=1)
                
                # Total
                total_frame = tk.Frame(tabla_frame, bg='#2c3e50')
                total_frame.pack(fill='x', padx=20, pady=(0, 20))
                
                tk.Label(total_frame, text=f"TOTAL PENDIENTE: ${total_pendiente:,.0f}", 
                        font=("Segoe UI", 12, "bold"), bg='#2c3e50', fg='white', pady=10).pack()
            else:
                tk.Label(tabla_frame, text="✅ No hay cuentas pendientes por cobrar", 
                        bg='white', fg='#27ae60', font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)
                
        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar cuentas por cobrar: {str(e)}", 
                    bg='white', fg='#e74c3c').pack(expand=True)
    
    # Métodos de filtros de fecha
    def filtro_hoy(self):
        """Filtro para el día de hoy"""
        hoy = datetime.now()
        self.fecha_inicio_var.set(hoy.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(hoy.strftime('%Y-%m-%d'))
    
    def filtro_semana(self):
        """Filtro para esta semana"""
        hoy = datetime.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        self.fecha_inicio_var.set(inicio_semana.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(fin_semana.strftime('%Y-%m-%d'))
    
    def filtro_mes(self):
        """Filtro para este mes"""
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year+1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month+1, day=1) - timedelta(days=1)
        self.fecha_inicio_var.set(inicio_mes.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(fin_mes.strftime('%Y-%m-%d'))
    
    def aplicar_filtro_fecha(self):
        """Aplicar filtro de fecha a los reportes"""
        try:
            fecha_inicio = self.fecha_inicio_var.get()
            fecha_fin = self.fecha_fin_var.get()
            
            if fecha_inicio and fecha_fin:
                self.cargar_ventas_tabla(fecha_inicio, fecha_fin)
                messagebox.showinfo("Filtro Aplicado", f"Mostrando datos desde {fecha_inicio} hasta {fecha_fin}")
            else:
                messagebox.showwarning("Advertencia", "Seleccione ambas fechas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro: {str(e)}")
    
    def cargar_ventas_tabla(self, fecha_inicio=None, fecha_fin=None):
        """Cargar datos en la tabla de ventas"""
        try:
            # Limpiar tabla
            for item in self.tree_ventas.get_children():
                self.tree_ventas.delete(item)
            
            # Obtener ventas
            if fecha_inicio and fecha_fin:
                ventas = self.controller.obtener_ventas_por_rango_fecha(fecha_inicio, fecha_fin)
            else:
                ventas = self.controller.obtener_ventas_recientes(50)  # Últimas 50 ventas
            
            # Cargar datos
            for venta in ventas:
                fecha = venta[0][:10] if venta[0] else 'N/A'
                cliente = f"{venta[1]} {venta[2]}" if venta[1] and venta[2] else "Cliente no especificado"
                productos = f"{venta[3]} productos" if venta[3] else "0 productos"
                total = venta[4] if venta[4] else 0
                
                self.tree_ventas.insert('', 'end', values=(
                    fecha,
                    cliente,
                    productos,
                    f"${total:,.0f}"
                ))
                
        except Exception as e:
            print(f"Error al cargar ventas: {str(e)}")
    
    def actualizar_reportes(self):
        """Actualizar todos los reportes"""
        try:
            # Recargar pestañas activas
            self.cargar_ventas_tabla()
            messagebox.showinfo("Actualizado", "Reportes actualizados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def exportar_reportes(self):
        """Exportar reportes (funcionalidad futura)"""
        messagebox.showinfo("Exportar", "Funcionalidad de exportación en desarrollo")
    
    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()