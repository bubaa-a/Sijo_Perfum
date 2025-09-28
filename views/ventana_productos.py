"""
Ventana para gestión de productos
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
        """Crear la ventana de productos"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Productos")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#ecf0f1')
        
        # Hacer que la ventana sea modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Crear interfaz
        self.crear_toolbar()
        self.crear_formulario()
        self.crear_lista_productos()
        self.crear_botones()
        
        # Cargar productos
        self.cargar_productos()
    
    def crear_toolbar(self):
        """Crear barra de herramientas"""
        toolbar_frame = tk.Frame(self.ventana, bg='#34495e', height=60)
        toolbar_frame.pack(fill='x', padx=5, pady=5)
        toolbar_frame.pack_propagate(False)
        
        # Título
        titulo = tk.Label(toolbar_frame, text="GESTIÓN DE PRODUCTOS", 
                         font=("Arial", 18, "bold"), fg='white', bg='#34495e')
        titulo.pack(side='left', padx=20, pady=15)
        
        # Buscador
        search_frame = tk.Frame(toolbar_frame, bg='#34495e')
        search_frame.pack(side='right', padx=20, pady=15)
        
        tk.Label(search_frame, text="Buscar:", font=("Arial", 10), 
                fg='white', bg='#34495e').pack(side='left', padx=(0, 5))
        
        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_productos)
        
        buscar_entry = tk.Entry(search_frame, textvariable=self.buscar_var, 
                               font=("Arial", 10), width=20)
        buscar_entry.pack(side='left')
    
    def crear_formulario(self):
        """Crear formulario para agregar/editar productos"""
        # Frame principal del formulario
        form_frame = tk.LabelFrame(self.ventana, text="Datos del Producto", 
                                  font=("Arial", 12, "bold"), bg='#ecf0f1')
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Variables del formulario
        self.nombre_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.precio_compra_var = tk.StringVar()
        self.precio_venta_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.stock_minimo_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        
        # Primera fila
        fila1 = tk.Frame(form_frame, bg='#ecf0f1')
        fila1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila1, text="Nombre:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila1, textvariable=self.nombre_var, font=("Arial", 10), width=25).pack(side='left', padx=(5, 20))
        
        tk.Label(fila1, text="Categoría:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        categorias = ["General", "Electrónicos", "Ropa", "Hogar", "Deportes", "Otros"]
        categoria_combo = ttk.Combobox(fila1, textvariable=self.categoria_var, values=categorias, width=15)
        categoria_combo.pack(side='left', padx=5)
        
        # Segunda fila
        fila2 = tk.Frame(form_frame, bg='#ecf0f1')
        fila2.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila2, text="Descripción:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila2, textvariable=self.descripcion_var, font=("Arial", 10), width=40).pack(side='left', padx=5)
        
        # Tercera fila
        fila3 = tk.Frame(form_frame, bg='#ecf0f1')
        fila3.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila3, text="Precio Compra:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila3, textvariable=self.precio_compra_var, font=("Arial", 10), width=15).pack(side='left', padx=(5, 20))
        
        tk.Label(fila3, text="Precio Venta:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila3, textvariable=self.precio_venta_var, font=("Arial", 10), width=15).pack(side='left', padx=(5, 20))
        
        tk.Label(fila3, text="Stock:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila3, textvariable=self.stock_var, font=("Arial", 10), width=10).pack(side='left', padx=(5, 20))
        
        tk.Label(fila3, text="Stock Mín:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila3, textvariable=self.stock_minimo_var, font=("Arial", 10), width=10).pack(side='left', padx=5)
    
    def crear_lista_productos(self):
        """Crear lista de productos con Treeview"""
        # Frame para la lista
        lista_frame = tk.LabelFrame(self.ventana, text="Lista de Productos", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear Treeview
        columns = ('ID', 'Nombre', 'Categoría', 'Precio Compra', 'Precio Venta', 'Stock', 'Stock Mín', 'Ganancia')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('Precio Compra', text='P. Compra')
        self.tree.heading('Precio Venta', text='P. Venta')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Stock Mín', text='S. Mín')
        self.tree.heading('Ganancia', text='Ganancia')
        
        # Configurar ancho de columnas
        self.tree.column('ID', width=50)
        self.tree.column('Nombre', width=200)
        self.tree.column('Categoría', width=100)
        self.tree.column('Precio Compra', width=100)
        self.tree.column('Precio Venta', width=100)
        self.tree.column('Stock', width=80)
        self.tree.column('Stock Mín', width=80)
        self.tree.column('Ganancia', width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
    
    def crear_botones(self):
        """Crear botones de acción"""
        botones_frame = tk.Frame(self.ventana, bg='#ecf0f1')
        botones_frame.pack(fill='x', padx=10, pady=10)
        
        # Estilo de botones
        btn_style = {
            'font': ('Arial', 10, 'bold'),
            'width': 15,
            'height': 2
        }
        
        # Botones
        tk.Button(botones_frame, text="Nuevo", bg='#2ecc71', fg='white',
                 command=self.nuevo_producto, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Guardar", bg='#3498db', fg='white',
                 command=self.guardar_producto, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Editar", bg='#f39c12', fg='white',
                 command=self.editar_producto, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Eliminar", bg='#e74c3c', fg='white',
                 command=self.eliminar_producto, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Actualizar Lista", bg='#9b59b6', fg='white',
                 command=self.cargar_productos, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Cerrar", bg='#95a5a6', fg='white',
                 command=self.cerrar_ventana, **btn_style).pack(side='right', padx=5)
        
        # Variable para modo edición
        self.modo_edicion = False
        self.producto_editando_id = None
    
    def cargar_productos(self):
        """Cargar productos en la lista"""
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
            
            self.tree.insert('', 'end', values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                f"${producto.precio_compra:.2f}",
                f"${producto.precio_venta:.2f}",
                producto.stock,
                producto.stock_minimo,
                ganancia
            ), tags=tags)
        
        # Configurar colores
        self.tree.tag_configure('bajo_stock', background='#ffebee')
        self.tree.tag_configure('normal', background='white')
    
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
            
            self.tree.insert('', 'end', values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                f"${producto.precio_compra:.2f}",
                f"${producto.precio_venta:.2f}",
                producto.stock,
                producto.stock_minimo,
                ganancia
            ), tags=tags)
    
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
                self.descripcion_var.set(producto.descripcion)
    
    def nuevo_producto(self):
        """Preparar para nuevo producto"""
        self.limpiar_formulario()
        self.modo_edicion = False
        self.producto_editando_id = None
    
    def guardar_producto(self):
        """Guardar producto"""
        datos = {
            'nombre': self.nombre_var.get(),
            'descripcion': self.descripcion_var.get(),
            'precio_compra': self.precio_compra_var.get(),
            'precio_venta': self.precio_venta_var.get(),
            'stock': self.stock_var.get(),
            'stock_minimo': self.stock_minimo_var.get(),
            'categoria': self.categoria_var.get()
        }
        
        if self.modo_edicion and self.producto_editando_id:
            # Actualizar producto existente
            if self.controller.actualizar_producto(self.producto_editando_id, datos):
                self.cargar_productos()
                self.limpiar_formulario()
                self.modo_edicion = False
                self.producto_editando_id = None
        else:
            # Crear nuevo producto
            if self.controller.crear_producto(datos):
                self.cargar_productos()
                self.limpiar_formulario()
    
    def editar_producto(self):
        """Preparar para editar producto"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        self.modo_edicion = True
        self.producto_editando_id = valores[0]
        messagebox.showinfo("Modo Edición", f"Editando producto: {valores[1]}\nModifique los datos y haga clic en Guardar")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        
        if self.controller.eliminar_producto(producto_id):
            self.cargar_productos()
            self.limpiar_formulario()
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_var.set('')
        self.descripcion_var.set('')
        self.precio_compra_var.set('')
        self.precio_venta_var.set('')
        self.stock_var.set('')
        self.stock_minimo_var.set('')
        self.categoria_var.set('')
    
    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()