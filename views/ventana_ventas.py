"""
Ventana para gestión de ventas - Diseño Moderno con CustomTkinter
Versión con estilos unificados
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.venta_controller import VentaController
from config.estilos import (Colores, Fuentes, Espaciado, Dimensiones,
                            Iconos, obtener_color_hover)

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
        """Crear la ventana de ventas con diseño moderno CustomTkinter"""
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Ventas - Sistema Empresarial Pro")
        self.ventana.geometry("1650x950")
        self.ventana.configure(bg=Colores.BG_PRIMARY)

        # Modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Cargar datos iniciales
        self.cargar_datos_iniciales()

        # Crear interfaz
        self.crear_header()
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

    def crear_header(self):
        """Crear header moderno con CustomTkinter"""
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
            text=f"{Iconos.VENTAS} SISTEMA DE VENTAS",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(anchor='w')

        ctk.CTkLabel(
            title_frame,
            text="Punto de venta y gestión de facturación",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
            text_color='#e8eaf6'
        ).pack(anchor='w', pady=(3, 0))

        # Estadísticas derecha
        self.stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.stats_frame.grid(row=0, column=1, sticky='e', padx=40, pady=20)

        self.crear_estadisticas(self.stats_frame)

    def crear_estadisticas(self, parent):
        """Crear tarjetas de estadísticas"""
        # Limpiar contenedor antes de recrear
        for widget in parent.winfo_children():
            widget.destroy()

        try:
            stats = self.controller.obtener_estadisticas_ventas()
            print(f"DEBUG Ventana: Estadísticas recibidas: {stats}")

            cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
            cards_frame.pack()

            # Total Vendido Hoy
            card = ctk.CTkFrame(cards_frame, fg_color='#27ae60', corner_radius=10)
            card.pack(side='left')

            ctk.CTkLabel(card, text="💰 Total Vendido Hoy", font=("Segoe UI", 10, "bold"),
                        text_color='white').pack(padx=20, pady=(10, 2))
            ingresos = stats.get('ingresos_hoy', 0)
            ctk.CTkLabel(card, text=f"${ingresos:,.0f}",
                        font=("Segoe UI", 18, "bold"),
                        text_color='white').pack(padx=20, pady=(0, 10))

        except Exception as e:
            print(f"Error al cargar estadísticas: {str(e)}")
            import traceback
            traceback.print_exc()
            error_card = ctk.CTkFrame(parent, fg_color='#95a5a6', corner_radius=10)
            error_card.pack()
            ctk.CTkLabel(error_card, text="Estadísticas no disponibles",
                        font=("Segoe UI", 10),
                        text_color='white').pack(padx=20, pady=10)

    def actualizar_estadisticas(self):
        """Actualizar las estadísticas en el header"""
        self.crear_estadisticas(self.stats_frame)

    def crear_contenido_principal(self):
        """Crear contenido principal con diseño en columnas"""
        main_container = ctk.CTkFrame(self.ventana, fg_color='#f0f2f5', corner_radius=0)
        main_container.grid(row=1, column=0, sticky='nsew', padx=25, pady=20)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        # Columna izquierda - Formulario y Carrito
        self.crear_columna_izquierda(main_container)

        # Columna derecha - Lista de ventas
        self.crear_columna_derecha(main_container)

        # Botones principales
        self.crear_botones_principales(main_container)

    def crear_columna_izquierda(self, parent):
        """Crear columna izquierda con formulario y carrito"""
        left_column = ctk.CTkFrame(parent, fg_color='transparent')
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        left_column.grid_rowconfigure(1, weight=1)

        # Formulario
        self.crear_formulario(left_column)

        # Carrito
        self.crear_carrito(left_column)

    def crear_formulario(self, parent):
        """Crear formulario de venta moderno"""
        # Card del formulario
        form_card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                                border_width=1, border_color='#e9ecef')
        form_card.grid(row=0, column=0, sticky='ew', pady=(0, 15))

        # Header
        header_form = ctk.CTkFrame(form_card, fg_color='#667eea', height=50, corner_radius=10)
        header_form.pack(fill='x', padx=2, pady=2)
        header_form.pack_propagate(False)

        ctk.CTkLabel(header_form, text="📝 Nueva Venta",
                    font=("Segoe UI", 14, "bold"),
                    text_color='white').pack(expand=True)

        # Contenido
        form_content = ctk.CTkFrame(form_card, fg_color='white')
        form_content.pack(fill='x', padx=20, pady=20)

        # Variables
        self.numero_recibo_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.observaciones_var = tk.StringVar()

        # Generar número de recibo automáticamente
        self.generar_numero_recibo()

        # Número de Recibo (solo lectura)
        ctk.CTkLabel(form_content, text="🧾 Número de Recibo:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        recibo_entry = ctk.CTkEntry(form_content, textvariable=self.numero_recibo_var,
                                   font=("Segoe UI", 10, "bold"),
                                   height=32, corner_radius=8,
                                   border_width=1, border_color='#dee2e6',
                                   state='readonly',
                                   fg_color='#f8f9fa',
                                   text_color='#667eea')
        recibo_entry.pack(fill='x', pady=(0, 15))

        # Cliente
        ctk.CTkLabel(form_content, text="👤 Cliente:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        self.cliente_combo = ttk.Combobox(form_content, textvariable=self.cliente_var,
                                         state="readonly", font=("Segoe UI", 10))
        self.cliente_combo.pack(fill='x', pady=(0, 15), ipady=4)

        # Observaciones
        ctk.CTkLabel(form_content, text="📄 Observaciones:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        obs_entry = ctk.CTkEntry(form_content, textvariable=self.observaciones_var,
                                font=("Segoe UI", 10),
                                height=32, corner_radius=8,
                                border_width=1, border_color='#dee2e6')
        obs_entry.pack(fill='x', pady=(0, 15))

        # Divisor
        ctk.CTkFrame(form_content, fg_color='#e9ecef', height=2).pack(fill='x', pady=(5, 15))

        # Sección productos
        ctk.CTkLabel(form_content, text="🛒 Agregar Productos",
                    font=("Segoe UI", 12, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 10))

        # Producto
        ctk.CTkLabel(form_content, text="📦 Producto:",
                    font=("Segoe UI", 10, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        self.producto_combo = ttk.Combobox(form_content, textvariable=self.producto_var,
                                          state="readonly", font=("Segoe UI", 10))
        self.producto_combo.pack(fill='x', pady=(0, 15), ipady=4)
        self.producto_combo.bind('<<ComboboxSelected>>', self.producto_seleccionado)

        # Grid para cantidad y precio
        grid_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        grid_frame.pack(fill='x', pady=(0, 15))
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

        # Cantidad
        cantidad_frame = ctk.CTkFrame(grid_frame, fg_color='transparent')
        cantidad_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))

        ctk.CTkLabel(cantidad_frame, text="🔢 Cantidad:",
                    font=("Segoe UI", 10, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        cantidad_entry = ctk.CTkEntry(cantidad_frame, textvariable=self.cantidad_var,
                                     font=("Segoe UI", 10),
                                     height=32, corner_radius=8,
                                     border_width=1, border_color='#dee2e6')
        cantidad_entry.pack(fill='x')

        # Precio
        precio_frame = ctk.CTkFrame(grid_frame, fg_color='transparent')
        precio_frame.grid(row=0, column=1, sticky='ew')

        ctk.CTkLabel(precio_frame, text="💵 Precio Unit.:",
                    font=("Segoe UI", 10, "bold"),
                    text_color='#667eea').pack(anchor='w', pady=(0, 5))

        precio_entry = ctk.CTkEntry(precio_frame, textvariable=self.precio_var,
                                   font=("Segoe UI", 10),
                                   height=32, corner_radius=8,
                                   border_width=1, border_color='#dee2e6')
        precio_entry.pack(fill='x')

        # Botón agregar
        btn_agregar = ctk.CTkButton(form_content, text="+ Agregar al Carrito",
                                    fg_color='#27ae60',
                                    hover_color='#229954',
                                    font=("Segoe UI", 11, "bold"),
                                    height=38, corner_radius=10,
                                    command=self.agregar_al_carrito)
        btn_agregar.pack(fill='x', pady=(5, 0))

        # Cargar combos
        self.cargar_combos_iniciales()

    def crear_carrito(self, parent):
        """Crear carrito de compras moderno"""
        # Card del carrito
        cart_card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                                border_width=1, border_color='#e9ecef')
        cart_card.grid(row=1, column=0, sticky='nsew')

        # Header
        header_cart = ctk.CTkFrame(cart_card, fg_color='#667eea', height=50, corner_radius=10)
        header_cart.pack(fill='x', padx=2, pady=2)
        header_cart.pack_propagate(False)

        ctk.CTkLabel(header_cart, text="🛒 Carrito de Compras",
                    font=("Segoe UI", 14, "bold"),
                    text_color='white').pack(expand=True)

        # Container del treeview
        tree_container = tk.Frame(cart_card, bg='white')
        tree_container.pack(fill='both', expand=True, padx=15, pady=(10, 10))

        # Estilo
        style = ttk.Style()
        style.configure("Carrito.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=32)

        style.configure("Carrito.Treeview.Heading",
                       background="#667eea",
                       foreground="white",
                       font=("Segoe UI", 10, "bold"))

        # Treeview
        columns = ('Producto', 'Cant.', 'P.Unit', 'Subtotal')
        self.tree_carrito = ttk.Treeview(tree_container, columns=columns, show='headings',
                                        height=10, style="Carrito.Treeview")

        self.tree_carrito.heading('Producto', text='Producto')
        self.tree_carrito.heading('Cant.', text='Cant.')
        self.tree_carrito.heading('P.Unit', text='P.Unit')
        self.tree_carrito.heading('Subtotal', text='Subtotal')

        self.tree_carrito.column('Producto', width=180, anchor='w')
        self.tree_carrito.column('Cant.', width=60, anchor='center')
        self.tree_carrito.column('P.Unit', width=80, anchor='center')
        self.tree_carrito.column('Subtotal', width=90, anchor='center')

        # Scrollbar
        cart_scrollbar = ttk.Scrollbar(tree_container, orient='vertical',
                                      command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=cart_scrollbar.set)

        self.tree_carrito.pack(side='left', fill='both', expand=True)
        cart_scrollbar.pack(side='right', fill='y')

        # Panel inferior
        bottom_panel = ctk.CTkFrame(cart_card, fg_color='white')
        bottom_panel.pack(fill='x', padx=15, pady=(5, 15))

        # Botones
        btn_frame = ctk.CTkFrame(bottom_panel, fg_color='transparent')
        btn_frame.pack(side='left')

        btn_quitar = ctk.CTkButton(btn_frame, text="🗑️ Quitar",
                                  fg_color='#ff3838',
                                  hover_color='#e62020',
                                  font=("Segoe UI", 10, "bold"),
                                  width=100, height=32,
                                  corner_radius=8,
                                  command=self.quitar_del_carrito)
        btn_quitar.pack(side='left', padx=(0, 8))

        btn_limpiar = ctk.CTkButton(btn_frame, text="🧹 Limpiar",
                                   fg_color='#f39c12',
                                   hover_color='#e67e22',
                                   font=("Segoe UI", 10, "bold"),
                                   width=100, height=32,
                                   corner_radius=8,
                                   command=self.limpiar_carrito)
        btn_limpiar.pack(side='left')

        # Total
        total_frame = ctk.CTkFrame(bottom_panel, fg_color='#667eea', corner_radius=8)
        total_frame.pack(side='right')

        self.total_var = tk.StringVar(value="Total: $0")
        ctk.CTkLabel(total_frame, textvariable=self.total_var,
                    font=("Segoe UI", 12, "bold"),
                    text_color='white').pack(padx=15, pady=8)

    def crear_columna_derecha(self, parent):
        """Crear columna derecha con lista de ventas"""
        # Card de ventas
        ventas_card = ctk.CTkFrame(parent, fg_color='white', corner_radius=12,
                                  border_width=1, border_color='#e9ecef')
        ventas_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        # Header
        header_ventas = ctk.CTkFrame(ventas_card, fg_color='#667eea', height=50, corner_radius=10)
        header_ventas.pack(fill='x', padx=2, pady=2)
        header_ventas.pack_propagate(False)

        ctk.CTkLabel(header_ventas, text="📊 Historial de Ventas",
                    font=("Segoe UI", 14, "bold"),
                    text_color='white').pack(expand=True)

        # Info
        info_label = ctk.CTkLabel(ventas_card,
                                 text="💡 Doble clic para ver detalles de la venta",
                                 font=("Segoe UI", 9, "italic"),
                                 text_color='#6c757d')
        info_label.pack(pady=(10, 5))

        # Container del treeview
        tree_container = tk.Frame(ventas_card, bg='white')
        tree_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Estilo
        style = ttk.Style()
        style.configure("Ventas.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=35)

        style.configure("Ventas.Treeview.Heading",
                       background="#667eea",
                       foreground="white",
                       font=("Segoe UI", 10, "bold"))

        style.map('Ventas.Treeview',
                 background=[('selected', '#667eea')],
                 foreground=[('selected', 'white')])

        # Treeview
        columns = ('ID', 'Cliente', 'Total', 'Fecha', 'Observaciones')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="Ventas.Treeview")

        headers = {
            'ID': ('ID', 60),
            'Cliente': ('Cliente', 200),
            'Total': ('Total', 110),
            'Fecha': ('Fecha', 130),
            'Observaciones': ('Observaciones', 180)
        }

        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            anchor = 'center' if col in ['ID', 'Total'] else 'w'
            self.tree.column(col, width=width, anchor=anchor)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Evento doble clic
        self.tree.bind('<Double-1>', self.ver_detalle_venta)

    def crear_botones_principales(self, parent):
        """Crear botones principales"""
        botones_panel = ctk.CTkFrame(parent, fg_color='#f0f2f5', corner_radius=0)
        botones_panel.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        botones_container = ctk.CTkFrame(botones_panel, fg_color='transparent')
        botones_container.pack()

        # Botones
        botones = [
            ("✓ PROCESAR VENTA", '#27ae60', '#229954', self.procesar_venta, 180, 45),
            ("👁 Ver Detalle", '#00a8ff', '#0088cc', self.ver_detalle_venta, 140, 40),
            ("🗑️ Eliminar Venta", '#ff3838', '#e62020', self.eliminar_venta, 150, 40),
            ("🔄 Actualizar", '#9b59b6', '#8e44ad', self.cargar_ventas, 130, 40),
            ("✖ Cerrar", '#95a5a6', '#7f8c8d', self.cerrar_ventana, 120, 40)
        ]

        for texto, color, hover, comando, ancho, alto in botones:
            btn = ctk.CTkButton(botones_container, text=texto,
                               fg_color=color,
                               hover_color=hover,
                               font=("Segoe UI", 11, "bold"),
                               width=ancho, height=alto,
                               corner_radius=10,
                               command=comando)
            btn.pack(side='left', padx=8)

    def cargar_combos_iniciales(self):
        """Cargar datos en los combos"""
        try:
            # Clientes
            clientes_nombres = [f"{c.id} - {c.nombre} {c.apellido}" for c in self.clientes_disponibles]
            clientes_nombres.sort(key=lambda x: x.split(' - ')[1])
            self.cliente_combo['values'] = clientes_nombres

            # Productos
            from models.producto import Producto
            productos_todos = Producto.obtener_todos()
            productos_formateados = []

            for producto in productos_todos:
                sku_display = producto.sku if producto.sku else "SIN-SKU"
                formato = f"{producto.id} - {sku_display} - {producto.nombre} (Stock: {producto.stock}) - ${producto.precio_venta:.0f}"
                productos_formateados.append(formato)

            self.producto_combo['values'] = productos_formateados

        except Exception as e:
            print(f"ERROR al cargar combos: {str(e)}")
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

            self.carrito.append({
                'producto_id': producto_id,
                'producto': producto,
                'cantidad': cantidad,
                'precio': precio,
                'subtotal': subtotal
            })

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

            detalles_venta = []
            for item in self.carrito:
                detalles_venta.append({
                    'producto_id': item['producto_id'],
                    'cantidad': item['cantidad'],
                    'precio_unitario': item['precio']
                })

            if self.controller.crear_venta(cliente_id, detalles_venta, self.observaciones_var.get(), self.numero_recibo_var.get()):
                self.limpiar_formulario_venta()
                self.cargar_ventas()
                self.cargar_datos_iniciales()
                self.cargar_combos_iniciales()
                # Actualizar estadísticas después de registrar venta
                self.actualizar_estadisticas()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")

    def generar_numero_recibo(self):
        """Generar número de recibo automático"""
        try:
            numero_recibo = self.controller.generar_numero_recibo()
            self.numero_recibo_var.set(numero_recibo)
        except Exception as e:
            print(f"Error al generar número de recibo: {str(e)}")
            from datetime import datetime
            self.numero_recibo_var.set(f"REC-{datetime.now().strftime('%Y%m%d')}-0001")

    def limpiar_formulario_venta(self):
        """Limpiar formulario de venta"""
        self.cliente_var.set('')
        self.observaciones_var.set('')
        self.producto_var.set('')
        self.cantidad_var.set('')
        self.precio_var.set('')

        # Generar nuevo número de recibo
        self.generar_numero_recibo()

        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        self.carrito.clear()
        self.actualizar_total()

    def cargar_ventas(self):
        """Cargar ventas en la lista"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

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

                    if fila[5] and fila[6]:
                        cliente_nombre = f"{fila[5]} {fila[6]}"
                    else:
                        cliente_nombre = "Cliente no encontrado"

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
        """Ver detalle de venta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver su detalle")
            return

        item = self.tree.item(seleccion[0])
        venta_id = item['values'][0]

        self.mostrar_ventana_detalle_venta(venta_id)

    def mostrar_ventana_detalle_venta(self, venta_id):
        """Mostrar ventana con detalle de venta"""
        detalle_window = tk.Toplevel(self.ventana)
        detalle_window.title(f"Detalle de Venta #{venta_id}")
        detalle_window.geometry("1200x800")
        detalle_window.configure(bg='#f0f2f5')
        detalle_window.transient(self.ventana)
        detalle_window.grab_set()

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

        self.crear_header_detalle(detalle_window, venta_datos)
        self.crear_contenido_detalle(detalle_window, venta_datos)

    def obtener_datos_completos_venta(self, venta_id):
        """Obtener todos los datos relacionados con la venta"""
        from config.database import DatabaseManager
        db = DatabaseManager()

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

        query_detalle = '''
            SELECT dv.producto_id, dv.cantidad, dv.precio_unitario, dv.subtotal,
                   p.nombre, p.descripcion, p.categoria
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        '''
        productos = db.ejecutar_consulta(query_detalle, (venta_id,))

        query_cuenta = '''
            SELECT saldo_total, saldo_pendiente, fecha_ultima_actualizacion
            FROM cuentas_corrientes
            WHERE cliente_id = ? AND activa = 1
        '''
        cuenta_info = db.ejecutar_consulta(query_cuenta, (venta_data[1],))

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
        """Crear header para ventana de detalle"""
        header_frame = ctk.CTkFrame(parent, fg_color=("#667eea", "#764ba2"),
                                    height=100, corner_radius=0)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(expand=True)

        ctk.CTkLabel(title_frame, text=f"DETALLE DE VENTA #{datos['venta']['id']}",
                    font=("Segoe UI", 20, "bold"),
                    text_color='white').pack(expand=True)

        info_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        info_frame.pack()

        ctk.CTkLabel(info_frame, text=f"Cliente: {datos['venta']['cliente_nombre']}",
                    font=("Segoe UI", 12),
                    text_color='white').pack(side='left', padx=20)

        ctk.CTkLabel(info_frame, text=f"Total: ${datos['venta']['total']:,.2f}",
                    font=("Segoe UI", 12, "bold"),
                    text_color='#2ecc71').pack(side='left', padx=20)

        ctk.CTkLabel(info_frame, text=f"Fecha: {datos['venta']['fecha_venta']}",
                    font=("Segoe UI", 12),
                    text_color='white').pack(side='left', padx=20)

    def crear_contenido_detalle(self, parent, datos):
        """Crear contenido con pestañas"""
        main_frame = ctk.CTkFrame(parent, fg_color='#f0f2f5', corner_radius=0)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        self.crear_pestaña_productos_vendidos(notebook, datos)
        self.crear_pestaña_estado_cuenta(notebook, datos)
        self.crear_pestaña_info_cliente(notebook, datos)

    def crear_pestaña_productos_vendidos(self, notebook, datos):
        """Crear pestaña con productos vendidos"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🛒 Productos Vendidos")

        main_frame = ctk.CTkFrame(frame, fg_color='white', corner_radius=12,
                                 border_width=1, border_color='#e9ecef')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(main_frame, text="Productos incluidos en esta venta",
                    font=("Segoe UI", 14, "bold"),
                    text_color='#2c3e50').pack(pady=(15, 20))

        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        style = ttk.Style()
        style.configure("Detalle.Treeview",
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       font=("Segoe UI", 10),
                       rowheight=30)
        style.configure("Detalle.Treeview.Heading",
                       background="#667eea",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))

        columns = ('Producto', 'Categoría', 'Cantidad', 'Precio Unit.', 'Subtotal')
        tree_productos = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                     style="Detalle.Treeview")

        tree_productos.heading('Producto', text='Producto')
        tree_productos.heading('Categoría', text='Categoría')
        tree_productos.heading('Cantidad', text='Cantidad')
        tree_productos.heading('Precio Unit.', text='Precio Unit.')
        tree_productos.heading('Subtotal', text='Subtotal')

        tree_productos.column('Producto', width=200, anchor='w')
        tree_productos.column('Categoría', width=120, anchor='center')
        tree_productos.column('Cantidad', width=80, anchor='center')
        tree_productos.column('Precio Unit.', width=100, anchor='center')
        tree_productos.column('Subtotal', width=100, anchor='center')

        total_productos = 0
        for producto in datos['productos']:
            tree_productos.insert('', 'end', values=(
                producto[4],
                producto[6] or 'Sin categoría',
                f"{producto[1]:,}",
                f"${producto[2]:,.2f}",
                f"${producto[3]:,.2f}"
            ))
            total_productos += producto[1]

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree_productos.yview)
        tree_productos.configure(yscrollcommand=scrollbar.set)

        tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        resumen_frame = ctk.CTkFrame(main_frame, fg_color='#f8f9fa', corner_radius=8)
        resumen_frame.pack(fill='x', padx=15, pady=(0, 15))

        ctk.CTkLabel(resumen_frame, text=f"Total de productos: {total_productos:,}",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#2c3e50').pack(side='left', padx=15, pady=10)

        ctk.CTkLabel(resumen_frame, text=f"TOTAL VENTA: ${datos['venta']['total']:,.2f}",
                    font=("Segoe UI", 12, "bold"),
                    text_color='#27ae60').pack(side='right', padx=15, pady=10)

    def crear_pestaña_estado_cuenta(self, notebook, datos):
        """Crear pestaña con estado de cuenta"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="💳 Estado de Cuenta")

        main_frame = ctk.CTkFrame(frame, fg_color='white', corner_radius=12,
                                 border_width=1, border_color='#e9ecef')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(main_frame, text="Estado de cuenta del cliente",
                    font=("Segoe UI", 14, "bold"),
                    text_color='#2c3e50').pack(pady=(15, 20))

        estado_frame = ctk.CTkFrame(main_frame, fg_color='white')
        estado_frame.pack(fill='x', padx=15, pady=(0, 20))

        saldo_total = datos['cuenta'][0]
        saldo_pendiente = datos['cuenta'][1]
        saldo_abonado = saldo_total - saldo_pendiente

        # Cards
        tarjetas = [
            ("SALDO TOTAL", f"${saldo_total:,.2f}", '#3498db'),
            ("ABONADO", f"${saldo_abonado:,.2f}", '#27ae60'),
            ("PENDIENTE", f"${saldo_pendiente:,.2f}", '#e74c3c')
        ]

        for titulo, valor, color in tarjetas:
            card = ctk.CTkFrame(estado_frame, fg_color=color, corner_radius=10)
            card.pack(side='left', fill='both', expand=True, padx=10)

            ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 10, "bold"),
                        text_color='white').pack(pady=(15, 5))
            ctk.CTkLabel(card, text=valor, font=("Segoe UI", 16, "bold"),
                        text_color='white').pack(pady=(0, 15))

        if datos['abonos']:
            ctk.CTkLabel(main_frame, text="Últimos abonos realizados",
                        font=("Segoe UI", 12, "bold"),
                        text_color='#2c3e50').pack(pady=(20, 10))

            abonos_frame = tk.Frame(main_frame, bg='white')
            abonos_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

            columns_abonos = ('Fecha', 'Monto', 'Método', 'Descripción', 'Recibo')
            tree_abonos = ttk.Treeview(abonos_frame, columns=columns_abonos, show='headings',
                                      style="Detalle.Treeview", height=8)

            tree_abonos.heading('Fecha', text='Fecha')
            tree_abonos.heading('Monto', text='Monto')
            tree_abonos.heading('Método', text='Método')
            tree_abonos.heading('Descripción', text='Descripción')
            tree_abonos.heading('Recibo', text='Recibo #')

            tree_abonos.column('Fecha', width=120, anchor='center')
            tree_abonos.column('Monto', width=100, anchor='center')
            tree_abonos.column('Método', width=100, anchor='center')
            tree_abonos.column('Descripción', width=200, anchor='w')
            tree_abonos.column('Recibo', width=100, anchor='center')

            for abono in datos['abonos']:
                tree_abonos.insert('', 'end', values=(
                    abono[3][:10] if abono[3] else '',
                    f"${abono[0]:,.2f}",
                    abono[1] or 'Efectivo',
                    abono[2] or '',
                    abono[4] or ''
                ))

            scrollbar_abonos = ttk.Scrollbar(abonos_frame, orient='vertical', command=tree_abonos.yview)
            tree_abonos.configure(yscrollcommand=scrollbar_abonos.set)

            tree_abonos.pack(side='left', fill='both', expand=True)
            scrollbar_abonos.pack(side='right', fill='y')
        else:
            ctk.CTkLabel(main_frame, text="No hay abonos registrados para este cliente",
                        font=("Segoe UI", 11, "italic"),
                        text_color='#6c757d').pack(pady=30)

    def crear_pestaña_info_cliente(self, notebook, datos):
        """Crear pestaña con información del cliente"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="👤 Info. Cliente")

        main_frame = ctk.CTkFrame(frame, fg_color='white', corner_radius=12,
                                 border_width=1, border_color='#e9ecef')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(main_frame, text="Información del cliente",
                    font=("Segoe UI", 14, "bold"),
                    text_color='#2c3e50').pack(pady=(15, 30))

        info_frame = ctk.CTkFrame(main_frame, fg_color='white')
        info_frame.pack(expand=True)

        venta = datos['venta']

        info_data = [
            ("Nombre completo:", venta['cliente_nombre']),
            ("Teléfono:", venta['cliente_telefono'] or "No registrado"),
            ("Email:", venta['cliente_email'] or "No registrado"),
            ("Dirección:", venta['cliente_direccion'] or "No registrada"),
        ]

        for label, value in info_data:
            row_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=8)

            ctk.CTkLabel(row_frame, text=label, font=('Segoe UI', 11, 'bold'),
                        text_color='#2c3e50').pack(side='left', anchor='w')
            ctk.CTkLabel(row_frame, text=value, font=('Segoe UI', 11),
                        text_color='#34495e').pack(side='left', padx=(20, 0))

        ctk.CTkLabel(main_frame, text="Información de esta venta",
                    font=("Segoe UI", 12, "bold"),
                    text_color='#2c3e50').pack(pady=(40, 20))

        venta_info_frame = ctk.CTkFrame(main_frame, fg_color='#f8f9fa', corner_radius=8)
        venta_info_frame.pack(fill='x', padx=15, pady=(0, 15))

        venta_data = [
            ("ID de venta:", f"#{venta['id']}"),
            ("Fecha de venta:", venta['fecha_venta']),
            ("Observaciones:", venta['observaciones'] or "Ninguna"),
        ]

        for label, value in venta_data:
            row_frame = ctk.CTkFrame(venta_info_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=5, padx=15)

            ctk.CTkLabel(row_frame, text=label, font=('Segoe UI', 10, 'bold'),
                        text_color='#2c3e50').pack(side='left')
            ctk.CTkLabel(row_frame, text=value, font=('Segoe UI', 10),
                        text_color='#34495e').pack(side='left', padx=(10, 0))

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
