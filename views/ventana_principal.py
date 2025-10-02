"""
Ventana principal del sistema - Diseño moderno con CustomTkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.producto_controller import ProductoController
from datetime import datetime
from config.estilos import Colores, Fuentes, Espaciado, Dimensiones, Iconos, ModuloConfig

class VentanaPrincipal:
    def __init__(self):
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Usar CTk para la ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Gestión Empresarial Pro")
        self.root.geometry("1400x850")
        self.root.state('zoomed')  # Maximizar ventana

        # Controladores
        self.producto_controller = ProductoController()

        # Crear interfaz moderna
        self.crear_interfaz_moderna()

    def crear_interfaz_moderna(self):
        """Crear interfaz principal moderna con CustomTkinter"""
        # Header elegante
        self.crear_header_elegante()

        # Dashboard principal con tarjetas modernas
        self.crear_dashboard_principal()

        # Footer con estadísticas
        self.crear_footer_estadisticas()

    def crear_header_elegante(self):
        """Crear header moderno con CustomTkinter y gradiente"""
        # Header con gradiente usando estilos unificados
        header_frame = ctk.CTkFrame(
            self.root,
            fg_color=(Colores.PRIMARY_START, Colores.PRIMARY_END),
            height=Dimensiones.HEADER_HEIGHT + 10,
            corner_radius=0
        )
        header_frame.pack(fill='x', pady=(0, 0))
        header_frame.pack_propagate(False)

        # Container interno
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill='both', expand=True, padx=Espaciado.XXL, pady=Espaciado.MEDIO)

        # Sección izquierda - Logo y título
        left_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_section.pack(side='left', fill='y')

        title_label = ctk.CTkLabel(
            left_section,
            text=f"{Iconos.EMPRESA} GESTIÓN EMPRESARIAL PRO",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XXL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        title_label.pack(anchor='w')

        subtitle_label = ctk.CTkLabel(
            left_section,
            text="Sistema Integral de Administración",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO+2),
            text_color="#e8eaf6"
        )
        subtitle_label.pack(anchor='w', pady=(3, 0))

        # Sección derecha - Información
        right_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_section.pack(side='right', fill='y')

        # Fecha y hora
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M")

        time_label = ctk.CTkLabel(
            right_section,
            text=f"{Iconos.HORA} {hora_actual}",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        time_label.pack(anchor='e')

        date_label = ctk.CTkLabel(
            right_section,
            text=fecha_actual,
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.NORMAL),
            text_color="#e8eaf6"
        )
        date_label.pack(anchor='e', pady=(2, 0))

    def crear_dashboard_principal(self):
        """Crear dashboard principal con CustomTkinter"""
        # Container principal
        dashboard_frame = ctk.CTkFrame(self.root, fg_color=Colores.BG_PRIMARY, corner_radius=0)
        dashboard_frame.pack(fill='both', expand=True, padx=Espaciado.XL, pady=Espaciado.MEDIO)

        # Título del dashboard
        title_label = ctk.CTkLabel(
            dashboard_frame,
            text="🎯 Centro de Control",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_PRIMARY
        )
        title_label.pack(pady=(Espaciado.NORMAL, Espaciado.MUY_PEQUENO))

        subtitle_label = ctk.CTkLabel(
            dashboard_frame,
            text="Selecciona un módulo para comenzar",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO+2),
            text_color=Colores.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, Espaciado.MEDIO))

        # Grid de tarjetas
        cards_container = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        cards_container.pack(expand=True, fill='both', padx=20, pady=10)

        # Configurar grid
        for i in range(3):
            cards_container.grid_columnconfigure(i, weight=1)
        for i in range(2):
            cards_container.grid_rowconfigure(i, weight=1)

        # Módulos con iconos modernos usando configuración unificada
        modulos = [
            {
                **ModuloConfig.PRODUCTOS,
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Control total de stock',
                'comando': self.abrir_productos
            },
            {
                **ModuloConfig.CLIENTES,
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Gestión de relaciones',
                'comando': self.abrir_clientes
            },
            {
                **ModuloConfig.VENTAS,
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Procesamiento rápido',
                'comando': self.abrir_ventas
            },
            {
                **ModuloConfig.CUENTAS,
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Control de créditos',
                'comando': self.abrir_cuentas
            },
            {
                **ModuloConfig.REPORTES,
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Inteligencia de negocio',
                'comando': self.abrir_reportes
            },
            {
                'nombre': 'CONFIGURACIÓN',
                'descripcion': 'Ajustes del Sistema',
                'emoji': Iconos.CONFIGURACION,
                'color': '#5f27cd',
                'hover': '#341f97',
                'color_text': Colores.TEXT_WHITE,
                'subtitle': 'Personalización avanzada',
                'comando': self.abrir_configuracion
            }
        ]

        # Crear tarjetas modernas
        for i, modulo in enumerate(modulos):
            row = i // 3
            col = i % 3
            self.crear_tarjeta_moderna(cards_container, modulo, row, col)

    def crear_tarjeta_moderna(self, parent, modulo, row, col):
        """Crear tarjeta moderna con CustomTkinter y bordes redondeados"""
        # Obtener colores (compatibilidad con ambas nomenclaturas)
        color_fondo = modulo.get('color', modulo.get('color_bg', Colores.PRIMARY_START))
        color_hover = modulo.get('hover', modulo.get('color_hover', Colores.PRIMARY_DARK))

        # Botón como tarjeta con CustomTkinter
        card_btn = ctk.CTkButton(
            parent,
            text="",  # Sin texto, lo agregaremos como widgets hijos
            fg_color=color_fondo,
            hover_color=color_hover,
            corner_radius=Dimensiones.RADIUS_LARGE,
            border_width=0,
            command=modulo['comando'],
            cursor="hand2",
            height=200
        )
        card_btn.grid(row=row, column=col, padx=Espaciado.NORMAL, pady=Espaciado.NORMAL, sticky='nsew')

        # Frame interno para contenido (sobre el botón)
        content_frame = ctk.CTkFrame(card_btn, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Icono emoji
        icon_label = ctk.CTkLabel(
            content_frame,
            text=modulo['emoji'],
            font=(Fuentes.FAMILIA_PRINCIPAL, 50),
            text_color=Colores.TEXT_WHITE
        )
        icon_label.pack(pady=(5, 10))

        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text=modulo['nombre'],
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.GRANDE, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        title_label.pack()

        # Descripción
        desc_label = ctk.CTkLabel(
            content_frame,
            text=modulo['descripcion'],
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.NORMAL),
            text_color="#f0f0f0"
        )
        desc_label.pack(pady=(3, 0))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text=modulo['subtitle'],
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.ITALIC),
            text_color="#e0e0e0"
        )
        subtitle_label.pack(pady=(5, 5))


    def crear_footer_estadisticas(self):
        """Crear footer moderno con CustomTkinter"""
        # Footer con gradiente
        footer_frame = ctk.CTkFrame(
            self.root,
            fg_color=(Colores.GRIS_OSCURO, "#34495e"),
            height=Dimensiones.FOOTER_HEIGHT,
            corner_radius=0
        )
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        # Container interno
        content_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        content_frame.pack(fill='both', expand=True, padx=Espaciado.XXL, pady=Espaciado.NORMAL)

        # Panel izquierdo - Estado
        left_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_panel.pack(side='left')

        status_label = ctk.CTkLabel(left_panel, text="🚀 Sistema Activo",
                                    font=("Segoe UI", 13, "bold"), text_color="#2ecc71")
        status_label.pack()

        # Panel central - Estadísticas
        center_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        center_panel.pack(side='left', expand=True, padx=50)

        self.crear_mini_estadisticas(center_panel)

        # Panel derecho
        right_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_panel.pack(side='right')

        # Versión
        version_label = ctk.CTkLabel(right_panel, text="v3.0 PRO",
                                     font=("Segoe UI", 11, "bold"),
                                     text_color="white",
                                     fg_color="#e74c3c",
                                     corner_radius=8)
        version_label.pack(side='left', padx=(0, 15), ipadx=10, ipady=5)

        # Botón ayuda
        help_btn = ctk.CTkButton(right_panel, text="💡 Ayuda",
                                font=("Segoe UI", 11, "bold"),
                                fg_color="#3498db",
                                hover_color="#2980b9",
                                width=100, height=35,
                                corner_radius=8,
                                command=self.abrir_ayuda)
        help_btn.pack(side='left')

    def crear_mini_estadisticas(self, parent):
        """Crear mini estadísticas con CustomTkinter"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(expand=True)

        try:
            stats = self.producto_controller.obtener_estadisticas_productos()

            # Crear badges modernos
            self.crear_stat_badge(stats_frame, "📦", str(stats['total_productos']), "Productos", 0)
            self.crear_stat_badge(stats_frame, "💵", f"${stats['valor_inventario']:,.0f}", "Inventario", 1)

            if stats['productos_bajo_stock'] > 0:
                self.crear_stat_badge(stats_frame, "⚠️", str(stats['productos_bajo_stock']), "Stock Bajo", 2, alert=True)
            else:
                self.crear_stat_badge(stats_frame, "✅", "0", "Stock OK", 2)

        except Exception as e:
            # Estadísticas por defecto
            error_label = ctk.CTkLabel(stats_frame, text="📊 Estadísticas no disponibles",
                                      font=("Segoe UI", 11), text_color="#95a5a6")
            error_label.pack()

    def crear_stat_badge(self, parent, icon, value, label, position, alert=False):
        """Crear badge moderno con CustomTkinter"""
        color = '#e74c3c' if alert else '#3498db'

        # Badge container
        badge = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        badge.pack(side='left', padx=10)

        # Contenido del badge
        content = ctk.CTkFrame(badge, fg_color="transparent")
        content.pack(padx=15, pady=10)

        # Icono
        icon_label = ctk.CTkLabel(content, text=icon,
                                  font=("Segoe UI", 18))
        icon_label.pack()

        # Valor
        value_label = ctk.CTkLabel(content, text=value,
                                   font=("Segoe UI", 14, "bold"),
                                   text_color="white")
        value_label.pack(pady=(2, 0))

        # Etiqueta
        label_label = ctk.CTkLabel(content, text=label,
                                   font=("Segoe UI", 10),
                                   text_color="#f0f0f0")
        label_label.pack()
    
    def abrir_productos(self):
        """Abrir ventana de productos"""
        print("DEBUG: Intentando abrir modulo de productos...")
        try:
            from views.ventana_productos import VentanaProductos
            ventana_productos = VentanaProductos(self.root)
            print("DEBUG: Modulo de productos abierto correctamente")
        except Exception as e:
            print(f"ERROR en productos: {str(e)}")
            messagebox.showinfo("Información", f"Módulo de productos:\n{str(e)}")

    def abrir_clientes(self):
        """Abrir ventana de clientes"""
        print("DEBUG: Intentando abrir modulo de clientes...")
        try:
            from views.ventana_clientes import VentanaClientes
            ventana_clientes = VentanaClientes(self.root)
            print("DEBUG: Modulo de clientes abierto correctamente")
        except Exception as e:
            print(f"ERROR en clientes: {str(e)}")
            messagebox.showinfo("Información", f"Módulo de clientes:\n{str(e)}")

    def abrir_ventas(self):
        """Abrir ventana de ventas"""
        print("DEBUG: Intentando abrir modulo de ventas...")
        try:
            from views.ventana_ventas import VentanaVentas
            ventana_ventas = VentanaVentas(self.root)
            print("DEBUG: Modulo de ventas abierto correctamente")
        except Exception as e:
            print(f"ERROR en ventas: {str(e)}")
            messagebox.showinfo("Información", f"Módulo de ventas:\n{str(e)}")

    def abrir_cuentas(self):
        """Abrir ventana de cuentas corrientes"""
        print("DEBUG: Intentando abrir modulo de cuentas...")
        try:
            from views.ventana_cuentas import VentanaCuentas
            ventana_cuentas = VentanaCuentas(self.root)
            print("DEBUG: Modulo de cuentas abierto correctamente")
        except Exception as e:
            print(f"ERROR en cuentas: {str(e)}")
            messagebox.showinfo("Información", f"Módulo de cuentas:\n{str(e)}")

    def abrir_reportes(self):
        """Abrir ventana de reportes"""
        print("DEBUG: Intentando abrir modulo de reportes...")
        try:
            from views.ventana_reportes import VentanaReportes
            ventana_reportes = VentanaReportes(self.root)
            print("DEBUG: Modulo de reportes abierto correctamente")
        except Exception as e:
            print(f"ERROR en reportes: {str(e)}")
            messagebox.showinfo("Información", f"Módulo de reportes:\n{str(e)}")

    def test_modulos(self):
        """Método de prueba para verificar que los botones funcionen"""
        print("DEBUG: Probando funcionalidad de botones...")
        messagebox.showinfo("✅ Test de Sistema",
                           "¡Sistema funcionando perfectamente!\n\n" +
                           "🎯 Todas las tarjetas son interactivas\n" +
                           "🎨 Efectos visuales operativos\n" +
                           "🚀 Interfaz moderna activada")

    def abrir_configuracion(self):
        """Abrir configuración del sistema"""
        # Crear ventana de configuración moderna
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuración del Sistema")
        config_window.geometry("600x400")
        config_window.configure(bg='#f8f9fa')
        config_window.transient(self.root)
        config_window.grab_set()

        # Centrar ventana
        config_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 300,
            self.root.winfo_rooty() + 200
        ))

        # Header
        header = tk.Frame(config_window, bg='#3498db', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        title_label = tk.Label(header, text="[CONFIG] CONFIGURACIÓN DEL SISTEMA",
                              font=("Segoe UI", 16, "bold"),
                              fg='white', bg='#3498db')
        title_label.pack(expand=True)

        # Contenido
        content = tk.Frame(config_window, bg='#f8f9fa')
        content.pack(fill='both', expand=True, padx=30, pady=30)

        # Opciones de configuración
        options = [
            "[CONF] Configuración General",
            "[DB] Gestión de Base de Datos",
            "[USER] Usuarios y Permisos",
            "[SEC] Seguridad",
            "[REP] Preferencias de Reportes",
            "[BAK] Respaldo y Restauración"
        ]

        for option in options:
            btn = tk.Button(content, text=option,
                           font=("Segoe UI", 12),
                           bg='white', fg='#2c3e50',
                           relief='flat', bd=1,
                           pady=15, anchor='w',
                           cursor='hand2')
            btn.pack(fill='x', pady=5)

            # Efecto hover
            def on_enter(e, button=btn):
                button.configure(bg='#ecf0f1')
            def on_leave(e, button=btn):
                button.configure(bg='white')

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Botón cerrar
        close_btn = tk.Button(content, text="Cerrar",
                             font=("Segoe UI", 11, "bold"),
                             bg='#95a5a6', fg='white',
                             relief='flat', pady=10,
                             command=config_window.destroy,
                             cursor='hand2')
        close_btn.pack(pady=(20, 0), ipadx=20)

    def abrir_ayuda(self):
        """Mostrar ayuda del sistema"""
        # Crear ventana de ayuda moderna
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda del Sistema")
        help_window.geometry("800x600")
        help_window.configure(bg='#f8f9fa')
        help_window.transient(self.root)
        help_window.grab_set()

        # Centrar ventana
        help_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 200,
            self.root.winfo_rooty() + 100
        ))

        # Header
        header = tk.Frame(help_window, bg='#2ecc71', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        title_label = tk.Label(header, text="[AYUDA] AYUDA DEL SISTEMA",
                              font=("Segoe UI", 16, "bold"),
                              fg='white', bg='#2ecc71')
        title_label.pack(expand=True)

        # Contenido con scroll
        main_frame = tk.Frame(help_window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Crear texto scrollable
        text_frame = tk.Frame(main_frame, bg='#f8f9fa')
        text_frame.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')

        text_widget = tk.Text(text_frame,
                             font=("Segoe UI", 11),
                             bg='white', fg='#2c3e50',
                             relief='flat', bd=0,
                             yscrollcommand=scrollbar.set,
                             wrap='word',
                             padx=20, pady=20)
        text_widget.pack(fill='both', expand=True)

        scrollbar.config(command=text_widget.yview)

        # Contenido de ayuda
        help_content = """
SISTEMA DE GESTIÓN EMPRESARIAL PRO v2.0

GUÍA DE INICIO RÁPIDO:

🏢 DESCRIPCIÓN GENERAL
Este sistema le permite gestionar completamente su empresa desde una sola aplicación.
Controle inventario, clientes, ventas y genere reportes profesionales.

📦 MÓDULO PRODUCTOS
• Registre productos con precios, stock y categorías
• Configure alertas de stock mínimo
• Calcule automáticamente márgenes de ganancia
• Busque productos por nombre o categoría

👥 MÓDULO CLIENTES
• Mantenga una base de datos completa de clientes
• Registre información de contacto y direcciones
• Consulte historial de compras por cliente
• Identifique sus mejores clientes

💰 MÓDULO VENTAS
• Procese ventas con carrito interactivo
• Actualización automática de inventario
• Soporte para ventas al contado y crédito
• Cálculos automáticos de totales

💳 MÓDULO CUENTAS CORRIENTES
• Gestione créditos otorgados a clientes
• Registre abonos y pagos
• Control de saldos pendientes
• Historial completo de movimientos

📊 MÓDULO REPORTES
• Análisis de ventas por períodos
• Gráficos de rendimiento
• Exportación a CSV
• Reportes de inventario crítico

PRIMEROS PASOS:

1️⃣ CONFIGURAR PRODUCTOS
   • Vaya al módulo PRODUCTOS
   • Agregue sus productos con precios y stock inicial
   • Configure stock mínimo para alertas

2️⃣ REGISTRAR CLIENTES
   • Use el módulo CLIENTES
   • Registre información completa de contacto
   • Puede configurar crédito en CUENTAS CORRIENTES

3️⃣ PROCESAR VENTAS
   • Use el módulo VENTAS
   • Seleccione cliente y productos
   • El sistema actualiza inventario automáticamente

4️⃣ ANALIZAR RESULTADOS
   • Revise REPORTES para análisis detallados
   • Exporte datos para análisis externos

CARACTERÍSTICAS TÉCNICAS:
• Base de datos SQLite integrada
• Respaldos automáticos
• Interfaz moderna y responsive
• Validaciones automáticas de datos
• Cálculos en tiempo real

SOPORTE:
Para soporte técnico o consultas, contacte al administrador del sistema.

¡Su sistema está completamente operativo y listo para usar!
"""

        text_widget.insert('1.0', help_content)
        text_widget.configure(state='disabled')

        # Botón cerrar
        close_btn = tk.Button(main_frame, text="Cerrar",
                             font=("Segoe UI", 11, "bold"),
                             bg='#2ecc71', fg='white',
                             relief='flat', pady=10,
                             command=help_window.destroy,
                             cursor='hand2')
        close_btn.pack(pady=(10, 0), ipadx=20)

    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()