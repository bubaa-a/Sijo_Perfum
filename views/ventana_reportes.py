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
        """Crear ventana de reportes con diseño moderno elegante"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("📊 Reportes y Análisis - Sistema Pro")
        self.ventana.geometry("1600x950")
        self.ventana.configure(bg='#1a1a2e')

        # Hacer modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Crear interfaz moderna
        self.crear_header_moderno()
        self.crear_panel_principal_elegante()
    
    def crear_header_moderno(self):
        """Crear header elegante estilo glassmorphism"""
        # Header principal con gradiente
        header = tk.Frame(self.ventana, bg='#0e4b99', height=120)
        header.pack(fill='x', padx=20, pady=(20, 0))
        header.pack_propagate(False)

        # Container interno con bordes suavizados
        header_content = tk.Frame(header, bg='#0e4b99', relief='flat', bd=0)
        header_content.pack(fill='both', expand=True, padx=3, pady=3)

        # Esquinas redondeadas del header
        self.crear_esquinas_redondeadas_header(header_content)

        # Lado izquierdo - Logo y título elegante
        left_section = tk.Frame(header_content, bg='#0e4b99')
        left_section.pack(side='left', padx=40, pady=25)

        # Logo/Icono moderno
        logo_frame = tk.Frame(left_section, bg='#ff6b6b', width=60, height=60, relief='flat')
        logo_frame.pack_propagate(False)
        logo_frame.pack(side='left')

        logo_text = tk.Label(logo_frame, text="📊", font=("Segoe UI", 24),
                            fg='white', bg='#ff6b6b')
        logo_text.place(relx=0.5, rely=0.5, anchor='center')

        # Títulos modernos
        titles_frame = tk.Frame(left_section, bg='#0e4b99')
        titles_frame.pack(side='left', padx=(20, 0))

        main_title = tk.Label(titles_frame, text="CENTRO DE REPORTES",
                             font=("Segoe UI", 24, "bold"), fg='#ffffff', bg='#0e4b99')
        main_title.pack(anchor='w')

        subtitle = tk.Label(titles_frame, text="🚀 Analytics & Business Intelligence",
                           font=("Segoe UI", 11), fg='#4ecdc4', bg='#0e4b99')
        subtitle.pack(anchor='w', pady=(2, 0))

        # Lado derecho - Panel de botones modernos
        right_section = tk.Frame(header_content, bg='#0e4b99')
        right_section.pack(side='right', padx=40, pady=25)

        # Botones con diseño moderno
        self.crear_botones_header_modernos(right_section)

    def crear_esquinas_redondeadas_header(self, header_content):
        """Crear esquinas redondeadas para el header"""
        # Esquinas del header
        top_left = tk.Frame(header_content, bg='#1a1a2e', width=10, height=10)
        top_left.place(x=0, y=0)

        top_right = tk.Frame(header_content, bg='#1a1a2e', width=10, height=10)
        top_right.place(relx=1.0, x=-10, y=0)

        bottom_left = tk.Frame(header_content, bg='#1a1a2e', width=10, height=10)
        bottom_left.place(x=0, rely=1.0, y=-10)

        bottom_right = tk.Frame(header_content, bg='#1a1a2e', width=10, height=10)
        bottom_right.place(relx=1.0, x=-10, rely=1.0, y=-10)

    def crear_botones_header_modernos(self, parent):
        """Crear botones modernos en el header"""
        buttons_container = tk.Frame(parent, bg='#0e4b99')
        buttons_container.pack()

        # Datos de botones modernos
        botones = [
            {"texto": "🔄 Actualizar", "color": "#4ecdc4", "comando": self.actualizar_reportes},
            {"texto": "📤 Exportar", "color": "#feca57", "comando": self.exportar_reportes},
            {"texto": "❌ Cerrar", "color": "#ff6b6b", "comando": self.cerrar_ventana}
        ]

        for i, btn_data in enumerate(botones):
            btn_frame = tk.Frame(buttons_container, bg=btn_data["color"], relief='flat')
            btn_frame.pack(side='left', padx=8)

            btn = tk.Button(btn_frame, text=btn_data["texto"],
                           font=("Segoe UI", 10, "bold"),
                           fg='white', bg=btn_data["color"],
                           relief='flat', bd=0, cursor='hand2',
                           padx=15, pady=8,
                           command=btn_data["comando"])
            btn.pack(padx=2, pady=2)

            # Esquinas redondeadas simples para botones
            self.crear_esquinas_boton(btn_frame)

    def crear_esquinas_boton(self, btn_frame):
        """Crear esquinas redondeadas para botones"""
        # Esquinas pequeñas para botones
        tk.Frame(btn_frame, bg='#1a1a2e', width=4, height=4).place(x=0, y=0)
        tk.Frame(btn_frame, bg='#1a1a2e', width=4, height=4).place(relx=1.0, x=-4, y=0)
        tk.Frame(btn_frame, bg='#1a1a2e', width=4, height=4).place(x=0, rely=1.0, y=-4)
        tk.Frame(btn_frame, bg='#1a1a2e', width=4, height=4).place(relx=1.0, x=-4, rely=1.0, y=-4)

    def crear_panel_principal_elegante(self):
        """Crear panel principal con diseño moderno elegante"""
        main_container = tk.Frame(self.ventana, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=25, pady=(25, 20))

        # Crear pestañas con estilo ultra moderno
        self.crear_pestanas_ultramodernas(main_container)
    
    def crear_pestanas_ultramodernas(self, parent):
        """Crear pestañas con diseño ultra moderno"""
        # Configurar estilo de las pestañas modernas
        style = ttk.Style()
        style.theme_use('clam')

        # Personalizar pestañas con colores modernos
        style.configure('UltraModern.TNotebook',
                       background='#1a1a2e',
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])

        style.configure('UltraModern.TNotebook.Tab',
                       background='#2a2a4e',
                       foreground='#a8dadc',
                       padding=[25, 12],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)

        style.map('UltraModern.TNotebook.Tab',
                 background=[('selected', '#4ecdc4'),
                           ('active', '#6ed5d2')],
                 foreground=[('selected', '#ffffff'),
                           ('active', '#ffffff')])

        # Crear notebook con sombra
        notebook_container = tk.Frame(parent, bg='#0d0d1a')
        notebook_container.pack(fill='both', expand=True, padx=4, pady=4)

        self.notebook = ttk.Notebook(notebook_container, style='UltraModern.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=2, pady=2)

        # Pestañas con iconos modernos
        self.crear_pestaña_dashboard_moderna()
        self.crear_pestaña_ventas_moderna()
        self.crear_pestaña_productos_moderna()
        self.crear_pestaña_clientes_moderna()
        self.crear_pestaña_financiero_moderna()
    
    def crear_pestaña_dashboard_moderna(self):
        """Crear pestaña de dashboard principal con diseño moderno"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏠 Dashboard")

        # Container principal con fondo moderno
        main_frame = tk.Frame(frame, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True)

        # Crear scroll con estilo moderno
        canvas = tk.Canvas(main_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cards de métricas principales
        self.crear_cards_metricas_dashboard(scrollable_frame)
        
        # Gráficos principales
        self.crear_seccion_graficos(scrollable_frame)
        
        # Pack scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_pestaña_ventas_moderna(self):
        """Crear pestaña de ventas moderna"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💰 Ventas")

        main_content = tk.Frame(frame, bg='#1a1a2e')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Crear filtros y tabla con diseño moderno
        self.crear_filtros_fecha_moderno(main_content)
        self.crear_tabla_ventas_detallada_moderna(main_content)

    def crear_pestaña_productos_moderna(self):
        """Crear pestaña de productos moderna"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Productos")

        main_content = tk.Frame(frame, bg='#1a1a2e')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Cards de productos
        self.crear_cards_productos_modernas(main_content)

        # Tabla de productos con bajo stock
        self.crear_tabla_bajo_stock_moderna(main_content)

    def crear_pestaña_clientes_moderna(self):
        """Crear pestaña de clientes moderna"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Clientes")

        main_content = tk.Frame(frame, bg='#1a1a2e')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Métricas de clientes
        self.crear_metricas_clientes_modernas(main_content)

        # Top clientes
        self.crear_tabla_top_clientes_moderna(main_content)

    def crear_pestaña_financiero_moderna(self):
        """Crear pestaña financiera moderna"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💳 Financiero")

        main_content = tk.Frame(frame, bg='#1a1a2e')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Métricas financieras
        self.crear_metricas_financieras_modernas(main_content)

        # Análisis de cuentas por cobrar
        self.crear_analisis_cuentas_cobrar_moderno(main_content)

    def crear_cards_metricas_dashboard(self, parent):
        """Crear cards con métricas principales para dashboard"""
        metrics_frame = tk.Frame(parent, bg='#1a1a2e')
        metrics_frame.pack(fill='x', padx=20, pady=20)

        tk.Label(metrics_frame, text="📊 MÉTRICAS PRINCIPALES",
                font=("Segoe UI", 16, "bold"), bg='#1a1a2e', fg='#4ecdc4').pack(anchor='w', pady=(0, 20))

        # Contenedor de cards
        cards_container = tk.Frame(metrics_frame, bg='#1a1a2e')
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

            # Crear cards modernas
            for i, metrica in enumerate(metricas):
                self.crear_card_metrica_moderna_dashboard(cards_container, metrica, i)

        except Exception as e:
            error_label = tk.Label(cards_container,
                                 text=f"Error al cargar métricas: {str(e)}",
                                 bg='#1a1a2e', fg='#e74c3c', font=("Segoe UI", 12))
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
        graficos_frame = tk.Frame(parent, bg='#1a1a2e')
        graficos_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(graficos_frame, text="📈 ANÁLISIS VISUAL",
                font=("Segoe UI", 16, "bold"), bg='#1a1a2e', fg='#4ecdc4').pack(anchor='w', pady=(0, 20))

        # Contenedor de gráficos
        charts_container = tk.Frame(graficos_frame, bg='#1a1a2e')
        charts_container.pack(fill='both', expand=True)
        
        # Gráfico de ventas por mes
        self.crear_grafico_ventas_mes(charts_container)
        
        # Gráfico de productos más vendidos
        self.crear_grafico_productos_vendidos(charts_container)
    
    def crear_grafico_ventas_mes(self, parent):
        """Crear gráfico de ventas por mes"""
        chart_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header moderno
        header = tk.Frame(chart_frame, bg='#3498db', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="📅 VENTAS POR MES",
                font=("Segoe UI", 12, "bold"), bg='#3498db', fg='white').pack(expand=True)
        
        # Obtener datos
        try:
            datos_ventas = self.controller.obtener_ventas_por_mes()
            
            if datos_ventas:
                # Crear tabla con los datos
                tabla_frame = tk.Frame(chart_frame, bg='#2a2a4e')
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

                    color_fila = '#1e1e3f' if i % 2 == 0 else '#2a2a4e'
                    text_color = '#ffffff'

                    tk.Label(tabla_frame, text=mes, bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_frame, text=f"${ventas:,.0f}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(tabla_frame, text=f"{cantidad:,}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_frame, text=f"${promedio:,.0f}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=3, sticky='ew')

                # Configurar columnas
                for i in range(4):
                    tabla_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(chart_frame, text="No hay datos de ventas disponibles",
                        bg='#2a2a4e', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True)
                
        except Exception as e:
            tk.Label(chart_frame, text=f"Error al cargar datos: {str(e)}",
                    bg='#2a2a4e', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)
    
    def crear_grafico_productos_vendidos(self, parent):
        """Crear gráfico de productos más vendidos"""
        chart_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header moderno
        header = tk.Frame(chart_frame, bg='#27ae60', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="🏆 PRODUCTOS MÁS VENDIDOS",
                font=("Segoe UI", 12, "bold"), bg='#27ae60', fg='white').pack(expand=True)
        
        try:
            productos_vendidos = self.controller.obtener_productos_mas_vendidos(10)
            
            if productos_vendidos:
                # Crear tabla
                tabla_frame = tk.Frame(chart_frame, bg='#2a2a4e')
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

                    color_fila = '#1e1e3f' if i % 2 == 0 else '#2a2a4e'
                    text_color = '#ffffff'

                    tk.Label(tabla_frame, text=f"{i}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_frame, text=nombre, bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='w')
                    tk.Label(tabla_frame, text=f"{cantidad:,}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_frame, text=f"${total:,.0f}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=3, sticky='ew')

                # Configurar columnas
                tabla_frame.grid_columnconfigure(1, weight=2)
                for i in [0, 2, 3]:
                    tabla_frame.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(chart_frame, text="No hay datos de productos disponibles",
                        bg='#2a2a4e', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True)
                
        except Exception as e:
            tk.Label(chart_frame, text=f"Error al cargar productos: {str(e)}",
                    bg='#2a2a4e', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)
    
    def crear_pestaña_ventas(self):
        """Crear pestaña de reportes de ventas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="[VENT] Ventas")
        
        # Contenido principal
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(main_content, text="[ANLSS] Análisis de Ventas", 
                font=("Segoe UI", 18, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Filtros de fecha
        self.crear_filtros_fecha(main_content)
        
        # Reportes de ventas
        self.crear_tabla_ventas_detallada(main_content)
    
    def crear_filtros_fecha(self, parent):
        """Crear filtros de fecha"""
        filtros_frame = tk.LabelFrame(parent, text="[DATE] Filtros de Fecha", 
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
        tabla_frame = tk.LabelFrame(parent, text="[DETAIL] Ventas Detalladas", 
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
        
        # Grid - Corregir geometry manager
        self.tree_ventas.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        # Configurar expansión
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        
        # Cargar datos iniciales
        self.cargar_ventas_tabla()
    
    def crear_pestaña_productos(self):
        """Crear pestaña de reportes de productos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="[PROD] Productos")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="[INV] Análisis de Inventario", 
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
                    'icono': '[BOX]',
                    'descripcion': 'En inventario'
                },
                {
                    'titulo': 'Valor Inventario',
                    'valor': f"${resumen_productos.get('valor_total', 0):,.0f}",
                    'color': '#27ae60',
                    'icono': '[VALUE]',
                    'descripcion': 'Valor total'
                },
                {
                    'titulo': 'Stock Bajo',
                    'valor': f"{resumen_productos.get('productos_bajo_stock', 0):,}",
                    'color': '#e74c3c',
                    'icono': '[ALERT]',
                    'descripcion': 'Requieren atención'
                }
            ]
            
            for i, metrica in enumerate(metricas_productos):
                self.crear_card_metrica(cards_frame, metrica, i)
                
        except Exception as e:
            tk.Label(cards_frame, text=f"Error al cargar métricas de productos: {str(e)}", 
                    bg='#f8f9fa', fg='#e74c3c').pack()
    
    def crear_tabla_bajo_stock(self, parent):
        """Crear tabla de productos con bajo stock"""
        tabla_frame = tk.LabelFrame(parent, text="[ALERT] Productos con Stock Bajo", 
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
                tk.Label(tabla_frame, text="[OK] Todos los productos tienen stock suficiente", 
                        bg='white', fg='#27ae60', font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)
                
        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar productos: {str(e)}", 
                    bg='white', fg='#e74c3c').pack(expand=True)
    
    def crear_pestaña_clientes(self):
        """Crear pestaña de reportes de clientes"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="[CLNT] Clientes")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="[CLNT] Análisis de Clientes", 
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
                    'icono': '[USERS]',
                    'descripcion': 'Registrados'
                },
                {
                    'titulo': 'Clientes Activos',
                    'valor': f"{resumen_clientes.get('clientes_activos', 0):,}",
                    'color': '#27ae60',
                    'icono': '[OK]',
                    'descripcion': 'Con compras'
                },
                {
                    'titulo': 'Cliente Top',
                    'valor': f"${resumen_clientes.get('mayor_compra', 0):,.0f}",
                    'color': '#f39c12',
                    'icono': '[TOP]',
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
        tabla_frame = tk.LabelFrame(parent, text="[TOP10] Top 10 Clientes", 
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
        self.notebook.add(frame, text="[FIN] Financiero")
        
        main_content = tk.Frame(frame, bg='#f8f9fa')
        main_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_content, text="[FIN] Análisis Financiero", 
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
                    'icono': '[MONEY]',
                    'descripcion': 'Ventas totales'
                },
                {
                    'titulo': 'Cuentas por Cobrar',
                    'valor': f"${resumen_financiero.get('cuentas_cobrar', 0):,.0f}",
                    'color': '#e74c3c',
                    'icono': '[LIST]',
                    'descripcion': 'Pendiente de cobro'
                },
                {
                    'titulo': 'Promedio Venta',
                    'valor': f"${resumen_financiero.get('promedio_venta', 0):,.0f}",
                    'color': '#3498db',
                    'icono': '[CHART]',
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
        tabla_frame = tk.LabelFrame(parent, text="[DEBT] Cuentas por Cobrar", 
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
                tk.Label(tabla_frame, text="[OK] No hay cuentas pendientes por cobrar", 
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
    
    def crear_filtros_fecha_moderno(self, parent):
        """Crear filtros de fecha con diseño moderno"""
        filtros_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        filtros_frame.pack(fill='x', pady=(0, 20), padx=10)

        # Header del frame
        header_filtros = tk.Frame(filtros_frame, bg='#4ecdc4', height=40)
        header_filtros.pack(fill='x')
        header_filtros.pack_propagate(False)

        tk.Label(header_filtros, text="📅 FILTROS DE FECHA",
                font=("Segoe UI", 12, "bold"), bg='#4ecdc4', fg='white').pack(expand=True)

        # Contenido
        content = tk.Frame(filtros_frame, bg='#2a2a4e')
        content.pack(fill='x', padx=20, pady=15)

        # Variables de fecha
        self.fecha_inicio_var = tk.StringVar()
        self.fecha_fin_var = tk.StringVar()

        # Primera fila - Campos de fecha
        fecha_frame = tk.Frame(content, bg='#2a2a4e')
        fecha_frame.pack(fill='x', pady=(0, 10))

        # Desde
        tk.Label(fecha_frame, text="Desde:", font=("Segoe UI", 10, "bold"),
                bg='#2a2a4e', fg='#a8dadc').grid(row=0, column=0, sticky='w', padx=(0, 10))

        fecha_inicio_entry = tk.Entry(fecha_frame, textvariable=self.fecha_inicio_var,
                                     font=("Segoe UI", 10), width=12, bg='#1a1a2e', fg='white',
                                     insertbackground='white', relief='flat', bd=5)
        fecha_inicio_entry.grid(row=0, column=1, padx=(0, 20))

        # Hasta
        tk.Label(fecha_frame, text="Hasta:", font=("Segoe UI", 10, "bold"),
                bg='#2a2a4e', fg='#a8dadc').grid(row=0, column=2, sticky='w', padx=(0, 10))

        fecha_fin_entry = tk.Entry(fecha_frame, textvariable=self.fecha_fin_var,
                                  font=("Segoe UI", 10), width=12, bg='#1a1a2e', fg='white',
                                  insertbackground='white', relief='flat', bd=5)
        fecha_fin_entry.grid(row=0, column=3, padx=(0, 20))

        # Segunda fila - Botones
        botones_frame = tk.Frame(content, bg='#2a2a4e')
        botones_frame.pack(fill='x')

        btn_style = {'font': ('Segoe UI', 9, 'bold'), 'relief': 'flat',
                    'cursor': 'hand2', 'padx': 12, 'pady': 6, 'bd': 0}

        tk.Button(botones_frame, text="Hoy", bg='#3498db', fg='white',
                 command=self.filtro_hoy, **btn_style).pack(side='left', padx=2)

        tk.Button(botones_frame, text="Esta Semana", bg='#27ae60', fg='white',
                 command=self.filtro_semana, **btn_style).pack(side='left', padx=2)

        tk.Button(botones_frame, text="Este Mes", bg='#9b59b6', fg='white',
                 command=self.filtro_mes, **btn_style).pack(side='left', padx=2)

        tk.Button(botones_frame, text="🔍 Aplicar Filtro", bg='#e67e22', fg='white',
                 command=self.aplicar_filtro_fecha, **btn_style).pack(side='right', padx=(20, 0))

        # Establecer fechas por defecto
        self.filtro_mes()

    def crear_tabla_ventas_detallada_moderna(self, parent):
        """Crear tabla detallada de ventas con diseño moderno"""
        tabla_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        tabla_frame.pack(fill='both', expand=True, padx=10)

        # Header
        header_tabla = tk.Frame(tabla_frame, bg='#ff6b6b', height=40)
        header_tabla.pack(fill='x')
        header_tabla.pack_propagate(False)

        tk.Label(header_tabla, text="💰 VENTAS DETALLADAS",
                font=("Segoe UI", 12, "bold"), bg='#ff6b6b', fg='white').pack(expand=True)

        # Contenedor de la tabla
        tabla_container = tk.Frame(tabla_frame, bg='#2a2a4e')
        tabla_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Configurar estilo del Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.Treeview',
                       background='#1a1a2e',
                       foreground='white',
                       fieldbackground='#1a1a2e',
                       borderwidth=0)
        style.configure('Modern.Treeview.Heading',
                       background='#4ecdc4',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))

        # Treeview
        columns = ('fecha', 'cliente', 'productos', 'total')
        self.tree_ventas = ttk.Treeview(tabla_container, columns=columns, show='headings',
                                       height=15, style='Modern.Treeview')

        # Headers
        self.tree_ventas.heading('fecha', text='📅 Fecha')
        self.tree_ventas.heading('cliente', text='👤 Cliente')
        self.tree_ventas.heading('productos', text='📦 Productos')
        self.tree_ventas.heading('total', text='💰 Total')

        # Columnas
        self.tree_ventas.column('fecha', width=120, anchor='center')
        self.tree_ventas.column('cliente', width=200, anchor='w')
        self.tree_ventas.column('productos', width=150, anchor='center')
        self.tree_ventas.column('total', width=120, anchor='e')

        # Scrollbars con estilo
        v_scrollbar = ttk.Scrollbar(tabla_container, orient='vertical', command=self.tree_ventas.yview)
        h_scrollbar = ttk.Scrollbar(tabla_container, orient='horizontal', command=self.tree_ventas.xview)
        self.tree_ventas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid
        self.tree_ventas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Configurar expansión
        tabla_container.grid_rowconfigure(0, weight=1)
        tabla_container.grid_columnconfigure(0, weight=1)

        # Cargar datos iniciales
        self.cargar_ventas_tabla()

    def crear_cards_productos_modernas(self, parent):
        """Crear cards de métricas de productos con diseño moderno"""
        cards_frame = tk.Frame(parent, bg='#1a1a2e')
        cards_frame.pack(fill='x', pady=(0, 20))

        try:
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
                    'icono': '💰',
                    'descripcion': 'Valor total'
                },
                {
                    'titulo': 'Stock Bajo',
                    'valor': f"{resumen_productos.get('productos_bajo_stock', 0):,}",
                    'color': '#e74c3c',
                    'icono': '⚠️',
                    'descripcion': 'Requieren atención'
                }
            ]

            for i, metrica in enumerate(metricas_productos):
                self.crear_card_metrica_moderna(cards_frame, metrica, i)

        except Exception as e:
            tk.Label(cards_frame, text=f"Error al cargar métricas de productos: {str(e)}",
                    bg='#1a1a2e', fg='#e74c3c', font=("Segoe UI", 12)).pack()

    def crear_tabla_bajo_stock_moderna(self, parent):
        """Crear tabla de productos con bajo stock moderna"""
        tabla_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        tabla_frame.pack(fill='both', expand=True, padx=10)

        # Header
        header = tk.Frame(tabla_frame, bg='#e74c3c', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="⚠️ PRODUCTOS CON STOCK BAJO",
                font=("Segoe UI", 12, "bold"), bg='#e74c3c', fg='white').pack(expand=True)

        try:
            productos_bajo_stock = self.controller.obtener_productos_bajo_stock()

            if productos_bajo_stock:
                # Contenedor de tabla
                tabla_container = tk.Frame(tabla_frame, bg='#2a2a4e')
                tabla_container.pack(fill='both', expand=True, padx=10, pady=10)

                # Headers
                headers = ['Producto', 'Stock Actual', 'Stock Mínimo', 'Estado']
                for i, header_text in enumerate(headers):
                    tk.Label(tabla_container, text=header_text, font=("Segoe UI", 11, "bold"),
                            bg='#e74c3c', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')

                # Datos
                for i, producto in enumerate(productos_bajo_stock, 1):
                    nombre = producto[0]
                    stock_actual = producto[1]
                    stock_minimo = producto[2]
                    estado = "CRÍTICO" if stock_actual == 0 else "BAJO"

                    color_fila = '#ffebee' if estado == "CRÍTICO" else '#fff3e0'

                    tk.Label(tabla_container, text=nombre, bg=color_fila,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_container, text=f"{stock_actual:,}", bg=color_fila,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(tabla_container, text=f"{stock_minimo:,}", bg=color_fila,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_container, text=estado, bg=color_fila,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8,
                            fg='#c0392b' if estado == "CRÍTICO" else '#e67e22').grid(row=i, column=3, sticky='ew')

                # Configurar grid
                for i in range(4):
                    tabla_container.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(tabla_frame, text="✅ Todos los productos tienen stock suficiente",
                        bg='#2a2a4e', fg='#27ae60', font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)

        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar productos: {str(e)}",
                    bg='#2a2a4e', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)

    def crear_metricas_clientes_modernas(self, parent):
        """Crear métricas de clientes con diseño moderno"""
        metrics_frame = tk.Frame(parent, bg='#1a1a2e')
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
                self.crear_card_metrica_moderna(metrics_frame, metrica, i)

        except Exception as e:
            tk.Label(metrics_frame, text=f"Error al cargar métricas: {str(e)}",
                    bg='#1a1a2e', fg='#e74c3c', font=("Segoe UI", 12)).pack()

    def crear_tabla_top_clientes_moderna(self, parent):
        """Crear tabla de top clientes moderna"""
        tabla_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        tabla_frame.pack(fill='both', expand=True, padx=10)

        # Header
        header = tk.Frame(tabla_frame, bg='#f39c12', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="🏆 TOP 10 CLIENTES",
                font=("Segoe UI", 12, "bold"), bg='#f39c12', fg='white').pack(expand=True)

        try:
            top_clientes = self.controller.obtener_top_clientes(10)

            if top_clientes:
                # Contenedor de tabla
                tabla_container = tk.Frame(tabla_frame, bg='#2a2a4e')
                tabla_container.pack(fill='both', expand=True, padx=10, pady=10)

                # Headers
                headers = ['#', 'Cliente', 'Total Compras', 'Última Compra']
                for i, header_text in enumerate(headers):
                    tk.Label(tabla_container, text=header_text, font=("Segoe UI", 11, "bold"),
                            bg='#f39c12', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')

                # Datos
                for i, cliente in enumerate(top_clientes, 1):
                    nombre = f"{cliente[0]} {cliente[1]}"
                    total = cliente[2]
                    ultima_compra = cliente[3] if cliente[3] else "N/A"

                    color_fila = '#fff8e1' if i <= 3 else ('#2a2a4e' if i % 2 == 0 else '#1e1e3f')
                    text_color = '#333' if i <= 3 else '#ffffff'

                    tk.Label(tabla_container, text=f"{i}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=0, sticky='ew')
                    tk.Label(tabla_container, text=nombre, bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='w')
                    tk.Label(tabla_container, text=f"${total:,.0f}", bg=color_fila, fg=text_color,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_container, text=ultima_compra[:10] if ultima_compra != "N/A" else "N/A",
                            bg=color_fila, fg=text_color, font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=3, sticky='ew')

                # Configurar grid
                tabla_container.grid_columnconfigure(1, weight=2)
                for i in [0, 2, 3]:
                    tabla_container.grid_columnconfigure(i, weight=1)
            else:
                tk.Label(tabla_frame, text="No hay datos de clientes disponibles",
                        bg='#2a2a4e', fg='#7f8c8d', font=("Segoe UI", 12)).pack(expand=True, pady=40)

        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar clientes: {str(e)}",
                    bg='#2a2a4e', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)

    def crear_metricas_financieras_modernas(self, parent):
        """Crear métricas financieras modernas"""
        metrics_frame = tk.Frame(parent, bg='#1a1a2e')
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
                    'icono': '📈',
                    'descripcion': 'Por transacción'
                }
            ]

            for i, metrica in enumerate(metricas):
                self.crear_card_metrica_moderna(metrics_frame, metrica, i)

        except Exception as e:
            tk.Label(metrics_frame, text=f"Error al cargar métricas financieras: {str(e)}",
                    bg='#1a1a2e', fg='#e74c3c', font=("Segoe UI", 12)).pack()

    def crear_analisis_cuentas_cobrar_moderno(self, parent):
        """Crear análisis de cuentas por cobrar moderno"""
        tabla_frame = tk.Frame(parent, bg='#2a2a4e', relief='flat')
        tabla_frame.pack(fill='both', expand=True, padx=10)

        # Header
        header = tk.Frame(tabla_frame, bg='#e74c3c', height=40)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="📋 CUENTAS POR COBRAR",
                font=("Segoe UI", 12, "bold"), bg='#e74c3c', fg='white').pack(expand=True)

        try:
            cuentas_cobrar = self.controller.obtener_cuentas_por_cobrar()

            if cuentas_cobrar:
                # Contenedor de tabla
                tabla_container = tk.Frame(tabla_frame, bg='#2a2a4e')
                tabla_container.pack(fill='both', expand=True, padx=10, pady=10)

                # Headers
                headers = ['Cliente', 'Deuda Total', 'Saldo Pendiente', 'Estado']
                for i, header_text in enumerate(headers):
                    tk.Label(tabla_container, text=header_text, font=("Segoe UI", 11, "bold"),
                            bg='#e74c3c', fg='white', relief='flat', padx=15, pady=10).grid(row=0, column=i, sticky='ew')

                # Datos
                total_pendiente = 0
                for i, cuenta in enumerate(cuentas_cobrar, 1):
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

                    tk.Label(tabla_container, text=cliente, bg=color_fila,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=0, sticky='w')
                    tk.Label(tabla_container, text=f"${deuda_total:,.0f}", bg=color_fila,
                            font=("Segoe UI", 10), padx=15, pady=8).grid(row=i, column=1, sticky='ew')
                    tk.Label(tabla_container, text=f"${saldo_pendiente:,.0f}", bg=color_fila,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8).grid(row=i, column=2, sticky='ew')
                    tk.Label(tabla_container, text=estado, bg=color_fila,
                            font=("Segoe UI", 10, "bold"), padx=15, pady=8, fg=color_estado).grid(row=i, column=3, sticky='ew')

                # Configurar grid
                for i in range(4):
                    tabla_container.grid_columnconfigure(i, weight=1)

                # Total
                total_frame = tk.Frame(tabla_frame, bg='#2c3e50')
                total_frame.pack(fill='x', padx=10, pady=(0, 10))

                tk.Label(total_frame, text=f"TOTAL PENDIENTE: ${total_pendiente:,.0f}",
                        font=("Segoe UI", 12, "bold"), bg='#2c3e50', fg='white', pady=10).pack()
            else:
                tk.Label(tabla_frame, text="✅ No hay cuentas pendientes por cobrar",
                        bg='#2a2a4e', fg='#27ae60', font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)

        except Exception as e:
            tk.Label(tabla_frame, text=f"Error al cargar cuentas por cobrar: {str(e)}",
                    bg='#2a2a4e', fg='#e74c3c', font=("Segoe UI", 12)).pack(expand=True)

    def crear_card_metrica_moderna(self, parent, metrica, index):
        """Crear una card individual de métrica moderna"""
        # Card container
        card = tk.Frame(parent, bg='#2a2a4e', relief='flat', bd=0)
        card.grid(row=0, column=index, padx=10, pady=10, sticky='ew')

        # Configurar grid
        parent.grid_columnconfigure(index, weight=1)

        # Contenido de la card
        content_frame = tk.Frame(card, bg='#2a2a4e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con color
        header_frame = tk.Frame(content_frame, bg=metrica['color'], height=5)
        header_frame.pack(fill='x', pady=(0, 15))

        # Ícono y título
        title_frame = tk.Frame(content_frame, bg='#2a2a4e')
        title_frame.pack(fill='x')

        tk.Label(title_frame, text=metrica['icono'],
                font=("Segoe UI", 20), bg='#2a2a4e').pack(side='left')

        tk.Label(title_frame, text=metrica['titulo'],
                font=("Segoe UI", 12, "bold"), bg='#2a2a4e', fg='#a8dadc').pack(side='left', padx=(10, 0))

        # Valor principal
        tk.Label(content_frame, text=metrica['valor'],
                font=("Segoe UI", 24, "bold"), bg='#2a2a4e', fg=metrica['color']).pack(anchor='w', pady=(10, 0))

        # Descripción
        tk.Label(content_frame, text=metrica['descripcion'],
                font=("Segoe UI", 10), bg='#2a2a4e', fg='#95a5a6').pack(anchor='w', pady=(5, 0))

    def crear_card_metrica_moderna_dashboard(self, parent, metrica, index):
        """Crear una card individual de métrica moderna para dashboard"""
        # Card container con estilo dashboard
        card = tk.Frame(parent, bg='#2a2a4e', relief='flat', bd=0)
        card.grid(row=0, column=index, padx=15, pady=10, sticky='ew')

        # Configurar grid
        parent.grid_columnconfigure(index, weight=1)

        # Contenido de la card
        content_frame = tk.Frame(card, bg='#2a2a4e')
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)

        # Header con color
        header_frame = tk.Frame(content_frame, bg=metrica['color'], height=8)
        header_frame.pack(fill='x', pady=(0, 20))

        # Ícono grande y título
        title_frame = tk.Frame(content_frame, bg='#2a2a4e')
        title_frame.pack(fill='x')

        tk.Label(title_frame, text=metrica['icono'],
                font=("Segoe UI", 28), bg='#2a2a4e').pack(side='left')

        tk.Label(title_frame, text=metrica['titulo'],
                font=("Segoe UI", 14, "bold"), bg='#2a2a4e', fg='#ffffff').pack(side='left', padx=(15, 0))

        # Valor principal destacado
        tk.Label(content_frame, text=metrica['valor'],
                font=("Segoe UI", 32, "bold"), bg='#2a2a4e', fg=metrica['color']).pack(anchor='w', pady=(15, 0))

        # Descripción
        tk.Label(content_frame, text=metrica['descripcion'],
                font=("Segoe UI", 11), bg='#2a2a4e', fg='#a8dadc').pack(anchor='w', pady=(8, 0))

    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()