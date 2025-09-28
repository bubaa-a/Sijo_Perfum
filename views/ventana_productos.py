"""
Ventana para gestión de productos - Diseño moderno y funcional
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController

class VentanaProductos:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProductoController()
        self.ventana = None
        self.tree = None
        self.crear_ventana()

    def crear_ventana(self):
        """Crear la ventana de productos con diseño moderno"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Productos - Sistema Empresarial Pro")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg='#f8f9fa')

        # Hacer que la ventana sea modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Configurar el grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Crear interfaz
        self.crear_header_moderno()
        self.crear_contenido_principal()

        # Cargar productos
        self.cargar_productos()

    def crear_header_moderno(self):
        """Crear header atractivo con búsqueda"""
        # Header principal
        header_frame = tk.Frame(self.ventana, bg='#2c3e50', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Icono y título
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.grid(row=0, column=0, sticky='w', padx=30, pady=20)

        # Título principal
        tk.Label(title_frame, text="PRODUCTOS",
                font=("Segoe UI", 24, "bold"), fg='#ecf0f1', bg='#2c3e50').pack()

        # Subtítulo
        tk.Label(title_frame, text="Gestión completa de inventario",
                font=("Segoe UI", 12), fg='#bdc3c7', bg='#2c3e50').pack()

        # Panel de búsqueda
        search_frame = tk.Frame(header_frame, bg='#34495e')
        search_frame.grid(row=0, column=1, sticky='e', padx=30, pady=20)

        tk.Label(search_frame, text="Buscar Producto:",
                font=("Segoe UI", 11, "bold"), fg='#ecf0f1', bg='#34495e').pack()

        # Entry de búsqueda con estilo
        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_productos)

        search_entry = tk.Entry(search_frame, textvariable=self.buscar_var,
                               font=("Segoe UI", 12), width=30, relief='flat',
                               bg='white', fg='#2c3e50', insertbackground='#2c3e50')
        search_entry.pack(pady=(5, 0), ipady=8)


    def crear_contenido_principal(self):
        """Crear el contenido principal con formulario y lista"""
        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg='#f8f9fa')
        main_container.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Crear formulario
        self.crear_formulario_moderno(main_container)

        # Crear lista de productos
        self.crear_lista_moderna(main_container)

        # Crear botones
        self.crear_botones_modernos(main_container)

    def crear_formulario_moderno(self, parent):
        """Crear formulario atractivo"""
        # Frame del formulario
        form_frame = tk.LabelFrame(parent, text="  Información del Producto  ",
                                  font=("Segoe UI", 14, "bold"), fg='#2c3e50',
                                  bg='white', relief='raised', bd=2)
        form_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        form_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

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

        # Estilo para labels y entries
        label_style = {'font': ('Segoe UI', 10, 'bold'), 'fg': '#34495e', 'bg': 'white'}
        entry_style = {'font': ('Segoe UI', 11), 'relief': 'solid', 'bd': 1, 'bg': '#f8f9fa'}

        # Primera fila
        tk.Label(form_frame, text="Nombre del Producto:", **label_style).grid(
            row=0, column=0, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.nombre_var, width=25, **entry_style).grid(
            row=1, column=0, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Categoría:", **label_style).grid(
            row=0, column=1, sticky='w', padx=15, pady=(15, 5))
        categoria_combo = ttk.Combobox(form_frame, textvariable=self.categoria_var, width=22,
                                      font=('Segoe UI', 11))
        categoria_combo['values'] = ('Electrónicos', 'Ropa', 'Hogar', 'Deportes', 'Libros', 'Otros')
        categoria_combo.grid(row=1, column=1, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Stock Actual:", **label_style).grid(
            row=0, column=2, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.stock_var, width=15, **entry_style).grid(
            row=1, column=2, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Stock Mínimo:", **label_style).grid(
            row=0, column=3, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.stock_minimo_var, width=15, **entry_style).grid(
            row=1, column=3, sticky='ew', padx=15, pady=(0, 15))

        # Segunda fila
        tk.Label(form_frame, text="Precio de Compra:", **label_style).grid(
            row=2, column=0, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.precio_compra_var, width=25, **entry_style).grid(
            row=3, column=0, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Precio de Venta:", **label_style).grid(
            row=2, column=1, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.precio_venta_var, width=22, **entry_style).grid(
            row=3, column=1, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Descripción:", **label_style).grid(
            row=2, column=2, columnspan=2, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.descripcion_var, width=40, **entry_style).grid(
            row=3, column=2, columnspan=2, sticky='ew', padx=15, pady=(0, 15))

        # Tercera fila - Nuevos campos
        tk.Label(form_frame, text="Marca:", **label_style).grid(
            row=4, column=0, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.marca_var, width=25, **entry_style).grid(
            row=5, column=0, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Tipo:", **label_style).grid(
            row=4, column=1, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.tipo_var, width=22, **entry_style).grid(
            row=5, column=1, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Proveedor:", **label_style).grid(
            row=4, column=2, columnspan=2, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.proveedor_var, width=40, **entry_style).grid(
            row=5, column=2, columnspan=2, sticky='ew', padx=15, pady=(0, 15))

        # Variables para modo edición
        self.modo_edicion = False
        self.producto_editando_id = None

    def crear_lista_moderna(self, parent):
        """Crear lista atractiva de productos"""
        # Frame de la lista
        list_frame = tk.LabelFrame(parent, text="  Inventario de Productos  ",
                                  font=("Segoe UI", 14, "bold"), fg='#2c3e50',
                                  bg='white', relief='raised', bd=2)
        list_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 15))
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Info header
        info_frame = tk.Frame(list_frame, bg='white')
        info_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=10)

        tk.Label(info_frame, text="Haga doble clic en un producto para editarlo",
                font=("Segoe UI", 10, "italic"), fg='#7f8c8d', bg='white').pack(side='left')

        # Container del treeview
        tree_container = tk.Frame(list_frame, bg='white')
        tree_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configurar estilo moderno
        style = ttk.Style()
        style.configure("Modern.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=35)
        style.configure("Modern.Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Marca', 'Tipo', 'Categoría', 'Proveedor', 'P.Compra', 'P.Venta', 'Stock', 'Mín', 'Estado')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="Modern.Treeview")

        # Configurar columnas
        headers = {
            'ID': ('ID', 50),
            'Nombre': ('Producto', 180),
            'Marca': ('Marca', 100),
            'Tipo': ('Tipo', 100),
            'Categoría': ('Categoría', 100),
            'Proveedor': ('Proveedor', 120),
            'P.Compra': ('P. Compra', 90),
            'P.Venta': ('P. Venta', 90),
            'Stock': ('Stock', 70),
            'Mín': ('Mín', 60),
            'Estado': ('Estado', 90)
        }

        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center' if col in ['Stock', 'Mín', 'ID'] else 'w')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout para scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Eventos
        self.tree.bind('<Double-1>', self.seleccionar_producto)

    def crear_botones_modernos(self, parent):
        """Crear botones atractivos"""
        # Frame de botones
        buttons_frame = tk.Frame(parent, bg='#f8f9fa')
        buttons_frame.grid(row=2, column=0, sticky='ew')

        # Contenedor centrado
        center_frame = tk.Frame(buttons_frame, bg='#f8f9fa')
        center_frame.pack(expand=True)

        # Función para crear botones modernos
        def crear_boton(texto, color, comando, icono=""):
            btn = tk.Button(center_frame, text=f"{icono} {texto}",
                           font=("Segoe UI", 11, "bold"), fg='white', bg=color,
                           relief='flat', cursor='hand2', padx=20, pady=10,
                           command=comando)
            btn.pack(side='left', padx=8)

            # Efectos hover
            def on_enter(e):
                btn.configure(relief='raised', bg=self.darken_color(color))
            def on_leave(e):
                btn.configure(relief='flat', bg=color)

            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            return btn

        # Botones principales
        crear_boton("Nuevo", "#27ae60", self.nuevo_producto, "➕")
        crear_boton("Guardar", "#3498db", self.guardar_producto, "💾")
        crear_boton("Editar", "#f39c12", self.editar_producto, "✏️")
        crear_boton("Eliminar", "#e74c3c", self.eliminar_producto, "🗑️")
        crear_boton("Actualizar", "#9b59b6", self.cargar_productos, "🔄")
        crear_boton("Cerrar", "#95a5a6", self.cerrar_ventana, "❌")

    def darken_color(self, color):
        """Oscurecer un color para efecto hover"""
        color_map = {
            "#27ae60": "#219a52",
            "#3498db": "#2980b9",
            "#f39c12": "#e67e22",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad",
            "#95a5a6": "#7f8c8d"
        }
        return color_map.get(color, color)

    def cargar_productos(self):
        """Cargar productos en la lista"""
        try:
            # Limpiar lista
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener productos
            productos = self.controller.obtener_todos_productos()

            # Agregar productos a la lista
            for producto in productos:
                ganancia = f"${producto.calcular_ganancia():.2f}"

                # Cambiar color si stock bajo
                tags = ('normal',)
                if producto.necesita_restock():
                    tags = ('bajo_stock',)
                elif producto.stock <= 0:
                    tags = ('agotado',)

                # Determinar estado
                if producto.stock <= 0:
                    estado = "Agotado"
                elif producto.necesita_restock():
                    estado = "Stock Bajo"
                else:
                    estado = "Disponible"

                self.tree.insert('', 'end', values=(
                    producto.id,
                    producto.nombre,
                    producto.marca or '',
                    producto.tipo or '',
                    producto.categoria or '',
                    producto.proveedor or '',
                    f"${producto.precio_compra:.2f}",
                    f"${producto.precio_venta:.2f}",
                    producto.stock,
                    producto.stock_minimo,
                    estado
                ), tags=tags)

            # Configurar colores
            self.tree.tag_configure('bajo_stock', background='#fff3cd')
            self.tree.tag_configure('agotado', background='#f8d7da')
            self.tree.tag_configure('normal', background='#d4edda')

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")

    def buscar_productos(self, *args):
        """Buscar productos"""
        termino = self.buscar_var.get()

        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Buscar productos
        if termino.strip():
            productos = self.controller.buscar_productos(termino)
        else:
            productos = self.controller.obtener_todos_productos()

        # Mostrar resultados
        for producto in productos:
            ganancia = f"${producto.calcular_ganancia():.2f}"

            tags = ('normal',)
            if producto.necesita_restock():
                tags = ('bajo_stock',)
            elif producto.stock <= 0:
                tags = ('agotado',)

            # Determinar estado
            if producto.stock <= 0:
                estado = "❌ Agotado"
            elif producto.necesita_restock():
                estado = "⚠️ Stock Bajo"
            else:
                estado = "✅ Disponible"

            self.tree.insert('', 'end', values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                f"${producto.precio_compra:.2f}",
                f"${producto.precio_venta:.2f}",
                producto.stock,
                producto.stock_minimo,
                ganancia,
                estado
            ), tags=tags)

        # Configurar colores
        self.tree.tag_configure('bajo_stock', background='#fff3cd')
        self.tree.tag_configure('agotado', background='#f8d7da')
        self.tree.tag_configure('normal', background='#d4edda')

    def seleccionar_producto(self, event):
        """Manejar selección de producto"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            # Llenar formulario
            self.nombre_var.set(valores[1])
            self.categoria_var.set(valores[2])
            self.precio_compra_var.set(valores[3].replace('$', ''))
            self.precio_venta_var.set(valores[4].replace('$', ''))
            self.stock_var.set(valores[5])
            self.stock_minimo_var.set(valores[6])

            # Obtener descripción del producto
            from models.producto import Producto
            producto = Producto.buscar_por_id(valores[0])
            if producto:
                self.descripcion_var.set(producto.descripcion or "")

    def nuevo_producto(self):
        """Preparar para nuevo producto"""
        self.limpiar_formulario()
        self.modo_edicion = False
        self.producto_editando_id = None

    def guardar_producto(self):
        """Guardar producto"""
        datos = {
            'nombre': self.nombre_var.get(),
            'categoria': self.categoria_var.get(),
            'descripcion': self.descripcion_var.get(),
            'precio_compra': self.precio_compra_var.get(),
            'precio_venta': self.precio_venta_var.get(),
            'stock': self.stock_var.get(),
            'stock_minimo': self.stock_minimo_var.get(),
            'marca': self.marca_var.get(),
            'tipo': self.tipo_var.get(),
            'proveedor': self.proveedor_var.get()
        }

        if self.modo_edicion and self.producto_editando_id:
            # Actualizar producto existente
            if self.controller.actualizar_producto(self.producto_editando_id, datos):
                self.cargar_productos()
                self.limpiar_formulario()
                self.modo_edicion = False
                self.producto_editando_id = None
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        else:
            # Crear nuevo producto
            if self.controller.crear_producto(datos):
                self.cargar_productos()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", f"Producto '{datos['nombre']}' creado correctamente")

    def editar_producto(self):
        """Preparar para editar producto"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        # Obtener datos completos del producto desde la base de datos
        try:
            from models.producto import Producto
            producto = Producto.buscar_por_id(valores[0])
            if producto:
                # Cargar datos en el formulario
                self.nombre_var.set(producto.nombre)
                self.categoria_var.set(producto.categoria or '')
                self.descripcion_var.set(producto.descripcion or '')
                self.precio_compra_var.set(str(producto.precio_compra))
                self.precio_venta_var.set(str(producto.precio_venta))
                self.stock_var.set(str(producto.stock))
                self.stock_minimo_var.set(str(producto.stock_minimo))
                self.marca_var.set(producto.marca or '')
                self.tipo_var.set(producto.tipo or '')
                self.proveedor_var.set(producto.proveedor or '')

                self.modo_edicion = True
                self.producto_editando_id = valores[0]
                messagebox.showinfo("Modo Edición", f"Editando: {producto.nombre}\nModifique los datos y presione Guardar")
            else:
                messagebox.showerror("Error", "No se pudo cargar el producto para editar")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar producto: {str(e)}")

    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return

        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][1]

        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto '{producto_nombre}'?"):
            if self.controller.eliminar_producto(producto_id):
                self.cargar_productos()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")

    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_var.set('')
        self.categoria_var.set('')
        self.descripcion_var.set('')
        self.precio_compra_var.set('')
        self.precio_venta_var.set('')
        self.stock_var.set('')
        self.stock_minimo_var.set('')
        self.marca_var.set('')
        self.tipo_var.set('')
        self.proveedor_var.set('')

    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()