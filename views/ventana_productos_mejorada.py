"""
Ventana para gestión de productos - Diseño Moderno Mejorado con CustomTkinter
Versión con estilos unificados
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.producto_controller import ProductoController
from config.estilos import (Colores, Fuentes, Espaciado, Dimensiones,
                            Iconos, obtener_color_hover, estilo_entry, estilo_card)

class VentanaProductos:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProductoController()
        self.ventana = None
        self.tree = None
        self.style = ttk.Style()
        self.crear_ventana()

    def crear_ventana(self):
        """Crear ventana con diseño moderno CustomTkinter"""
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Productos - Sistema Pro")
        self.ventana.geometry("1500x900")
        self.ventana.configure(bg=Colores.BG_PRIMARY)
        self.ventana.resizable(True, True)

        # Modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Crear interfaz moderna
        self.crear_header_web()
        self.crear_contenido_web()
        self.cargar_productos()

    def crear_header_web(self):
        """Header estilo web moderno con CustomTkinter"""
        # Header principal con gradiente
        header = ctk.CTkFrame(
            self.ventana,
            fg_color=(Colores.PRIMARY_START, Colores.PRIMARY_END),
            height=Dimensiones.FOOTER_HEIGHT,
            corner_radius=0
        )
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Título con icono
        title_label = ctk.CTkLabel(
            header,
            text=f"{Iconos.PRODUCTOS} INVENTARIO",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.LARGE, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        title_label.grid(row=0, column=0, sticky='w', padx=Espaciado.LARGE, pady=Espaciado.NORMAL)

        # Barra de búsqueda moderna con CTkEntry
        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_productos)

        search_entry = ctk.CTkEntry(
            header,
            textvariable=self.buscar_var,
            placeholder_text=f"{Iconos.BUSCAR} Buscar productos...",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
            width=280,
            height=Dimensiones.ENTRY_HEIGHT,
            corner_radius=Dimensiones.RADIUS_SMALL,
            border_width=0,
            fg_color=Colores.BG_SECONDARY,
            text_color=Colores.TEXT_PRIMARY
        )
        search_entry.grid(row=0, column=1, sticky='e', padx=Espaciado.LARGE, pady=Espaciado.NORMAL)

    def crear_contenido_web(self):
        """Contenido principal estilo web con CustomTkinter"""
        # Container principal
        main_container = ctk.CTkFrame(self.ventana, fg_color=Colores.BG_PRIMARY, corner_radius=0)
        main_container.grid(row=1, column=0, sticky='nsew', padx=Espaciado.MEDIO, pady=Espaciado.MEDIO)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        # Panel izquierdo - Formulario
        self.crear_panel_formulario(main_container)

        # Panel derecho - Lista de productos
        self.crear_panel_lista(main_container)

    def crear_panel_formulario(self, parent):
        """Panel de formulario estilo card web con CustomTkinter"""
        # Card container
        form_card = ctk.CTkFrame(
            parent,
            **estilo_card()
        )
        form_card.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0, Espaciado.NORMAL))
        form_card.grid_rowconfigure(1, weight=1)

        # Header del card
        card_header = ctk.CTkFrame(
            form_card,
            fg_color=Colores.PRIMARY_START,
            height=50,
            corner_radius=Dimensiones.RADIUS_NORMAL
        )
        card_header.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        card_header.grid_propagate(False)

        ctk.CTkLabel(
            card_header,
            text=f"{Iconos.EDITAR} Información del Producto",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(pady=12)

        # Contenido del formulario
        form_content = ctk.CTkFrame(form_card, fg_color=Colores.BG_CARD, corner_radius=0)
        form_content.grid(row=1, column=0, sticky='nsew', padx=Espaciado.MEDIO, pady=Espaciado.MEDIO)

        # Variables del formulario
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_compra_var = tk.StringVar()
        self.precio_venta_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.stock_minimo_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.proveedor_var = tk.StringVar()

        # Crear campos del formulario
        self.crear_campos_formulario(form_content)

        # Botones de acción
        self.crear_botones_accion(form_card)

        # Variables para edición
        self.modo_edicion = False
        self.producto_editando_id = None

    def crear_campos_formulario(self, parent):
        """Crear campos de formulario con CustomTkinter"""
        row = 0

        # Función para crear campo
        def crear_campo(label_text, var, width=160):
            nonlocal row

            # Label
            ctk.CTkLabel(
                parent,
                text=label_text,
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.BOLD),
                text_color=Colores.PRIMARY_START
            ).grid(row=row, column=0, sticky='w', pady=(Espaciado.PEQUENO if row > 0 else 0, Espaciado.MINI))

            # Entry con CustomTkinter usando estilos
            entry_config = estilo_entry()
            entry = ctk.CTkEntry(
                parent,
                textvariable=var,
                width=width,
                **entry_config
            )
            entry.grid(row=row+1, column=0, sticky='w', pady=(0, Espaciado.MUY_PEQUENO))

            row += 2
            return entry

        # Campos principales (ancho compacto)
        crear_campo(f"{Iconos.DOCUMENTO} Nombre del Producto", self.nombre_var, 240)
        crear_campo(f"{Iconos.ETIQUETA} Marca", self.marca_var, 180)
        crear_campo("📂 Categoría", self.categoria_var, 180)
        crear_campo("🔧 Tipo", self.tipo_var, 180)
        crear_campo(f"{Iconos.DINERO} Precio de Compra", self.precio_compra_var, 140)
        crear_campo(f"{Iconos.DINERO} Precio de Venta", self.precio_venta_var, 140)
        crear_campo(f"{Iconos.PRODUCTOS} Stock Actual", self.stock_var, 120)
        crear_campo(f"{Iconos.ADVERTENCIA} Stock Mínimo", self.stock_minimo_var, 120)
        crear_campo("🏭 Proveedor", self.proveedor_var, 200)
        crear_campo(f"{Iconos.DOCUMENTO} Descripción", self.descripcion_var, 260)

    def crear_botones_accion(self, parent):
        """Botones de acción con CustomTkinter"""
        # Container de botones
        btn_container = ctk.CTkFrame(parent, fg_color=Colores.BG_CARD, corner_radius=0)
        btn_container.grid(row=2, column=0, sticky='ew', padx=Espaciado.MEDIO, pady=(Espaciado.PEQUENO, Espaciado.MEDIO))

        # Función para crear botón CTk moderno
        def crear_boton_ctk(texto, color, comando, icono=""):
            btn = ctk.CTkButton(
                btn_container,
                text=f"{icono} {texto}",
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
                fg_color=color,
                hover_color=obtener_color_hover(color),
                width=260,
                height=Dimensiones.BUTTON_HEIGHT_SMALL,
                corner_radius=Dimensiones.RADIUS_NORMAL,
                border_width=0,
                command=comando
            )
            btn.pack(fill='x', pady=Espaciado.MUY_PEQUENO)
            return btn

        # Botones principales
        crear_boton_ctk("Guardar Producto", Colores.INFO, self.guardar_producto, Iconos.GUARDAR)
        crear_boton_ctk("Actualizar Producto", Colores.WARNING, self.actualizar_producto, Iconos.EDITAR)
        crear_boton_ctk("Eliminar Producto", Colores.DANGER, self.eliminar_producto, Iconos.ELIMINAR)
        crear_boton_ctk("Limpiar Formulario", Colores.GRIS_MEDIO, self.limpiar_formulario, Iconos.LIMPIAR)
        crear_boton_ctk("Generar SKUs", Colores.SUCCESS, self.generar_skus, Iconos.ETIQUETA)

    def crear_panel_lista(self, parent):
        """Panel de lista de productos con CustomTkinter"""
        # Card de lista
        list_card = ctk.CTkFrame(
            parent,
            **estilo_card()
        )
        list_card.grid(row=0, column=1, rowspan=2, sticky='nsew')
        list_card.grid_rowconfigure(1, weight=1)
        list_card.grid_columnconfigure(0, weight=1)

        # Header de la lista
        list_header = ctk.CTkFrame(
            list_card,
            fg_color=Colores.PRIMARY_START,
            height=50,
            corner_radius=Dimensiones.RADIUS_NORMAL
        )
        list_header.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        list_header.grid_propagate(False)

        ctk.CTkLabel(
            list_header,
            text=f"{Iconos.REPORTES} Inventario de Productos",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(pady=12)

        # Divisor
        ctk.CTkFrame(list_card, fg_color=Colores.BORDER_LIGHT, height=2).grid(
            row=0, column=0, sticky='ew', padx=Espaciado.MEDIO, pady=(52, 0))

        # Container del treeview
        tree_container = tk.Frame(list_card, bg=Colores.BG_CARD)
        tree_container.grid(row=1, column=0, sticky='nsew', padx=Espaciado.MEDIO, pady=(Espaciado.PEQUENO, Espaciado.MEDIO))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configurar estilo del treeview
        self.configurar_estilo_treeview()

        # Crear treeview
        columns = ('ID', 'SKU', 'Nombre', 'Marca', 'Tipo', 'Categoría', 'P.Compra', 'P.Venta', 'Stock', 'Mín', 'Estado')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="WebModern.Treeview", height=20)

        # Configurar columnas
        headers = {
            'ID': ('ID', 50), 'SKU': ('SKU', 80), 'Nombre': ('Producto', 180),
            'Marca': ('Marca', 100), 'Tipo': ('Tipo', 90), 'Categoría': ('Categoría', 100),
            'P.Compra': ('P. Compra', 90), 'P.Venta': ('P. Venta', 90),
            'Stock': ('Stock', 70), 'Mín': ('Mín', 60), 'Estado': ('Estado', 100)
        }

        for col, (header, width) in headers.items():
            self.tree.heading(col, text=header)
            if col in ['P.Compra', 'P.Venta', 'Stock', 'Mín']:
                anchor = 'center'
            else:
                anchor = 'w'
            self.tree.column(col, width=width, anchor=anchor, minwidth=50)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Eventos
        self.tree.bind('<Double-1>', self.seleccionar_producto)

    def configurar_estilo_treeview(self):
        """Configurar estilo web del treeview"""
        self.style.configure("WebModern.Treeview",
                           background=Colores.BG_SECONDARY,
                           foreground=Colores.TEXT_PRIMARY,
                           fieldbackground=Colores.BG_SECONDARY,
                           font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO),
                           rowheight=35)

        self.style.configure("WebModern.Treeview.Heading",
                           background=Colores.SECONDARY,
                           foreground=Colores.TEXT_WHITE,
                           font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
                           relief="flat",
                           borderwidth=0,
                           focuscolor="none")

        # Colores de selección
        self.style.map("WebModern.Treeview",
                      background=[('selected', Colores.PRIMARY_START)],
                      foreground=[('selected', Colores.TEXT_WHITE)])

    def buscar_productos(self, *args):
        """Buscar productos"""
        # Verificar que el treeview esté inicializado
        if not self.tree:
            return

        termino = self.buscar_var.get()
        if termino == "Buscar productos...":
            termino = ""

        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not termino:
            self.cargar_productos()
            return

        try:
            productos = self.controller.buscar_productos(termino)
            for producto in productos:
                sku_display = getattr(producto, 'sku', 'SIN-SKU')

                if producto.stock <= 0:
                    estado = "Agotado"
                    tags = ('agotado',)
                elif producto.necesita_restock():
                    estado = "Stock Bajo"
                    tags = ('bajo_stock',)
                else:
                    estado = "Disponible"
                    tags = ('normal',)

                self.tree.insert('', 'end', values=(
                    producto.id, sku_display, producto.nombre,
                    producto.marca or '', producto.tipo or '', producto.categoria or '',
                    f"${producto.precio_compra:.0f}", f"${producto.precio_venta:.0f}",
                    producto.stock, producto.stock_minimo, estado
                ), tags=tags)

            self.configurar_colores_filas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {str(e)}")

    def cargar_productos(self):
        """Cargar productos en el treeview"""
        # Verificar que el treeview esté inicializado
        if not self.tree:
            return

        try:
            # Limpiar lista actual
            for item in self.tree.get_children():
                self.tree.delete(item)

            productos = self.controller.obtener_todos_productos()

            for producto in productos:
                sku_display = getattr(producto, 'sku', 'SIN-SKU')

                if producto.stock <= 0:
                    estado = "Agotado"
                    tags = ('agotado',)
                elif producto.necesita_restock():
                    estado = "Stock Bajo"
                    tags = ('bajo_stock',)
                else:
                    estado = "Disponible"
                    tags = ('normal',)

                self.tree.insert('', 'end', values=(
                    producto.id, sku_display, producto.nombre,
                    producto.marca or '', producto.tipo or '', producto.categoria or '',
                    f"${producto.precio_compra:.0f}", f"${producto.precio_venta:.0f}",
                    producto.stock, producto.stock_minimo, estado
                ), tags=tags)

            self.configurar_colores_filas()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")

    def configurar_colores_filas(self):
        """Configurar colores de filas según estado"""
        self.tree.tag_configure('bajo_stock', background=Colores.ALERT_WARNING_BG, foreground=Colores.ALERT_WARNING_TEXT)
        self.tree.tag_configure('agotado', background=Colores.ALERT_DANGER_BG, foreground=Colores.ALERT_DANGER_TEXT)
        self.tree.tag_configure('normal', background=Colores.ALERT_INFO_BG, foreground=Colores.ALERT_INFO_TEXT)

    def seleccionar_producto(self, event):
        """Seleccionar producto para edición"""
        item = self.tree.selection()[0]
        producto_id = self.tree.item(item, 'values')[0]

        try:
            producto = self.controller.obtener_producto_por_id(int(producto_id))
            if producto:
                self.cargar_datos_formulario(producto)
                self.modo_edicion = True
                self.producto_editando_id = producto.id
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar producto: {str(e)}")

    def cargar_datos_formulario(self, producto):
        """Cargar datos del producto en el formulario"""
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria or '')
        self.precio_compra_var.set(str(producto.precio_compra))
        self.precio_venta_var.set(str(producto.precio_venta))
        self.stock_var.set(str(producto.stock))
        self.stock_minimo_var.set(str(producto.stock_minimo))
        self.descripcion_var.set(producto.descripcion or '')
        self.marca_var.set(getattr(producto, 'marca', '') or '')
        self.tipo_var.set(getattr(producto, 'tipo', '') or '')
        self.proveedor_var.set(getattr(producto, 'proveedor', '') or '')

    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_var.set('')
        self.categoria_var.set('')
        self.precio_compra_var.set('')
        self.precio_venta_var.set('')
        self.stock_var.set('')
        self.stock_minimo_var.set('')
        self.descripcion_var.set('')
        self.marca_var.set('')
        self.tipo_var.set('')
        self.proveedor_var.set('')
        self.modo_edicion = False
        self.producto_editando_id = None

    def guardar_producto(self):
        """Guardar nuevo producto"""
        if self.modo_edicion:
            messagebox.showwarning("Advertencia", "Use 'Actualizar Producto' para modificar el producto seleccionado")
            return

        try:
            datos = {
                'nombre': self.nombre_var.get(),
                'descripcion': self.descripcion_var.get(),
                'precio_compra': self.precio_compra_var.get() or '0',
                'precio_venta': self.precio_venta_var.get() or '0',
                'stock': self.stock_var.get() or '0',
                'stock_minimo': self.stock_minimo_var.get() or '5',
                'categoria': self.categoria_var.get(),
                'marca': self.marca_var.get(),
                'tipo': self.tipo_var.get(),
                'proveedor': self.proveedor_var.get()
            }
            resultado = self.controller.crear_producto(datos)

            if resultado:
                messagebox.showinfo("Éxito", "Producto guardado correctamente")
                self.limpiar_formulario()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo guardar el producto")

        except ValueError as e:
            messagebox.showerror("Error", "Por favor, verifique que los precios y cantidades sean números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def actualizar_producto(self):
        """Actualizar producto existente"""
        if not self.modo_edicion:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la lista para actualizar")
            return

        try:
            datos = {
                'nombre': self.nombre_var.get(),
                'descripcion': self.descripcion_var.get(),
                'precio_compra': self.precio_compra_var.get() or '0',
                'precio_venta': self.precio_venta_var.get() or '0',
                'stock': self.stock_var.get() or '0',
                'stock_minimo': self.stock_minimo_var.get() or '5',
                'categoria': self.categoria_var.get(),
                'marca': self.marca_var.get(),
                'tipo': self.tipo_var.get(),
                'proveedor': self.proveedor_var.get()
            }
            resultado = self.controller.actualizar_producto(self.producto_editando_id, datos)

            if resultado:
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                self.limpiar_formulario()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")

        except ValueError:
            messagebox.showerror("Error", "Por favor, verifique que los precios y cantidades sean números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")

    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        if not self.modo_edicion:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la lista para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar",
                                       f"¿Está seguro de eliminar el producto?\n\nEsta acción no se puede deshacer.")
        if respuesta:
            try:
                resultado = self.controller.eliminar_producto(self.producto_editando_id)
                if resultado:
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.limpiar_formulario()
                    self.cargar_productos()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el producto")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def generar_skus(self):
        """Generar SKUs para productos sin SKU"""
        try:
            productos_actualizados = self.controller.generar_skus_faltantes()
            if productos_actualizados > 0:
                messagebox.showinfo("Éxito", f"Se generaron SKUs para {productos_actualizados} productos")
                self.cargar_productos()
            else:
                messagebox.showinfo("Información", "Todos los productos ya tienen SKU asignado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar SKUs: {str(e)}")
