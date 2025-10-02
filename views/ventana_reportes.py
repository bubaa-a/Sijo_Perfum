"""
Ventana para gestión de reportes - Diseño Moderno con CustomTkinter
Versión con estilos unificados
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.reporte_controller import ReporteController
from datetime import datetime, timedelta
from config.estilos import (Colores, Fuentes, Espaciado, Dimensiones,
                            Iconos, obtener_color_hover)

class VentanaReportes:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ReporteController()
        self.ventana = None
        self.crear_ventana()

    def crear_ventana(self):
        """Crear ventana de reportes con diseño moderno"""
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("📊 Reportes y Análisis - Sistema Pro")
        self.ventana.geometry("1650x950")
        self.ventana.configure(bg=Colores.BG_PRIMARY)

        # Modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Crear interfaz
        self.crear_header()
        self.crear_contenido_principal()

    def crear_header(self):
        """Crear header moderno"""
        header = ctk.CTkFrame(
            self.ventana,
            fg_color=(Colores.PRIMARY_START, Colores.PRIMARY_END),
            height=Dimensiones.HEADER_HEIGHT,
            corner_radius=0
        )
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Título izquierdo
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky='w', padx=Espaciado.XXL, pady=Espaciado.MEDIO)

        ctk.CTkLabel(
            title_frame,
            text=f"{Iconos.REPORTES} CENTRO DE REPORTES",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(anchor='w')

        ctk.CTkLabel(
            title_frame,
            text="Análisis e inteligencia de negocios",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
            text_color='#e8eaf6'
        ).pack(anchor='w', pady=(3, 0))

        # Botones derecha
        botones_frame = ctk.CTkFrame(header, fg_color="transparent")
        botones_frame.grid(row=0, column=1, sticky='e', padx=Espaciado.XXL, pady=Espaciado.MEDIO)

        botones = [
            (f"{Iconos.ACTUALIZAR} Actualizar", Colores.ACTIVO, self.actualizar_reportes),
            (f"{Iconos.EXPORTAR} Exportar", Colores.WARNING, self.exportar_reportes),
            (f"{Iconos.CERRAR} Cerrar", Colores.DANGER, self.cerrar_ventana)
        ]

        for texto, color, comando in botones:
            btn = ctk.CTkButton(
                botones_frame,
                text=texto,
                fg_color=color,
                hover_color=obtener_color_hover(color),
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.BOLD),
                width=130,
                height=Dimensiones.BUTTON_HEIGHT_NORMAL,
                corner_radius=Dimensiones.RADIUS_NORMAL,
                command=comando
            )
            btn.pack(side='left', padx=Espaciado.MUY_PEQUENO)

    def darken_color(self, color):
        """Oscurecer color para hover"""
        colors = {
            '#10ac84': '#0e9670',
            '#f39c12': '#e67e22',
            '#ff3838': '#e62020'
        }
        return colors.get(color, color)

    def crear_contenido_principal(self):
        """Crear contenido principal con pestañas personalizadas"""
        main_container = ctk.CTkFrame(self.ventana, fg_color='#f0f2f5', corner_radius=0)
        main_container.grid(row=1, column=0, sticky='nsew', padx=25, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Frame para botones de pestañas
        tabs_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        tabs_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(0, 10))

        # Frame para contenido
        self.content_frame = ctk.CTkFrame(main_container, fg_color='white', corner_radius=12)
        self.content_frame.grid(row=1, column=0, sticky='nsew')
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Variable para pestaña activa
        self.pestana_activa = None

        # Crear botones de pestañas con bordes redondeados
        pestanas = [
            ("🏠 Dashboard", self.mostrar_dashboard),
            ("💰 Ventas", self.mostrar_ventas),
            ("📦 Productos", self.mostrar_productos),
            ("👥 Clientes", self.mostrar_clientes),
            ("💳 Financiero", self.mostrar_financiero)
        ]

        self.botones_pestanas = {}
        for i, (texto, comando) in enumerate(pestanas):
            btn = ctk.CTkButton(
                tabs_frame,
                text=texto,
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
                fg_color='#e9ecef',
                text_color='#2c3e50',
                hover_color='#dee2e6',
                corner_radius=12,
                height=40,
                width=140,
                command=lambda cmd=comando, t=texto: self.cambiar_pestana(cmd, t)
            )
            btn.pack(side='left', padx=5)
            self.botones_pestanas[texto] = btn

        # Mostrar dashboard por defecto
        self.cambiar_pestana(self.mostrar_dashboard, "🏠 Dashboard")

    def cambiar_pestana(self, comando, texto):
        """Cambiar de pestaña y actualizar estilos"""
        # Resetear todos los botones
        for nombre, boton in self.botones_pestanas.items():
            if nombre == texto:
                boton.configure(fg_color='#3498db', text_color='#ffffff')
            else:
                boton.configure(fg_color='#e9ecef', text_color='#2c3e50')

        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Mostrar nuevo contenido
        comando()

    def mostrar_dashboard(self):
        """Mostrar pestaña dashboard"""
        self.crear_pestana_dashboard()

    def mostrar_ventas(self):
        """Mostrar pestaña ventas"""
        self.crear_pestana_ventas()

    def mostrar_productos(self):
        """Mostrar pestaña productos"""
        self.crear_pestana_productos()

    def mostrar_clientes(self):
        """Mostrar pestaña clientes"""
        self.crear_pestana_clientes()

    def mostrar_financiero(self):
        """Mostrar pestaña financiero"""
        self.crear_pestana_financiero()

    def crear_pestana_dashboard(self):
        """Crear pestaña dashboard principal"""
        frame = ctk.CTkFrame(self.content_frame, fg_color='white', corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew')

        # Scroll container
        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Métricas principales
        self.crear_metricas_dashboard(scrollable_frame)

        # Gráficos
        self.crear_graficos_dashboard(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_metricas_dashboard(self, parent):
        """Crear métricas del dashboard"""
        metrics_container = ctk.CTkFrame(parent, fg_color='white')
        metrics_container.pack(fill='x', padx=30, pady=30)

        ctk.CTkLabel(metrics_container, text="📊 MÉTRICAS PRINCIPALES",
                    font=("Segoe UI", 16, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Grid de métricas
        cards_grid = ctk.CTkFrame(metrics_container, fg_color='white')
        cards_grid.pack(fill='x')

        try:
            resumen = self.controller.obtener_resumen_general()

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

            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(cards_grid, metrica, i)

        except Exception as e:
            ctk.CTkLabel(cards_grid,
                        text=f"Error al cargar métricas: {str(e)}",
                        text_color='#e74c3c',
                        font=("Segoe UI", 12)).pack(pady=20)

    def crear_card_metrica(self, parent, metrica, index):
        """Crear card individual de métrica"""
        card = ctk.CTkFrame(parent, fg_color='#ffffff', corner_radius=12,
                           border_width=2, border_color=metrica['color'])
        card.grid(row=0, column=index, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(index, weight=1)

        # Barra de color superior
        color_bar = ctk.CTkFrame(card, fg_color=metrica['color'], height=8, corner_radius=0)
        color_bar.pack(fill='x', padx=0, pady=0)

        # Contenido
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=15)

        # Icono y título
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x')

        ctk.CTkLabel(header, text=metrica['icono'],
                    font=("Segoe UI", 24)).pack(side='left')

        ctk.CTkLabel(header, text=metrica['titulo'],
                    font=("Segoe UI", 11, "bold"),
                    text_color='#2c3e50').pack(side='left', padx=(10, 0))

        # Valor
        ctk.CTkLabel(content, text=metrica['valor'],
                    font=("Segoe UI", 28, "bold"),
                    text_color=metrica['color']).pack(anchor='w', pady=(10, 5))

        # Descripción
        ctk.CTkLabel(content, text=metrica['descripcion'],
                    font=("Segoe UI", 10),
                    text_color='#7f8c8d').pack(anchor='w')

    def crear_graficos_dashboard(self, parent):
        """Crear sección de gráficos"""
        graficos_container = ctk.CTkFrame(parent, fg_color='white')
        graficos_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        ctk.CTkLabel(graficos_container, text="📈 ANÁLISIS VISUAL",
                    font=("Segoe UI", 16, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Ventas por mes
        self.crear_grafico_ventas_mes(graficos_container)

        # Productos más vendidos
        self.crear_grafico_productos_vendidos(graficos_container)

    def crear_grafico_ventas_mes(self, parent):
        """Crear gráfico de ventas por mes"""
        card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                           border_width=1, border_color='#e9ecef')
        card.pack(fill='x', pady=(0, 20))

        # Header
        header = ctk.CTkFrame(card, fg_color='#3498db', height=50, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="📅 VENTAS POR MES",
                    font=("Segoe UI", 13, "bold"),
                    text_color='white').pack(expand=True)

        try:
            datos_ventas = self.controller.obtener_ventas_por_mes()

            if datos_ventas:
                # Container tabla
                tabla_frame = tk.Frame(card, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

                # Estilo
                style = ttk.Style()
                style.configure("Dashboard.Treeview",
                               background="#ffffff",
                               foreground="#2c3e50",
                               fieldbackground="#ffffff",
                               font=("Segoe UI", 10),
                               rowheight=32)
                style.configure("Dashboard.Treeview.Heading",
                               background="#3498db",
                               foreground="white",
                               font=("Segoe UI", 11, "bold"))

                columns = ('mes', 'ventas', 'cantidad', 'promedio')
                tree = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                   height=8, style="Dashboard.Treeview")

                tree.heading('mes', text='Mes')
                tree.heading('ventas', text='Ventas')
                tree.heading('cantidad', text='Cantidad')
                tree.heading('promedio', text='Promedio')

                tree.column('mes', width=150, anchor='w')
                tree.column('ventas', width=120, anchor='center')
                tree.column('cantidad', width=100, anchor='center')
                tree.column('promedio', width=120, anchor='center')

                for fila in datos_ventas:
                    mes = fila[0]
                    ventas = fila[1]
                    cantidad = fila[2]
                    promedio = ventas / cantidad if cantidad > 0 else 0

                    tree.insert('', 'end', values=(
                        mes,
                        f"${ventas:,.0f}",
                        f"{cantidad:,}",
                        f"${promedio:,.0f}"
                    ))

                scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
            else:
                ctk.CTkLabel(card, text="No hay datos de ventas disponibles",
                            text_color='#6c757d',
                            font=("Segoe UI", 12)).pack(expand=True, pady=30)

        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {str(e)}",
                        text_color='#e74c3c',
                        font=("Segoe UI", 12)).pack(expand=True, pady=30)

    def crear_grafico_productos_vendidos(self, parent):
        """Crear gráfico de productos más vendidos"""
        card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                           border_width=1, border_color='#e9ecef')
        card.pack(fill='x')

        # Header
        header = ctk.CTkFrame(card, fg_color='#27ae60', height=50, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="🏆 PRODUCTOS MÁS VENDIDOS",
                    font=("Segoe UI", 13, "bold"),
                    text_color='white').pack(expand=True)

        try:
            productos = self.controller.obtener_productos_mas_vendidos(10)

            if productos:
                tabla_frame = tk.Frame(card, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

                style = ttk.Style()
                style.configure("Productos.Treeview",
                               background="#ffffff",
                               foreground="#2c3e50",
                               fieldbackground="#ffffff",
                               font=("Segoe UI", 10),
                               rowheight=32)
                style.configure("Productos.Treeview.Heading",
                               background="#27ae60",
                               foreground="white",
                               font=("Segoe UI", 11, "bold"))

                columns = ('rank', 'producto', 'cantidad', 'total')
                tree = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                   height=10, style="Productos.Treeview")

                tree.heading('rank', text='#')
                tree.heading('producto', text='Producto')
                tree.heading('cantidad', text='Cantidad')
                tree.heading('total', text='Total Ventas')

                tree.column('rank', width=50, anchor='center')
                tree.column('producto', width=300, anchor='w')
                tree.column('cantidad', width=100, anchor='center')
                tree.column('total', width=120, anchor='center')

                for i, producto in enumerate(productos, 1):
                    tree.insert('', 'end', values=(
                        f"{i}",
                        producto[0],
                        f"{producto[1]:,}",
                        f"${producto[2]:,.0f}"
                    ))

                scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
            else:
                ctk.CTkLabel(card, text="No hay datos de productos disponibles",
                            text_color='#6c757d',
                            font=("Segoe UI", 12)).pack(expand=True, pady=30)

        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {str(e)}",
                        text_color='#e74c3c',
                        font=("Segoe UI", 12)).pack(expand=True, pady=30)

    def crear_pestana_ventas(self):
        """Crear pestaña de ventas"""
        frame = ctk.CTkFrame(self.content_frame, fg_color='white', corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew')

        content = ctk.CTkFrame(frame, fg_color='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)

        # Título
        ctk.CTkLabel(content, text="Análisis de Ventas",
                    font=("Segoe UI", 18, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Filtros
        self.crear_filtros_fecha(content)

        # Tabla
        self.crear_tabla_ventas(content)

    def crear_filtros_fecha(self, parent):
        """Crear filtros de fecha"""
        filtros_card = ctk.CTkFrame(parent, fg_color='#f8f9fa', corner_radius=12,
                                   border_width=1, border_color='#e9ecef')
        filtros_card.pack(fill='x', pady=(0, 20))

        header = ctk.CTkFrame(filtros_card, fg_color='#667eea', height=45, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="📅 FILTROS DE FECHA",
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(expand=True)

        content = ctk.CTkFrame(filtros_card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=15)

        # Variables
        self.fecha_inicio_var = tk.StringVar()
        self.fecha_fin_var = tk.StringVar()

        # Grid
        fecha_grid = ctk.CTkFrame(content, fg_color='transparent')
        fecha_grid.pack(fill='x', pady=(0, 10))

        # Desde
        ctk.CTkLabel(fecha_grid, text="Desde:",
                    font=("Segoe UI", 10, "bold"),
                    text_color='#667eea').grid(row=0, column=0, sticky='w', padx=(0, 10))

        fecha_inicio = ctk.CTkEntry(fecha_grid, textvariable=self.fecha_inicio_var,
                                   width=120, height=32, corner_radius=8,
                                   border_width=1, border_color='#dee2e6')
        fecha_inicio.grid(row=0, column=1, padx=(0, 20))

        # Hasta
        ctk.CTkLabel(fecha_grid, text="Hasta:",
                    font=("Segoe UI", 10, "bold"),
                    text_color='#667eea').grid(row=0, column=2, sticky='w', padx=(0, 10))

        fecha_fin = ctk.CTkEntry(fecha_grid, textvariable=self.fecha_fin_var,
                                width=120, height=32, corner_radius=8,
                                border_width=1, border_color='#dee2e6')
        fecha_fin.grid(row=0, column=3)

        # Botones
        botones_frame = ctk.CTkFrame(content, fg_color='transparent')
        botones_frame.pack(fill='x')

        botones = [
            ("Hoy", '#3498db', self.filtro_hoy),
            ("Esta Semana", '#27ae60', self.filtro_semana),
            ("Este Mes", '#9b59b6', self.filtro_mes),
            ("🔍 Aplicar", '#e67e22', self.aplicar_filtro_fecha)
        ]

        for texto, color, comando in botones:
            btn = ctk.CTkButton(botones_frame, text=texto,
                               fg_color=color,
                               hover_color=self.darken_color(color),
                               font=("Segoe UI", 9, "bold"),
                               width=100, height=30,
                               corner_radius=8,
                               command=comando)
            btn.pack(side='left', padx=5)

        self.filtro_mes()

    def crear_tabla_ventas(self, parent):
        """Crear tabla de ventas"""
        tabla_card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                                 border_width=1, border_color='#e9ecef')
        tabla_card.pack(fill='both', expand=True)

        header = ctk.CTkFrame(tabla_card, fg_color='#667eea', height=45, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="💰 VENTAS DETALLADAS",
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(expand=True)

        tabla_frame = tk.Frame(tabla_card, bg='white')
        tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Ventas.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=32,
                       borderwidth=0)
        style.configure("Ventas.Treeview.Heading",
                       background="#2C3E50",
                       foreground="#FFFFFF",
                       font=("Segoe UI", 10, "bold"),
                       relief="solid",
                       borderwidth=1)

        # Deshabilitar efectos hover para mantener color permanente
        style.map("Ventas.Treeview.Heading",
                 background=[('active', '#2C3E50'), ('pressed', '#2C3E50'), ('!active', '#2C3E50')],
                 foreground=[('active', '#FFFFFF'), ('pressed', '#FFFFFF'), ('!active', '#FFFFFF')],
                 relief=[('active', 'solid'), ('pressed', 'solid')])

        columns = ('recibo', 'fecha', 'cliente', 'productos', 'total')
        self.tree_ventas = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                       style="Ventas.Treeview")

        self.tree_ventas.heading('recibo', text='🧾 Recibo')
        self.tree_ventas.heading('fecha', text='📅 Fecha')
        self.tree_ventas.heading('cliente', text='👤 Cliente')
        self.tree_ventas.heading('productos', text='📦 Productos')
        self.tree_ventas.heading('total', text='💰 Total')

        self.tree_ventas.column('recibo', width=150, anchor='center')
        self.tree_ventas.column('fecha', width=120, anchor='center')
        self.tree_ventas.column('cliente', width=200, anchor='w')
        self.tree_ventas.column('productos', width=120, anchor='center')
        self.tree_ventas.column('total', width=120, anchor='center')

        v_scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree_ventas.yview)
        h_scrollbar = ttk.Scrollbar(tabla_frame, orient='horizontal', command=self.tree_ventas.xview)
        self.tree_ventas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree_ventas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        self.cargar_ventas_tabla()

    def crear_pestana_productos(self):
        """Crear pestaña de productos"""
        frame = ctk.CTkFrame(self.content_frame, fg_color='white', corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew')

        content = ctk.CTkFrame(frame, fg_color='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Análisis de Inventario",
                    font=("Segoe UI", 18, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Métricas
        self.crear_metricas_productos(content)

        # Tabla bajo stock
        self.crear_tabla_bajo_stock(content)

    def crear_metricas_productos(self, parent):
        """Crear métricas de productos"""
        cards_frame = ctk.CTkFrame(parent, fg_color='white')
        cards_frame.pack(fill='x', pady=(0, 20))

        try:
            resumen = self.controller.obtener_resumen_productos()

            metricas = [
                {
                    'titulo': 'Total Productos',
                    'valor': f"{resumen.get('total_productos', 0):,}",
                    'color': '#3498db',
                    'icono': '📦',
                    'descripcion': 'En inventario'
                },
                {
                    'titulo': 'Valor Inventario',
                    'valor': f"${resumen.get('valor_total', 0):,.0f}",
                    'color': '#27ae60',
                    'icono': '💰',
                    'descripcion': 'Valor total'
                },
                {
                    'titulo': 'Stock Bajo',
                    'valor': f"{resumen.get('productos_bajo_stock', 0):,}",
                    'color': '#e74c3c',
                    'icono': '⚠️',
                    'descripcion': 'Requieren atención'
                }
            ]

            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(cards_frame, metrica, i)

        except Exception as e:
            ctk.CTkLabel(cards_frame, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack()

    def crear_tabla_bajo_stock(self, parent):
        """Crear tabla de productos con bajo stock"""
        card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                           border_width=1, border_color='#e9ecef')
        card.pack(fill='both', expand=True)

        header = ctk.CTkFrame(card, fg_color='#e74c3c', height=45, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="⚠️ PRODUCTOS CON STOCK BAJO",
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(expand=True)

        try:
            productos = self.controller.obtener_productos_bajo_stock()

            if productos:
                tabla_frame = tk.Frame(card, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

                style = ttk.Style()
                style.configure("Stock.Treeview",
                               background="#ffffff",
                               foreground="#2c3e50",
                               fieldbackground="#ffffff",
                               font=("Segoe UI", 10),
                               rowheight=32)
                style.configure("Stock.Treeview.Heading",
                               background="#e74c3c",
                               foreground="white",
                               font=("Segoe UI", 10, "bold"))

                columns = ('producto', 'stock', 'minimo', 'estado')
                tree = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                   style="Stock.Treeview")

                tree.heading('producto', text='Producto')
                tree.heading('stock', text='Stock Actual')
                tree.heading('minimo', text='Stock Mínimo')
                tree.heading('estado', text='Estado')

                tree.column('producto', width=300, anchor='w')
                tree.column('stock', width=120, anchor='center')
                tree.column('minimo', width=120, anchor='center')
                tree.column('estado', width=100, anchor='center')

                for producto in productos:
                    estado = "CRÍTICO" if producto[1] == 0 else "BAJO"
                    tree.insert('', 'end', values=(
                        producto[0],
                        f"{producto[1]:,}",
                        f"{producto[2]:,}",
                        estado
                    ))

                scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
            else:
                ctk.CTkLabel(card, text="✅ Todos los productos tienen stock suficiente",
                            text_color='#27ae60',
                            font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)

        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack(expand=True, pady=30)

    def crear_pestana_clientes(self):
        """Crear pestaña de clientes"""
        frame = ctk.CTkFrame(self.content_frame, fg_color='white', corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew')

        content = ctk.CTkFrame(frame, fg_color='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Análisis de Clientes",
                    font=("Segoe UI", 18, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Métricas
        self.crear_metricas_clientes(content)

        # Top clientes
        self.crear_tabla_top_clientes(content)

    def crear_metricas_clientes(self, parent):
        """Crear métricas de clientes"""
        cards_frame = ctk.CTkFrame(parent, fg_color='white')
        cards_frame.pack(fill='x', pady=(0, 20))

        try:
            resumen = self.controller.obtener_resumen_clientes()

            metricas = [
                {
                    'titulo': 'Total Clientes',
                    'valor': f"{resumen.get('total_clientes', 0):,}",
                    'color': '#9b59b6',
                    'icono': '👥',
                    'descripcion': 'Registrados'
                },
                {
                    'titulo': 'Clientes Activos',
                    'valor': f"{resumen.get('clientes_activos', 0):,}",
                    'color': '#27ae60',
                    'icono': '✅',
                    'descripcion': 'Con compras'
                },
                {
                    'titulo': 'Cliente Top',
                    'valor': f"${resumen.get('mayor_compra', 0):,.0f}",
                    'color': '#f39c12',
                    'icono': '🏆',
                    'descripcion': 'Mayor compra'
                }
            ]

            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(cards_frame, metrica, i)

        except Exception as e:
            ctk.CTkLabel(cards_frame, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack()

    def crear_tabla_top_clientes(self, parent):
        """Crear tabla de top clientes"""
        card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                           border_width=1, border_color='#e9ecef')
        card.pack(fill='both', expand=True)

        header = ctk.CTkFrame(card, fg_color='#f39c12', height=45, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="🏆 TOP 10 CLIENTES",
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(expand=True)

        try:
            clientes = self.controller.obtener_top_clientes(10)

            if clientes:
                tabla_frame = tk.Frame(card, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

                style = ttk.Style()
                style.configure("Clientes.Treeview",
                               background="#ffffff",
                               foreground="#2c3e50",
                               fieldbackground="#ffffff",
                               font=("Segoe UI", 10),
                               rowheight=32)
                style.configure("Clientes.Treeview.Heading",
                               background="#f39c12",
                               foreground="white",
                               font=("Segoe UI", 10, "bold"))

                columns = ('rank', 'cliente', 'total', 'ultima', 'recibo_venta', 'recibo_abono')
                tree = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                   style="Clientes.Treeview")

                tree.heading('rank', text='#')
                tree.heading('cliente', text='Cliente')
                tree.heading('total', text='Total Compras')
                tree.heading('ultima', text='Última Compra')
                tree.heading('recibo_venta', text='🧾 Recibo Venta')
                tree.heading('recibo_abono', text='🧾 Recibo Abono')

                tree.column('rank', width=50, anchor='center')
                tree.column('cliente', width=200, anchor='w')
                tree.column('total', width=120, anchor='center')
                tree.column('ultima', width=120, anchor='center')
                tree.column('recibo_venta', width=150, anchor='center')
                tree.column('recibo_abono', width=150, anchor='center')

                for i, cliente in enumerate(clientes, 1):
                    tree.insert('', 'end', values=(
                        f"{i}",
                        f"{cliente[0]} {cliente[1]}",
                        f"${cliente[2]:,.0f}",
                        cliente[3][:10] if cliente[3] else "N/A",
                        cliente[4] if cliente[4] else "Sin recibo",
                        cliente[5] if cliente[5] else "Sin abono"
                    ))

                scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
            else:
                ctk.CTkLabel(card, text="No hay datos de clientes disponibles",
                            text_color='#6c757d',
                            font=("Segoe UI", 12)).pack(expand=True, pady=40)

        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack(expand=True, pady=30)

    def crear_pestana_financiero(self):
        """Crear pestaña financiera"""
        frame = ctk.CTkFrame(self.content_frame, fg_color='white', corner_radius=0)
        frame.grid(row=0, column=0, sticky='nsew')

        content = ctk.CTkFrame(frame, fg_color='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Análisis Financiero",
                    font=("Segoe UI", 18, "bold"),
                    text_color='#2c3e50').pack(anchor='w', pady=(0, 20))

        # Métricas
        self.crear_metricas_financieras(content)

        # Cuentas por cobrar
        self.crear_tabla_cuentas_cobrar(content)

    def crear_metricas_financieras(self, parent):
        """Crear métricas financieras"""
        cards_frame = ctk.CTkFrame(parent, fg_color='white')
        cards_frame.pack(fill='x', pady=(0, 20))

        try:
            resumen = self.controller.obtener_resumen_financiero()

            metricas = [
                {
                    'titulo': 'Ingresos del Mes',
                    'valor': f"${resumen.get('ingresos_mes', 0):,.0f}",
                    'color': '#27ae60',
                    'icono': '💰',
                    'descripcion': 'Ventas totales'
                },
                {
                    'titulo': 'Cuentas por Cobrar',
                    'valor': f"${resumen.get('cuentas_cobrar', 0):,.0f}",
                    'color': '#e74c3c',
                    'icono': '📋',
                    'descripcion': 'Pendiente de cobro'
                },
                {
                    'titulo': 'Promedio Venta',
                    'valor': f"${resumen.get('promedio_venta', 0):,.0f}",
                    'color': '#3498db',
                    'icono': '📈',
                    'descripcion': 'Por transacción'
                }
            ]

            for i, metrica in enumerate(metricas):
                self.crear_card_metrica(cards_frame, metrica, i)

        except Exception as e:
            ctk.CTkLabel(cards_frame, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack()

    def crear_tabla_cuentas_cobrar(self, parent):
        """Crear tabla de cuentas por cobrar"""
        card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                           border_width=1, border_color='#e9ecef')
        card.pack(fill='both', expand=True)

        header = ctk.CTkFrame(card, fg_color='#e74c3c', height=45, corner_radius=10)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="📋 CUENTAS POR COBRAR",
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(expand=True)

        try:
            cuentas = self.controller.obtener_cuentas_por_cobrar()

            if cuentas:
                tabla_frame = tk.Frame(card, bg='white')
                tabla_frame.pack(fill='both', expand=True, padx=15, pady=15)

                style = ttk.Style()
                style.configure("Cuentas.Treeview",
                               background="#ffffff",
                               foreground="#2c3e50",
                               fieldbackground="#ffffff",
                               font=("Segoe UI", 10),
                               rowheight=32)
                style.configure("Cuentas.Treeview.Heading",
                               background="#e74c3c",
                               foreground="white",
                               font=("Segoe UI", 10, "bold"))

                columns = ('cliente', 'deuda', 'pendiente', 'estado')
                tree = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                   style="Cuentas.Treeview")

                tree.heading('cliente', text='Cliente')
                tree.heading('deuda', text='Deuda Total')
                tree.heading('pendiente', text='Saldo Pendiente')
                tree.heading('estado', text='Estado')

                tree.column('cliente', width=300, anchor='w')
                tree.column('deuda', width=120, anchor='center')
                tree.column('pendiente', width=150, anchor='center')
                tree.column('estado', width=100, anchor='center')

                total = 0
                for cuenta in cuentas:
                    pendiente = cuenta[4]
                    total += pendiente

                    if pendiente > 100000:
                        estado = "ALTA"
                    elif pendiente > 50000:
                        estado = "MEDIA"
                    else:
                        estado = "BAJA"

                    tree.insert('', 'end', values=(
                        f"{cuenta[1]} {cuenta[2]}",
                        f"${cuenta[3]:,.0f}",
                        f"${pendiente:,.0f}",
                        estado
                    ))

                scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')

                # Total
                total_frame = ctk.CTkFrame(card, fg_color='#2c3e50', corner_radius=8)
                total_frame.pack(fill='x', padx=15, pady=(0, 15))

                ctk.CTkLabel(total_frame, text=f"TOTAL PENDIENTE: ${total:,.0f}",
                            font=("Segoe UI", 12, "bold"),
                            text_color='white').pack(pady=12)
            else:
                ctk.CTkLabel(card, text="✅ No hay cuentas pendientes por cobrar",
                            text_color='#27ae60',
                            font=("Segoe UI", 14, "bold")).pack(expand=True, pady=40)

        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {str(e)}",
                        text_color='#e74c3c').pack(expand=True, pady=30)

    # Métodos auxiliares
    def filtro_hoy(self):
        """Filtro para hoy"""
        hoy = datetime.now()
        self.fecha_inicio_var.set(hoy.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(hoy.strftime('%Y-%m-%d'))

    def filtro_semana(self):
        """Filtro para esta semana"""
        hoy = datetime.now()
        inicio = hoy - timedelta(days=hoy.weekday())
        fin = inicio + timedelta(days=6)
        self.fecha_inicio_var.set(inicio.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(fin.strftime('%Y-%m-%d'))

    def filtro_mes(self):
        """Filtro para este mes"""
        hoy = datetime.now()
        inicio = hoy.replace(day=1)
        if hoy.month == 12:
            fin = hoy.replace(year=hoy.year+1, month=1, day=1) - timedelta(days=1)
        else:
            fin = hoy.replace(month=hoy.month+1, day=1) - timedelta(days=1)
        self.fecha_inicio_var.set(inicio.strftime('%Y-%m-%d'))
        self.fecha_fin_var.set(fin.strftime('%Y-%m-%d'))

    def aplicar_filtro_fecha(self):
        """Aplicar filtro de fechas"""
        try:
            inicio = self.fecha_inicio_var.get()
            fin = self.fecha_fin_var.get()

            if inicio and fin:
                self.cargar_ventas_tabla(inicio, fin)
                messagebox.showinfo("Filtro Aplicado",
                                   f"Mostrando datos desde {inicio} hasta {fin}")
            else:
                messagebox.showwarning("Advertencia", "Ingrese ambas fechas")

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro: {str(e)}")

    def cargar_ventas_tabla(self, inicio=None, fin=None):
        """Cargar ventas en la tabla"""
        try:
            for item in self.tree_ventas.get_children():
                self.tree_ventas.delete(item)

            if inicio and fin:
                ventas = self.controller.obtener_ventas_por_rango_fecha(inicio, fin)
            else:
                ventas = self.controller.obtener_ventas_recientes(50)

            for venta in ventas:
                self.tree_ventas.insert('', 'end', values=(
                    venta[0] if venta[0] else 'Sin recibo',
                    venta[1][:10] if venta[1] else 'N/A',
                    f"{venta[2]} {venta[3]}" if venta[2] else "Sin cliente",
                    f"{venta[4]} productos" if venta[4] else "0",
                    f"${venta[5]:,.0f}" if venta[5] else "$0"
                ))

        except Exception as e:
            print(f"Error al cargar ventas: {str(e)}")

    def actualizar_reportes(self):
        """Actualizar reportes"""
        try:
            self.cargar_ventas_tabla()
            messagebox.showinfo("Actualizado", "Reportes actualizados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")

    def exportar_reportes(self):
        """Exportar reportes"""
        messagebox.showinfo("Exportar", "Funcionalidad de exportación en desarrollo")

    def cerrar_ventana(self):
        """Cerrar ventana"""
        self.ventana.destroy()
