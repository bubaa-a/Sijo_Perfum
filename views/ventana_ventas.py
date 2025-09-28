"""
Ventana para gestión de ventas - Diseño elegante y funcional
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.venta_controller import VentaController

class VentanaVentas:
    def __init__(self, parent):
        self.parent = parent
        self.controller = VentaController()
        self.ventana = None
        self.tree = None
        self.tree_carrito = None
        self.productos_disponibles = []
        self.clientes_disponibles = []
        self.carrito = []
        self.crear_ventana()

    def crear_ventana(self):
        """Crear la ventana de ventas con diseño elegante"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Ventas - Sistema Empresarial Pro")
        self.ventana.geometry("1600x900")
        self.ventana.configure(bg='#f4f6f9')

        # Hacer que la ventana sea modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Configurar el grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Cargar datos iniciales
        self.cargar_datos_iniciales()

        # Crear interfaz
        self.crear_header_elegante()
        self.crear_contenido_principal()

        # Cargar ventas
        self.cargar_ventas()

    def cargar_datos_iniciales(self):
        """Cargar productos y clientes disponibles"""
        try:
            self.productos_disponibles = self.controller.obtener_productos_disponibles()
            self.clientes_disponibles = self.controller.obtener_clientes_activos()
        except:
            self.productos_disponibles = []
            self.clientes_disponibles = []

    def crear_header_elegante(self):
        """Crear header elegante con gradiente y estadísticas"""
        # Header principal con gradiente simulado
        header_frame = tk.Frame(self.ventana, bg='#2c3e50', height=110)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Sección izquierda - Título
        title_section = tk.Frame(header_frame, bg='#2c3e50')
        title_section.grid(row=0, column=0, sticky='w', padx=40, pady=25)

        # Título principal con estilo
        tk.Label(title_section, text="SISTEMA DE VENTAS",
                font=("Segoe UI", 22, "bold"), fg='#ecf0f1', bg='#2c3e50').pack(anchor='w')

        tk.Label(title_section, text="Gestión completa de ventas y facturación",
                font=("Segoe UI", 11), fg='#bdc3c7', bg='#2c3e50').pack(anchor='w', pady=(2, 0))

        # Sección derecha - Estadísticas en tarjetas
        stats_section = tk.Frame(header_frame, bg='#2c3e50')
        stats_section.grid(row=0, column=1, sticky='e', padx=40, pady=20)

        self.crear_tarjetas_estadisticas(stats_section)


    def crear_tarjetas_estadisticas(self, parent):
        """Crear tarjetas de estadísticas elegantes"""
        try:
            stats = self.controller.obtener_estadisticas_ventas()

            # Container de tarjetas
            cards_frame = tk.Frame(parent, bg='#2c3e50')
            cards_frame.pack()

            # Tarjeta 1 - Ventas Hoy
            card1 = tk.Frame(cards_frame, bg='#27ae60', relief='raised', bd=1, padx=15, pady=10)
            card1.pack(side='left', padx=(0, 10))

            tk.Label(card1, text="Ventas Hoy", font=("Segoe UI", 9, "bold"),
                    fg='white', bg='#27ae60').pack()
            tk.Label(card1, text=str(stats.get('ventas_hoy', 0)), font=("Segoe UI", 16, "bold"),
                    fg='white', bg='#27ae60').pack()

            # Tarjeta 2 - Ingresos Hoy
            card2 = tk.Frame(cards_frame, bg='#e74c3c', relief='raised', bd=1, padx=15, pady=10)
            card2.pack(side='left')

            tk.Label(card2, text="Ingresos Hoy", font=("Segoe UI", 9, "bold"),
                    fg='white', bg='#e74c3c').pack()
            ingresos = stats.get('ingresos_hoy', 0)
            tk.Label(card2, text=f"${ingresos:,.0f}", font=("Segoe UI", 16, "bold"),
                    fg='white', bg='#e74c3c').pack()

        except:
            # Tarjeta de error simple
            error_card = tk.Frame(parent, bg='#7f8c8d', relief='raised', bd=1, padx=20, pady=10)
            error_card.pack()
            tk.Label(error_card, text="Estadísticas no disponibles",
                    font=("Segoe UI", 10), fg='white', bg='#7f8c8d').pack()

    def crear_contenido_principal(self):
        """Crear el contenido principal con diseño en columnas"""
        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg='#f4f6f9')
        main_container.grid(row=1, column=0, sticky='nsew', padx=25, pady=25)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure((0, 1), weight=1)

        # Columna izquierda - Formulario y Carrito
        self.crear_columna_izquierda(main_container)

        # Columna derecha - Lista de ventas
        self.crear_columna_derecha(main_container)

        # Fila inferior - Botones
        self.crear_botones_principales(main_container)

    def crear_columna_izquierda(self, parent):
        """Crear la columna izquierda con formulario y carrito"""
        left_column = tk.Frame(parent, bg='#f4f6f9')
        left_column.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0, 15))
        left_column.grid_rowconfigure(1, weight=1)
        left_column.grid_columnconfigure(0, weight=1)

        # Formulario de nueva venta
        self.crear_formulario_elegante(left_column)

        # Carrito de compras
        self.crear_carrito_elegante(left_column)

    def crear_columna_derecha(self, parent):
        """Crear la columna derecha con la lista de ventas"""
        right_column = tk.Frame(parent, bg='#f4f6f9')
        right_column.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=(15, 0))
        right_column.grid_rowconfigure(0, weight=1)
        right_column.grid_columnconfigure(0, weight=1)

        # Lista de ventas
        self.crear_lista_ventas_elegante(right_column)

    def crear_formulario_elegante(self, parent):
        """Crear formulario elegante para nueva venta"""
        # Marco del formulario
        form_frame = tk.LabelFrame(parent, text="   Nueva Venta   ",
                                  font=("Segoe UI", 13, "bold"), fg='#2c3e50',
                                  bg='white', relief='solid', bd=1, padx=20, pady=15)
        form_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        form_frame.grid_columnconfigure(0, weight=1)

        # Variables del formulario
        self.cliente_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.observaciones_var = tk.StringVar()

        # Estilo común
        label_style = {'font': ('Segoe UI', 10, 'bold'), 'fg': '#34495e', 'bg': 'white'}
        entry_style = {'font': ('Segoe UI', 10), 'relief': 'solid', 'bd': 1, 'bg': '#fafbfc'}

        # Sección Cliente
        cliente_frame = tk.Frame(form_frame, bg='white')
        cliente_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        cliente_frame.grid_columnconfigure(1, weight=1)

        tk.Label(cliente_frame, text="Cliente:", **label_style).grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.cliente_combo = ttk.Combobox(cliente_frame, textvariable=self.cliente_var,
                                         state="readonly", font=('Segoe UI', 10), width=40)
        self.cliente_combo.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 10))

        tk.Label(cliente_frame, text="Observaciones:", **label_style).grid(row=2, column=0, sticky='w', pady=(0, 5))
        tk.Entry(cliente_frame, textvariable=self.observaciones_var, **entry_style).grid(
            row=3, column=0, columnspan=2, sticky='ew')

        # Línea separadora
        separator = tk.Frame(form_frame, bg='#ecf0f1', height=2)
        separator.grid(row=1, column=0, sticky='ew', pady=20)

        # Sección Productos
        productos_label = tk.Label(form_frame, text="Agregar Productos al Carrito",
                                  font=("Segoe UI", 11, "bold"), fg='#e74c3c', bg='white')
        productos_label.grid(row=2, column=0, sticky='w', pady=(0, 15))

        productos_frame = tk.Frame(form_frame, bg='white')
        productos_frame.grid(row=3, column=0, sticky='ew')
        productos_frame.grid_columnconfigure((0, 1), weight=1)

        # Producto
        tk.Label(productos_frame, text="Producto:", **label_style).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        self.producto_combo = ttk.Combobox(productos_frame, textvariable=self.producto_var,
                                          state="readonly", font=('Segoe UI', 10))
        self.producto_combo.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        self.producto_combo.bind('<<ComboboxSelected>>', self.producto_seleccionado)

        # Cantidad y Precio
        tk.Label(productos_frame, text="Cantidad:", **label_style).grid(row=2, column=0, sticky='w', pady=(0, 5))
        tk.Entry(productos_frame, textvariable=self.cantidad_var, width=12, **entry_style).grid(
            row=3, column=0, sticky='ew', padx=(0, 10))

        tk.Label(productos_frame, text="Precio Unit.:", **label_style).grid(row=2, column=1, sticky='w', pady=(0, 5))
        tk.Entry(productos_frame, textvariable=self.precio_var, width=12, **entry_style).grid(
            row=3, column=1, sticky='ew')

        # Botón agregar
        btn_agregar = tk.Button(form_frame, text="+ Agregar al Carrito",
                               font=("Segoe UI", 10, "bold"), fg='white', bg='#27ae60',
                               relief='flat', cursor='hand2', pady=8,
                               command=self.agregar_al_carrito)
        btn_agregar.grid(row=4, column=0, pady=15)

        # Efecto hover
        def on_enter(e): btn_agregar.configure(relief='raised', bg='#229954')
        def on_leave(e): btn_agregar.configure(relief='flat', bg='#27ae60')
        btn_agregar.bind('<Enter>', on_enter)
        btn_agregar.bind('<Leave>', on_leave)

        # Cargar combos
        self.cargar_combos_iniciales()

    def crear_carrito_elegante(self, parent):
        """Crear carrito elegante"""
        # Marco del carrito
        cart_frame = tk.LabelFrame(parent, text="   Carrito de Compras   ",
                                  font=("Segoe UI", 13, "bold"), fg='#2c3e50',
                                  bg='white', relief='solid', bd=1, padx=15, pady=10)
        cart_frame.grid(row=1, column=0, sticky='nsew')
        cart_frame.grid_rowconfigure(0, weight=1)
        cart_frame.grid_columnconfigure(0, weight=1)

        # Container del treeview
        tree_container = tk.Frame(cart_frame, bg='white')
        tree_container.grid(row=0, column=0, sticky='nsew', pady=(10, 0))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Estilo del carrito
        style = ttk.Style()
        style.configure("Carrito.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 9),
                       rowheight=28)
        style.configure("Carrito.Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=("Segoe UI", 10, "bold"))

        # Treeview del carrito
        columns = ('Producto', 'Cant.', 'P.Unit', 'Subtotal')
        self.tree_carrito = ttk.Treeview(tree_container, columns=columns, show='headings',
                                        height=8, style="Carrito.Treeview")

        # Configurar columnas
        self.tree_carrito.heading('Producto', text='Producto')
        self.tree_carrito.heading('Cant.', text='Cant.')
        self.tree_carrito.heading('P.Unit', text='P.Unit')
        self.tree_carrito.heading('Subtotal', text='Subtotal')

        self.tree_carrito.column('Producto', width=140, anchor='w')
        self.tree_carrito.column('Cant.', width=50, anchor='center')
        self.tree_carrito.column('P.Unit', width=70, anchor='center')
        self.tree_carrito.column('Subtotal', width=80, anchor='center')

        # Scrollbar
        cart_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=cart_scrollbar.set)

        self.tree_carrito.grid(row=0, column=0, sticky='nsew')
        cart_scrollbar.grid(row=0, column=1, sticky='ns')

        # Panel inferior del carrito
        bottom_panel = tk.Frame(cart_frame, bg='white')
        bottom_panel.grid(row=1, column=0, sticky='ew', pady=(15, 5))
        bottom_panel.grid_columnconfigure(1, weight=1)

        # Botones del carrito
        btn_quitar = tk.Button(bottom_panel, text="Quitar", font=("Segoe UI", 9, "bold"),
                              fg='white', bg='#e74c3c', relief='flat', cursor='hand2',
                              padx=12, command=self.quitar_del_carrito)
        btn_quitar.grid(row=0, column=0, padx=(0, 5))

        btn_limpiar = tk.Button(bottom_panel, text="Limpiar", font=("Segoe UI", 9, "bold"),
                               fg='white', bg='#f39c12', relief='flat', cursor='hand2',
                               padx=12, command=self.limpiar_carrito)
        btn_limpiar.grid(row=0, column=1, padx=5)

        # Total
        total_frame = tk.Frame(bottom_panel, bg='#2c3e50', relief='solid', bd=1)
        total_frame.grid(row=0, column=2, padx=(10, 0))

        self.total_var = tk.StringVar(value="Total: $0")
        tk.Label(total_frame, textvariable=self.total_var,
                font=("Segoe UI", 11, "bold"), fg='white', bg='#2c3e50').pack(padx=12, pady=6)

        # Efectos hover
        def crear_hover_efecto(btn, normal, hover):
            def enter(e): btn.configure(relief='raised', bg=hover)
            def leave(e): btn.configure(relief='flat', bg=normal)
            btn.bind('<Enter>', enter)
            btn.bind('<Leave>', leave)

        crear_hover_efecto(btn_quitar, '#e74c3c', '#c0392b')
        crear_hover_efecto(btn_limpiar, '#f39c12', '#e67e22')

    def crear_lista_ventas_elegante(self, parent):
        """Crear lista elegante de ventas"""
        # Marco de la lista
        list_frame = tk.LabelFrame(parent, text="   Historial de Ventas   ",
                                  font=("Segoe UI", 13, "bold"), fg='#2c3e50',
                                  bg='white', relief='solid', bd=1, padx=15, pady=10)
        list_frame.grid(row=0, column=0, sticky='nsew')
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Info header
        info_frame = tk.Frame(list_frame, bg='white')
        info_frame.grid(row=0, column=0, sticky='ew', pady=(10, 5))

        tk.Label(info_frame, text="Doble clic para ver detalles de la venta",
                font=("Segoe UI", 9, "italic"), fg='#7f8c8d', bg='white').pack(side='left')

        # Container del treeview
        tree_container = tk.Frame(list_frame, bg='white')
        tree_container.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Estilo de ventas
        style = ttk.Style()
        style.configure("Ventas.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 9),
                       rowheight=30)
        style.configure("Ventas.Treeview.Heading",
                       background="#3498db",
                       foreground="white",
                       font=("Segoe UI", 10, "bold"))

        # Treeview de ventas
        columns = ('ID', 'Cliente', 'Total', 'Fecha', 'Observaciones')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="Ventas.Treeview")

        # Configurar columnas
        headers = {
            'ID': ('ID', 60),
            'Cliente': ('Cliente', 180),
            'Total': ('Total', 100),
            'Fecha': ('Fecha', 120),
            'Observaciones': ('Observaciones', 200)
        }

        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center' if col in ['ID', 'Total'] else 'w')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Evento doble clic
        self.tree.bind('<Double-1>', self.ver_detalle_venta)

    def crear_botones_principales(self, parent):
        """Crear botones principales con diseño elegante"""
        # Panel de botones
        buttons_panel = tk.Frame(parent, bg='#f4f6f9')
        buttons_panel.grid(row=2, column=0, columnspan=2, pady=(25, 0))

        # Contenedor centrado
        center_container = tk.Frame(buttons_panel, bg='#f4f6f9')
        center_container.pack()

        # Función para crear botones elegantes
        def crear_boton_elegante(texto, color, comando, destacado=False):
            width = 16 if destacado else 12
            pady = 12 if destacado else 8
            font_size = 11 if destacado else 10

            btn = tk.Button(center_container, text=texto,
                           font=("Segoe UI", font_size, "bold"), fg='white', bg=color,
                           relief='flat', cursor='hand2', width=width, pady=pady,
                           command=comando)
            btn.pack(side='left', padx=12)

            # Crear efecto hover
            hover_color = self.obtener_color_hover(color)
            def on_enter(e): btn.configure(relief='raised', bg=hover_color)
            def on_leave(e): btn.configure(relief='flat', bg=color)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)

            return btn

        # Botones principales
        crear_boton_elegante("PROCESAR VENTA", "#27ae60", self.procesar_venta, destacado=True)
        crear_boton_elegante("Ver Detalle", "#3498db", self.ver_detalle_venta)
        crear_boton_elegante("Eliminar Venta", "#e74c3c", self.eliminar_venta)
        crear_boton_elegante("Actualizar Lista", "#9b59b6", self.cargar_ventas)
        crear_boton_elegante("Cerrar", "#95a5a6", self.cerrar_ventana)

    def obtener_color_hover(self, color):
        """Obtener color más oscuro para hover"""
        colores = {
            "#27ae60": "#229954",
            "#3498db": "#2980b9",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad",
            "#95a5a6": "#7f8c8d"
        }
        return colores.get(color, color)

    def cargar_combos_iniciales(self):
        """Cargar datos en los combos"""
        try:
            # Cargar clientes
            clientes_nombres = [f"{c.id} - {c.nombre} {c.apellido}" for c in self.clientes_disponibles]
            self.cliente_combo['values'] = clientes_nombres

            # Cargar productos
            productos_nombres = [f"{p.id} - {p.nombre} (Stock: {p.stock}) - ${p.precio_venta:.0f}"
                               for p in self.productos_disponibles]
            self.producto_combo['values'] = productos_nombres
        except:
            self.cliente_combo['values'] = []
            self.producto_combo['values'] = []

    def producto_seleccionado(self, event):
        """Llenar precio cuando se selecciona producto"""
        seleccion = self.producto_var.get()
        if seleccion:
            try:
                producto_id = int(seleccion.split(' - ')[0])
                for producto in self.productos_disponibles:
                    if producto.id == producto_id:
                        self.precio_var.set(str(producto.precio_venta))
                        break
            except:
                pass

    def agregar_al_carrito(self):
        """Agregar producto al carrito"""
        try:
            if not self.producto_var.get() or not self.cantidad_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un producto y especifique la cantidad")
                return

            producto_id = int(self.producto_var.get().split(' - ')[0])
            cantidad = int(self.cantidad_var.get())
            precio = float(self.precio_var.get())

            # Buscar producto
            producto = None
            for p in self.productos_disponibles:
                if p.id == producto_id:
                    producto = p
                    break

            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return

            if cantidad > producto.stock:
                messagebox.showwarning("Advertencia", f"Stock insuficiente. Disponible: {producto.stock}")
                return

            # Agregar al carrito
            subtotal = cantidad * precio
            self.tree_carrito.insert('', 'end', values=(
                producto.nombre,
                cantidad,
                f"${precio:.2f}",
                f"${subtotal:.2f}"
            ))

            # Agregar a lista interna
            self.carrito.append({
                'producto_id': producto_id,
                'producto': producto,
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': subtotal
            })

            # Actualizar total
            self.actualizar_total()

            # Limpiar campos
            self.producto_var.set('')
            self.cantidad_var.set('')
            self.precio_var.set('')

        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def quitar_del_carrito(self):
        """Quitar producto del carrito"""
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para quitar")
            return

        item = seleccion[0]
        index = self.tree_carrito.index(item)

        self.tree_carrito.delete(item)
        if index < len(self.carrito):
            self.carrito.pop(index)

        self.actualizar_total()

    def limpiar_carrito(self):
        """Limpiar carrito completo"""
        if self.carrito and messagebox.askyesno("Confirmar", "¿Limpiar todo el carrito?"):
            for item in self.tree_carrito.get_children():
                self.tree_carrito.delete(item)
            self.carrito.clear()
            self.actualizar_total()

    def actualizar_total(self):
        """Actualizar total del carrito"""
        total = sum(item['subtotal'] for item in self.carrito)
        self.total_var.set(f"Total: ${total:,.2f}")

    def procesar_venta(self):
        """Procesar la venta actual"""
        if not self.cliente_var.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return

        if not self.carrito:
            messagebox.showwarning("Advertencia", "Agregue productos al carrito")
            return

        try:
            cliente_id = int(self.cliente_var.get().split(' - ')[0])

            # Preparar detalles de venta
            detalles_venta = []
            for item in self.carrito:
                detalles_venta.append({
                    'producto_id': item['producto_id'],
                    'cantidad': item['cantidad'],
                    'precio_unitario': item['precio']
                })

            # Procesar venta
            if self.controller.crear_venta(cliente_id, detalles_venta, self.observaciones_var.get()):
                self.limpiar_formulario_venta()
                self.cargar_ventas()
                # Recargar productos por si cambió el stock
                self.cargar_datos_iniciales()
                self.cargar_combos_iniciales()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")

    def limpiar_formulario_venta(self):
        """Limpiar formulario de venta"""
        self.cliente_var.set('')
        self.observaciones_var.set('')
        self.producto_var.set('')
        self.cantidad_var.set('')
        self.precio_var.set('')

        # Limpiar carrito
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        self.carrito.clear()
        self.actualizar_total()

    def cargar_ventas(self):
        """Cargar ventas en la lista - CORREGIDO"""
        try:
            # Limpiar lista
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener ventas usando método corregido
            from config.database import DatabaseManager
            db = DatabaseManager()

            query = '''
                SELECT v.id, v.cliente_id, v.total, v.fecha_venta, v.observaciones,
                       c.nombre, c.apellido
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.fecha_venta DESC
            '''

            resultados = db.ejecutar_consulta(query)

            if resultados:
                for fila in resultados:
                    venta_id = fila[0]
                    total = fila[2]
                    fecha_venta = fila[3]
                    observaciones = fila[4] or ""

                    # Obtener nombre del cliente
                    if fila[5] and fila[6]:  # Si hay nombre y apellido
                        cliente_nombre = f"{fila[5]} {fila[6]}"
                    else:
                        cliente_nombre = "Cliente no encontrado"

                    # Formatear fecha
                    try:
                        if isinstance(fecha_venta, str):
                            from datetime import datetime
                            fecha_obj = datetime.strptime(fecha_venta, '%Y-%m-%d %H:%M:%S')
                            fecha_formateada = fecha_obj.strftime('%Y-%m-%d %H:%M')
                        else:
                            fecha_formateada = str(fecha_venta)
                    except:
                        fecha_formateada = str(fecha_venta)

                    self.tree.insert('', 'end', values=(
                        venta_id,
                        cliente_nombre,
                        f"${total:.2f}",
                        fecha_formateada,
                        observaciones
                    ))

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {str(e)}")

    def ver_detalle_venta(self, event=None):
        """Ver detalle completo de venta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver su detalle")
            return

        item = self.tree.item(seleccion[0])
        venta_id = item['values'][0]

        # Crear ventana de detalle
        self.mostrar_ventana_detalle_venta(venta_id)

    def mostrar_ventana_detalle_venta(self, venta_id):
        """Mostrar ventana completa con detalle de venta"""
        # Crear ventana
        detalle_window = tk.Toplevel(self.ventana)
        detalle_window.title(f"Detalle de Venta #{venta_id}")
        detalle_window.geometry("1200x800")
        detalle_window.configure(bg='#f4f6f9')
        detalle_window.transient(self.ventana)
        detalle_window.grab_set()

        # Obtener datos de la venta
        try:
            venta_datos = self.obtener_datos_completos_venta(venta_id)
            if not venta_datos:
                messagebox.showerror("Error", "No se pudieron cargar los datos de la venta")
                detalle_window.destroy()
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener datos: {str(e)}")
            detalle_window.destroy()
            return

        # Crear header de la ventana
        self.crear_header_detalle(detalle_window, venta_datos)

        # Crear contenido principal en pestañas
        self.crear_contenido_detalle(detalle_window, venta_datos)

    def obtener_datos_completos_venta(self, venta_id):
        """Obtener todos los datos relacionados con la venta"""
        from config.database import DatabaseManager
        db = DatabaseManager()

        # Datos básicos de la venta
        query_venta = '''
            SELECT v.id, v.cliente_id, v.total, v.fecha_venta, v.observaciones,
                   c.nombre, c.apellido, c.telefono, c.email, c.direccion
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        '''
        venta_info = db.ejecutar_consulta(query_venta, (venta_id,))
        if not venta_info:
            return None

        venta_data = venta_info[0]

        # Detalles de productos vendidos
        query_detalle = '''
            SELECT dv.producto_id, dv.cantidad, dv.precio_unitario, dv.subtotal,
                   p.nombre, p.descripcion, p.categoria
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        '''
        productos = db.ejecutar_consulta(query_detalle, (venta_id,))

        # Estado de cuenta del cliente
        query_cuenta = '''
            SELECT saldo_total, saldo_pendiente, fecha_ultima_actualizacion
            FROM cuentas_corrientes
            WHERE cliente_id = ? AND activa = 1
        '''
        cuenta_info = db.ejecutar_consulta(query_cuenta, (venta_data[1],))

        # Abonos del cliente
        query_abonos = '''
            SELECT monto_abono, metodo_pago, descripcion, fecha_abono, recibo_numero
            FROM abonos
            WHERE cliente_id = ?
            ORDER BY fecha_abono DESC
            LIMIT 10
        '''
        abonos = db.ejecutar_consulta(query_abonos, (venta_data[1],))

        return {
            'venta': {
                'id': venta_data[0],
                'cliente_id': venta_data[1],
                'total': venta_data[2],
                'fecha_venta': venta_data[3],
                'observaciones': venta_data[4] or "",
                'cliente_nombre': f"{venta_data[5]} {venta_data[6]}" if venta_data[5] else "Sin nombre",
                'cliente_telefono': venta_data[7] or "",
                'cliente_email': venta_data[8] or "",
                'cliente_direccion': venta_data[9] or ""
            },
            'productos': productos or [],
            'cuenta': cuenta_info[0] if cuenta_info else (0, 0, None),
            'abonos': abonos or []
        }

    def crear_header_detalle(self, parent, datos):
        """Crear header elegante para la ventana de detalle"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Título principal
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(expand=True, fill='both')

        tk.Label(title_frame, text=f"DETALLE DE VENTA #{datos['venta']['id']}",
                font=("Segoe UI", 20, "bold"), fg='#ecf0f1', bg='#2c3e50').pack(expand=True)

        info_frame = tk.Frame(title_frame, bg='#2c3e50')
        info_frame.pack()

        tk.Label(info_frame, text=f"Cliente: {datos['venta']['cliente_nombre']}",
                font=("Segoe UI", 12), fg='#bdc3c7', bg='#2c3e50').pack(side='left', padx=20)

        tk.Label(info_frame, text=f"Total: ${datos['venta']['total']:,.2f}",
                font=("Segoe UI", 12, "bold"), fg='#27ae60', bg='#2c3e50').pack(side='left', padx=20)

        tk.Label(info_frame, text=f"Fecha: {datos['venta']['fecha_venta']}",
                font=("Segoe UI", 12), fg='#bdc3c7', bg='#2c3e50').pack(side='left', padx=20)

    def crear_contenido_detalle(self, parent, datos):
        """Crear contenido principal con pestañas"""
        main_frame = tk.Frame(parent, bg='#f4f6f9')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Crear notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        # Pestaña 1: Productos vendidos
        self.crear_pestaña_productos_vendidos(notebook, datos)

        # Pestaña 2: Estado de cuenta
        self.crear_pestaña_estado_cuenta(notebook, datos)

        # Pestaña 3: Información del cliente
        self.crear_pestaña_info_cliente(notebook, datos)

    def crear_pestaña_productos_vendidos(self, notebook, datos):
        """Crear pestaña con productos vendidos"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🛒 Productos Vendidos")

        # Frame principal
        main_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Título
        tk.Label(main_frame, text="Productos incluidos en esta venta",
                font=("Segoe UI", 14, "bold"), fg='#2c3e50', bg='white').pack(pady=(15, 20))

        # Crear tabla de productos
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Configurar estilo
        style = ttk.Style()
        style.configure("Detalle.Treeview",
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       font=("Segoe UI", 10),
                       rowheight=30)
        style.configure("Detalle.Treeview.Heading",
                       background="#3498db",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))

        # Treeview
        columns = ('Producto', 'Categoría', 'Cantidad', 'Precio Unit.', 'Subtotal')
        tree_productos = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                     style="Detalle.Treeview")

        # Headers
        tree_productos.heading('Producto', text='Producto')
        tree_productos.heading('Categoría', text='Categoría')
        tree_productos.heading('Cantidad', text='Cantidad')
        tree_productos.heading('Precio Unit.', text='Precio Unit.')
        tree_productos.heading('Subtotal', text='Subtotal')

        # Configurar columnas
        tree_productos.column('Producto', width=200, anchor='w')
        tree_productos.column('Categoría', width=120, anchor='center')
        tree_productos.column('Cantidad', width=80, anchor='center')
        tree_productos.column('Precio Unit.', width=100, anchor='center')
        tree_productos.column('Subtotal', width=100, anchor='center')

        # Cargar datos
        total_productos = 0
        for producto in datos['productos']:
            tree_productos.insert('', 'end', values=(
                producto[4],  # nombre
                producto[6] or 'Sin categoría',  # categoría
                f"{producto[1]:,}",  # cantidad
                f"${producto[2]:,.2f}",  # precio unitario
                f"${producto[3]:,.2f}"  # subtotal
            ))
            total_productos += producto[1]

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree_productos.yview)
        tree_productos.configure(yscrollcommand=scrollbar.set)

        tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Resumen
        resumen_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='solid', bd=1)
        resumen_frame.pack(fill='x', padx=15, pady=(0, 15))

        tk.Label(resumen_frame, text=f"Total de productos: {total_productos:,}",
                font=("Segoe UI", 11, "bold"), fg='#2c3e50', bg='#ecf0f1').pack(side='left', padx=15, pady=10)

        tk.Label(resumen_frame, text=f"TOTAL VENTA: ${datos['venta']['total']:,.2f}",
                font=("Segoe UI", 12, "bold"), fg='#27ae60', bg='#ecf0f1').pack(side='right', padx=15, pady=10)

    def crear_pestaña_estado_cuenta(self, notebook, datos):
        """Crear pestaña con estado de cuenta"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="💳 Estado de Cuenta")

        # Frame principal
        main_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Título
        tk.Label(main_frame, text="Estado de cuenta del cliente",
                font=("Segoe UI", 14, "bold"), fg='#2c3e50', bg='white').pack(pady=(15, 20))

        # Estado actual
        estado_frame = tk.Frame(main_frame, bg='white')
        estado_frame.pack(fill='x', padx=15, pady=(0, 20))

        # Cards de estado
        saldo_total = datos['cuenta'][0]
        saldo_pendiente = datos['cuenta'][1]
        saldo_abonado = saldo_total - saldo_pendiente

        # Card saldo total
        card1 = tk.Frame(estado_frame, bg='#3498db', relief='raised', bd=2)
        card1.pack(side='left', fill='x', expand=True, padx=(0, 10))

        tk.Label(card1, text="SALDO TOTAL", font=("Segoe UI", 10, "bold"),
                fg='white', bg='#3498db').pack(pady=(10, 5))
        tk.Label(card1, text=f"${saldo_total:,.2f}", font=("Segoe UI", 16, "bold"),
                fg='white', bg='#3498db').pack(pady=(0, 10))

        # Card saldo abonado
        card2 = tk.Frame(estado_frame, bg='#27ae60', relief='raised', bd=2)
        card2.pack(side='left', fill='x', expand=True, padx=5)

        tk.Label(card2, text="ABONADO", font=("Segoe UI", 10, "bold"),
                fg='white', bg='#27ae60').pack(pady=(10, 5))
        tk.Label(card2, text=f"${saldo_abonado:,.2f}", font=("Segoe UI", 16, "bold"),
                fg='white', bg='#27ae60').pack(pady=(0, 10))

        # Card saldo pendiente
        card3 = tk.Frame(estado_frame, bg='#e74c3c', relief='raised', bd=2)
        card3.pack(side='left', fill='x', expand=True, padx=(10, 0))

        tk.Label(card3, text="PENDIENTE", font=("Segoe UI", 10, "bold"),
                fg='white', bg='#e74c3c').pack(pady=(10, 5))
        tk.Label(card3, text=f"${saldo_pendiente:,.2f}", font=("Segoe UI", 16, "bold"),
                fg='white', bg='#e74c3c').pack(pady=(0, 10))

        # Historial de abonos
        if datos['abonos']:
            tk.Label(main_frame, text="Últimos abonos realizados",
                    font=("Segoe UI", 12, "bold"), fg='#2c3e50', bg='white').pack(pady=(20, 10))

            # Tabla de abonos
            abonos_frame = tk.Frame(main_frame, bg='white')
            abonos_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

            columns_abonos = ('Fecha', 'Monto', 'Método', 'Descripción', 'Recibo')
            tree_abonos = ttk.Treeview(abonos_frame, columns=columns_abonos, show='headings',
                                      style="Detalle.Treeview", height=8)

            # Headers
            tree_abonos.heading('Fecha', text='Fecha')
            tree_abonos.heading('Monto', text='Monto')
            tree_abonos.heading('Método', text='Método')
            tree_abonos.heading('Descripción', text='Descripción')
            tree_abonos.heading('Recibo', text='Recibo #')

            # Configurar columnas
            tree_abonos.column('Fecha', width=120, anchor='center')
            tree_abonos.column('Monto', width=100, anchor='center')
            tree_abonos.column('Método', width=100, anchor='center')
            tree_abonos.column('Descripción', width=200, anchor='w')
            tree_abonos.column('Recibo', width=100, anchor='center')

            # Cargar abonos
            for abono in datos['abonos']:
                tree_abonos.insert('', 'end', values=(
                    abono[3][:10] if abono[3] else '',  # fecha
                    f"${abono[0]:,.2f}",  # monto
                    abono[1] or 'Efectivo',  # método
                    abono[2] or '',  # descripción
                    abono[4] or ''  # recibo
                ))

            # Scrollbar
            scrollbar_abonos = ttk.Scrollbar(abonos_frame, orient='vertical', command=tree_abonos.yview)
            tree_abonos.configure(yscrollcommand=scrollbar_abonos.set)

            tree_abonos.pack(side='left', fill='both', expand=True)
            scrollbar_abonos.pack(side='right', fill='y')
        else:
            tk.Label(main_frame, text="No hay abonos registrados para este cliente",
                    font=("Segoe UI", 11, "italic"), fg='#7f8c8d', bg='white').pack(pady=30)

    def crear_pestaña_info_cliente(self, notebook, datos):
        """Crear pestaña con información del cliente"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="👤 Info. Cliente")

        # Frame principal
        main_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Título
        tk.Label(main_frame, text="Información del cliente",
                font=("Segoe UI", 14, "bold"), fg='#2c3e50', bg='white').pack(pady=(15, 30))

        # Información del cliente
        info_frame = tk.Frame(main_frame, bg='white')
        info_frame.pack(expand=True)

        venta = datos['venta']

        # Estilo para etiquetas
        label_style = {'font': ('Segoe UI', 11, 'bold'), 'fg': '#2c3e50', 'bg': 'white'}
        value_style = {'font': ('Segoe UI', 11), 'fg': '#34495e', 'bg': 'white'}

        info_data = [
            ("Nombre completo:", venta['cliente_nombre']),
            ("Teléfono:", venta['cliente_telefono'] or "No registrado"),
            ("Email:", venta['cliente_email'] or "No registrado"),
            ("Dirección:", venta['cliente_direccion'] or "No registrada"),
        ]

        for i, (label, value) in enumerate(info_data):
            row_frame = tk.Frame(info_frame, bg='white')
            row_frame.pack(fill='x', pady=8)

            tk.Label(row_frame, text=label, **label_style).pack(side='left', anchor='w')
            tk.Label(row_frame, text=value, **value_style).pack(side='left', padx=(20, 0))

        # Información de la venta
        tk.Label(main_frame, text="Información de esta venta",
                font=("Segoe UI", 12, "bold"), fg='#2c3e50', bg='white').pack(pady=(40, 20))

        venta_info_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='solid', bd=1)
        venta_info_frame.pack(fill='x', padx=15, pady=(0, 15))

        venta_data = [
            ("ID de venta:", f"#{venta['id']}"),
            ("Fecha de venta:", venta['fecha_venta']),
            ("Observaciones:", venta['observaciones'] or "Ninguna"),
        ]

        for label, value in venta_data:
            row_frame = tk.Frame(venta_info_frame, bg='#ecf0f1')
            row_frame.pack(fill='x', pady=5, padx=15)

            tk.Label(row_frame, text=label, font=('Segoe UI', 10, 'bold'),
                    fg='#2c3e50', bg='#ecf0f1').pack(side='left')
            tk.Label(row_frame, text=value, font=('Segoe UI', 10),
                    fg='#34495e', bg='#ecf0f1').pack(side='left', padx=(10, 0))

    def eliminar_venta(self):
        """Eliminar venta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta para eliminar")
            return

        item = self.tree.item(seleccion[0])
        venta_id = item['values'][0]
        cliente = item['values'][1]
        total = item['values'][2]

        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar la venta #{venta_id}?\n\n"
            f"Cliente: {cliente}\n"
            f"Total: {total}\n\n"
            "Esta acción no se puede deshacer."
        )

        if respuesta:
            try:
                if self.controller.eliminar_venta(venta_id):
                    messagebox.showinfo("Éxito", "Venta eliminada correctamente")
                    self.cargar_ventas()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la venta")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar venta: {str(e)}")

    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()