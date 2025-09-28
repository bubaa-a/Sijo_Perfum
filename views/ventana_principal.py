"""
Ventana principal del sistema
"""
import tkinter as tk
from tkinter import ttk
from controllers.producto_controller import ProductoController

class VentanaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Empresarial Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Controladores
        self.producto_controller = ProductoController()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Header
        self.crear_header()
        
        # Área principal
        self.crear_area_principal()
        
        # Footer con estadísticas
        self.crear_footer_estadisticas()
    
    def crear_header(self):
        """Crear el encabezado"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título principal
        titulo = tk.Label(header_frame, text="SISTEMA DE GESTIÓN EMPRESARIAL PRO", 
                         font=("Arial", 28, "bold"), fg='white', bg='#34495e')
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(header_frame, text="Gestiona tu inventario, clientes y ventas de forma profesional", 
                           font=("Arial", 14), fg='#bdc3c7', bg='#34495e')
        subtitulo.pack()
    
    def crear_area_principal(self):
        """Crear el área principal con los botones"""
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Frame para botones principales
        botones_frame = tk.Frame(main_frame, bg='#2c3e50')
        botones_frame.pack(expand=True)
        
        # Estilo para botones principales
        btn_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 18,
            'height': 4,
            'relief': 'raised',
            'bd': 5,
            'cursor': 'hand2'
        }
        
        # Primera fila de botones
        fila1 = tk.Frame(botones_frame, bg='#2c3e50')
        fila1.pack(pady=20)
        # Agregar después de la segunda fila de botones, antes de la tercera fila
        fila2_5 = tk.Frame(botones_frame, bg='#2c3e50')
        fila2_5.pack(pady=10)

        btn_cuentas = tk.Button(fila2_5, text="💰 CUENTAS\nCorrientes", 
                       bg='#8e44ad', fg='white', activebackground='#732d91',
                       command=self.abrir_cuentas, **btn_style)
        btn_cuentas.pack(side='left', padx=20)
        
        self.btn_productos = tk.Button(fila1, text="PRODUCTOS\nInventario", 
                                      bg='#3498db', fg='white', activebackground='#2980b9',
                                      command=self.abrir_productos, **btn_style)
        self.btn_productos.pack(side='left', padx=20)
        
        self.btn_clientes = tk.Button(fila1, text="CLIENTES\nBase de datos", 
                                     bg='#2ecc71', fg='white', activebackground='#27ae60',
                                     command=self.abrir_clientes, **btn_style)
        self.btn_clientes.pack(side='left', padx=20)
        
        # Segunda fila de botones
        fila2 = tk.Frame(botones_frame, bg='#2c3e50')
        fila2.pack(pady=20)
        
        self.btn_ventas = tk.Button(fila2, text="VENTAS\nProcesar", 
                                   bg='#e74c3c', fg='white', activebackground='#c0392b',
                                   command=self.abrir_ventas, **btn_style)
        self.btn_ventas.pack(side='left', padx=20)
        
        self.btn_reportes = tk.Button(fila2, text="REPORTES\nAnalíticas", 
                                     bg='#f39c12', fg='white', activebackground='#e67e22',
                                     command=self.abrir_reportes, **btn_style)
        self.btn_reportes.pack(side='left', padx=20)
        
        # Tercera fila - botones adicionales
        fila3 = tk.Frame(botones_frame, bg='#2c3e50')
        fila3.pack(pady=20)
        
        btn_config = tk.Button(fila3, text="CONFIGURACIÓN", 
                              bg='#9b59b6', fg='white', activebackground='#8e44ad',
                              command=self.abrir_configuracion,
                              font=('Arial', 12, 'bold'), width=20, height=2)
        btn_config.pack(side='left', padx=10)
        
        btn_ayuda = tk.Button(fila3, text="AYUDA", 
                             bg='#95a5a6', fg='white', activebackground='#7f8c8d',
                             command=self.abrir_ayuda,
                             font=('Arial', 12, 'bold'), width=20, height=2)
        btn_ayuda.pack(side='left', padx=10)
    
    def crear_footer_estadisticas(self):
        """Crear footer con estadísticas"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=120)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Título de estadísticas
        stats_titulo = tk.Label(footer_frame, text="ESTADÍSTICAS RÁPIDAS", 
                              font=("Arial", 16, "bold"), fg='white', bg='#34495e')
        stats_titulo.pack(pady=10)
        
        # Frame para las estadísticas
        self.stats_frame = tk.Frame(footer_frame, bg='#34495e')
        self.stats_frame.pack(expand=True, fill='both', padx=20)
    
    def actualizar_estadisticas(self):
        """Actualizar las estadísticas mostradas"""
        # Limpiar estadísticas anteriores
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
    
    # Obtener estadísticas de productos
        stats_productos = self.producto_controller.obtener_estadisticas_productos()
    
    # Obtener estadísticas de clientes
        from controllers.cliente_controller import ClienteController
        cliente_controller = ClienteController()
        stats_clientes = cliente_controller.obtener_estadisticas_clientes()

        # Obtener estadísticas de ventas
        from controllers.venta_controller import VentaController
        venta_controller = VentaController()
        stats_ventas = venta_controller.obtener_estadisticas_ventas()
    
    # Configurar estadísticas SIN EMOJIS
        estadisticas = [
        ("Total Productos", stats_productos['total_productos'], "#3498db", "PROD"),
        ("Total Clientes", stats_clientes['total_clientes'], "#2ecc71", "CLIEN"),
        ("Productos Bajo Stock", stats_productos['productos_bajo_stock'], "#e74c3c", "ALERT"),
        ("Valor Inventario", f"${stats_productos['valor_inventario']:,.0f}", "#f39c12", "VALOR")
    ]
    
    # Crear tarjetas de estadísticas
        for i, (titulo, valor, color, icono) in enumerate(estadisticas):
            stat_card = tk.Frame(self.stats_frame, bg=color, relief='raised', bd=3)
            stat_card.pack(side='left', fill='both', expand=True, padx=5, pady=10)
        
        # Icono y valor
            valor_frame = tk.Frame(stat_card, bg=color)
            valor_frame.pack(expand=True, fill='both')
        
            icono_label = tk.Label(valor_frame, text=icono, font=("Arial", 14, "bold"), 
                             fg='white', bg=color)
            icono_label.pack(pady=(10, 0))
        
            valor_label = tk.Label(valor_frame, text=str(valor), font=("Arial", 18, "bold"), 
                             fg='white', bg=color)
            valor_label.pack()
        
            titulo_label = tk.Label(valor_frame, text=titulo, font=("Arial", 10), 
                              fg='white', bg=color)
            titulo_label.pack(pady=(0, 10))
    
    def abrir_productos(self):
        """Abrir ventana de productos"""
        from views.ventana_productos import VentanaProductos
        ventana_productos = VentanaProductos(self.root)
        # Actualizar estadísticas cuando se cierre la ventana
        self.root.after(100, self.actualizar_estadisticas)

    def abrir_cuentas(self):
        """Abrir ventana de cuentas corrientes"""
        from views.ventana_cuentas import VentanaCuentas
        ventana_cuentas = VentanaCuentas(self.root)
        # Actualizar estadísticas cuando se cierre la ventana
        self.root.after(100, self.actualizar_estadisticas)
    
    def abrir_clientes(self):
        """Abrir ventana de clientes"""
        from views.ventana_clientes import VentanaClientes
        ventana_clientes = VentanaClientes(self.root)
        # Actualizar estadísticas cuando se cierre la ventana
        self.root.after(100, self.actualizar_estadisticas)
    
    def abrir_ventas(self):
        """Abrir ventana de ventas"""
        from views.ventana_ventas import VentanaVentas
        ventana_ventas = VentanaVentas(self.root)
        # Actualizar estadísticas cuando se cierre la ventana
        self.root.after(100, self.actualizar_estadisticas)
    
    def abrir_reportes(self):
        """Abrir ventana de reportes"""
        from views.ventana_reportes import VentanaReportes
        ventana_reportes = VentanaReportes(self.root)
        # Actualizar estadísticas cuando se cierre la ventana
        self.root.after(100, self.actualizar_estadisticas)
    
    def abrir_configuracion(self):
        """Abrir configuración"""
        tk.messagebox.showinfo("Configuración", "Módulo de configuración en desarrollo...")
    
    def abrir_ayuda(self):
        """Abrir ayuda"""
        ayuda_texto = """
        SISTEMA DE GESTIÓN EMPRESARIAL PRO
    
        MÓDULOS DISPONIBLES:
        PRODUCTOS: Gestión completa de inventario
        - Agregar, editar y eliminar productos
        - Control de stock y alertas
        - Categorización y búsqueda
    
    CLIENTES: Base de datos de clientes
    - Registro completo de clientes
    - Historial de compras
    - Análisis de mejores clientes
    
    VENTAS: Procesamiento de ventas
    - Carrito de compras interactivo
    - Actualización automática de stock
    - Cálculo de ganancias
    
    REPORTES: Análisis y reportes empresariales
    - Gráficos de ventas por período
    - Análisis de rentabilidad de productos
    - Ranking de mejores clientes
    - Inventario crítico
    - Exportación a CSV
    
    CÓMO USAR:
    1. Comience agregando productos en PRODUCTOS
    2. Registre sus clientes en CLIENTES
    3. Procese ventas en VENTAS
    4. Analice su negocio en REPORTES
    
    CARACTERÍSTICAS AVANZADAS:
    • Base de datos SQLite integrada
    • Exportación de reportes a CSV
    • Gráficos estadísticos (requiere matplotlib)
    • Validaciones automáticas
    • Interfaz profesional e intuitiva
    
    ¡Su sistema está completamente operativo!
    """
        tk.messagebox.showinfo("Ayuda del Sistema", ayuda_texto)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()