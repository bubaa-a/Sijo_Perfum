"""
Ventana para gestión de ventas
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
        self.productos_disponibles = []
        self.clientes_disponibles = []
        self.carrito = []  # Lista de productos en el carrito
        self.crear_ventana()
    
    def crear_ventana(self):
        """Crear la ventana de ventas"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Ventas")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg='#ecf0f1')
        
        # Hacer que la ventana sea modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
        
        # Crear interfaz
        self.crear_toolbar()
        self.crear_formulario_venta()
        self.crear_carrito()
        self.crear_lista_ventas()
        self.crear_botones()
        
        # Cargar ventas
        self.cargar_ventas()
        # Actualizar combos cada vez que se enfoca la ventana
        self.ventana.bind('<FocusIn>', self.actualizar_combos_evento)

    def actualizar_combos_evento(self, event):
        """Actualizar combos cuando la ventana recibe foco"""
        try:
            self.cargar_clientes_combo()
        except:
            pass
    
    def cargar_datos_iniciales(self):
        """Cargar productos y clientes disponibles"""
        self.productos_disponibles = self.controller.obtener_productos_disponibles()
        self.clientes_disponibles = self.controller.obtener_clientes_activos()
    
    def crear_toolbar(self):
        """Crear barra de herramientas"""
        toolbar_frame = tk.Frame(self.ventana, bg='#e74c3c', height=60)
        toolbar_frame.pack(fill='x', padx=5, pady=5)
        toolbar_frame.pack_propagate(False)
        
        # Título
        titulo = tk.Label(toolbar_frame, text="GESTIÓN DE VENTAS", 
                         font=("Arial", 18, "bold"), fg='white', bg='#e74c3c')
        titulo.pack(side='left', padx=20, pady=15)
        
        # Estadísticas rápidas
        stats_frame = tk.Frame(toolbar_frame, bg='#e74c3c')
        stats_frame.pack(side='right', padx=20, pady=10)
        
        stats = self.controller.obtener_estadisticas_ventas()
        
        tk.Label(stats_frame, text=f"Ventas Hoy: {stats['ventas_hoy']}", 
                font=("Arial", 10, "bold"), fg='white', bg='#e74c3c').pack()
        tk.Label(stats_frame, text=f"Ingresos Hoy: ${stats['ingresos_hoy']:,.0f}", 
                font=("Arial", 10, "bold"), fg='white', bg='#e74c3c').pack()
    
    def crear_formulario_venta(self):
        """Crear formulario para nueva venta"""
        # Frame principal del formulario
        form_frame = tk.LabelFrame(self.ventana, text="Nueva Venta", 
                                  font=("Arial", 12, "bold"), bg='#ecf0f1')
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Variables del formulario
        self.cliente_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.observaciones_var = tk.StringVar()
        
        # Primera fila - Cliente
        fila1 = tk.Frame(form_frame, bg='#ecf0f1')
        fila1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila1, text="Cliente:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        
        # Combobox de clientes
        clientes_nombres = [f"{c.id} - {c.nombre} {c.apellido}" for c in self.clientes_disponibles]
        cliente_combo = ttk.Combobox(fila1, textvariable=self.cliente_var, 
                                   values=clientes_nombres, width=40, state="readonly")
        cliente_combo.pack(side='left', padx=5)
        
        tk.Label(fila1, text="Observaciones:", font=("Arial", 10), bg='#ecf0f1').pack(side='left', padx=(20, 5))
        tk.Entry(fila1, textvariable=self.observaciones_var, font=("Arial", 10), width=30).pack(side='left', padx=5)
        
        # Segunda fila - Agregar productos
        fila2 = tk.Frame(form_frame, bg='#ecf0f1')
        fila2.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila2, text="Producto:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        
        # Combobox de productos
        productos_nombres = [f"{p.id} - {p.nombre} (Stock: {p.stock}) - ${p.precio_venta:.0f}" 
                           for p in self.productos_disponibles]
        producto_combo = ttk.Combobox(fila2, textvariable=self.producto_var, 
                                    values=productos_nombres, width=40, state="readonly")
        producto_combo.pack(side='left', padx=5)
        producto_combo.bind('<<ComboboxSelected>>', self.producto_seleccionado)
        
        tk.Label(fila2, text="Cantidad:", font=("Arial", 10), bg='#ecf0f1').pack(side='left', padx=(10, 5))
        tk.Entry(fila2, textvariable=self.cantidad_var, font=("Arial", 10), width=10).pack(side='left', padx=5)
        
        tk.Label(fila2, text="Precio:", font=("Arial", 10), bg='#ecf0f1').pack(side='left', padx=(10, 5))
        tk.Entry(fila2, textvariable=self.precio_var, font=("Arial", 10), width=15).pack(side='left', padx=5)
        
        tk.Button(fila2, text="Agregar al Carrito", bg='#27ae60', fg='white',
                 command=self.agregar_al_carrito, font=("Arial", 10, "bold")).pack(side='left', padx=10)
    
    def crear_carrito(self):
        """Crear sección del carrito de compras"""
        # Frame del carrito
        carrito_frame = tk.LabelFrame(self.ventana, text="Carrito de Compras", 
                                    font=("Arial", 12, "bold"), bg='#ecf0f1')
        carrito_frame.pack(fill='x', padx=10, pady=5)
        
        # Treeview para el carrito
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.tree_carrito = ttk.Treeview(carrito_frame, columns=columns, show='headings', height=6)
        
        # Configurar columnas
        self.tree_carrito.heading('Producto', text='Producto')
        self.tree_carrito.heading('Cantidad', text='Cantidad')
        self.tree_carrito.heading('Precio Unit.', text='Precio Unit.')
        self.tree_carrito.heading('Subtotal', text='Subtotal')
        
        self.tree_carrito.column('Producto', width=300)
        self.tree_carrito.column('Cantidad', width=100)
        self.tree_carrito.column('Precio Unit.', width=120)
        self.tree_carrito.column('Subtotal', width=120)
        
        self.tree_carrito.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar para carrito
        scrollbar_carrito = ttk.Scrollbar(carrito_frame, orient='vertical', command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=scrollbar_carrito.set)
        scrollbar_carrito.pack(side='right', fill='y')
        
        # Frame para botones del carrito y total
        carrito_bottom = tk.Frame(carrito_frame, bg='#ecf0f1')
        carrito_bottom.pack(fill='x', padx=5, pady=5)
        
        tk.Button(carrito_bottom, text="Quitar Producto", bg='#e74c3c', fg='white',
                 command=self.quitar_del_carrito, font=("Arial", 10)).pack(side='left', padx=5)
        
        tk.Button(carrito_bottom, text="Limpiar Carrito", bg='#f39c12', fg='white',
                 command=self.limpiar_carrito, font=("Arial", 10)).pack(side='left', padx=5)
        
        # Total
        self.total_var = tk.StringVar(value="Total: $0")
        tk.Label(carrito_bottom, textvariable=self.total_var, font=("Arial", 14, "bold"), 
                bg='#ecf0f1', fg='#2c3e50').pack(side='right', padx=20)
    
    def crear_lista_ventas(self):
        """Crear lista de ventas realizadas"""
        # Frame para la lista
        lista_frame = tk.LabelFrame(self.ventana, text="Historial de Ventas", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear Treeview
        columns = ('ID', 'Cliente', 'Total', 'Fecha', 'Observaciones')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Total', text='Total')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Observaciones', text='Observaciones')
        
        self.tree.column('ID', width=50)
        self.tree.column('Cliente', width=200)
        self.tree.column('Total', width=120)
        self.tree.column('Fecha', width=150)
        self.tree.column('Observaciones', width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
    
    def crear_botones(self):
        """Crear botones de acción"""
        botones_frame = tk.Frame(self.ventana, bg='#ecf0f1')
        botones_frame.pack(fill='x', padx=10, pady=10)
        
        # Estilo de botones
        btn_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 15,
            'height': 2
        }
        
        # Botones
        tk.Button(botones_frame, text="PROCESAR VENTA", bg='#27ae60', fg='white',
                 command=self.procesar_venta, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Ver Detalle", bg='#3498db', fg='white',
                 command=self.ver_detalle_venta, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Actualizar Lista", bg='#9b59b6', fg='white',
                 command=self.cargar_ventas, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Cerrar", bg='#95a5a6', fg='white',
                 command=self.cerrar_ventana, **btn_style).pack(side='right', padx=5)
    
    def producto_seleccionado(self, event):
        """Cuando se selecciona un producto, llenar el precio automáticamente"""
        seleccion = self.producto_var.get()
        if seleccion:
            producto_id = int(seleccion.split(' - ')[0])
            producto = next((p for p in self.productos_disponibles if p.id == producto_id), None)
            if producto:
                self.precio_var.set(str(producto.precio_venta))
    
    def agregar_al_carrito(self):
        """Agregar producto al carrito"""
        try:
            if not self.producto_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            # Obtener datos
            producto_id = int(self.producto_var.get().split(' - ')[0])
            cantidad = int(self.cantidad_var.get())
            precio = float(self.precio_var.get())
            
            # Buscar el producto
            producto = next((p for p in self.productos_disponibles if p.id == producto_id), None)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            # Validar cantidad
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            if cantidad > producto.stock:
                messagebox.showwarning("Advertencia", f"Stock insuficiente. Disponible: {producto.stock}")
                return
            
            # Validar precio
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
            
            # Verificar si el producto ya está en el carrito
            for i, item in enumerate(self.carrito):
                if item['producto_id'] == producto_id:
                    # Actualizar cantidad
                    nueva_cantidad = item['cantidad'] + cantidad
                    if nueva_cantidad > producto.stock:
                        messagebox.showwarning("Advertencia", f"Cantidad total excede el stock. Disponible: {producto.stock}")
                        return
                    self.carrito[i]['cantidad'] = nueva_cantidad
                    self.carrito[i]['subtotal'] = nueva_cantidad * precio
                    break
            else:
                # Agregar nuevo producto al carrito
                self.carrito.append({
                    'producto_id': producto_id,
                    'producto_nombre': producto.nombre,
                    'cantidad': cantidad,
                    'precio_unitario': precio,
                    'subtotal': cantidad * precio
                })
            
            # Actualizar vista del carrito
            self.actualizar_carrito()
            
            # Limpiar campos
            self.producto_var.set('')
            self.cantidad_var.set('')
            self.precio_var.set('')
            
        except ValueError:
            messagebox.showerror("Error", "Verifique que cantidad y precio sean números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def actualizar_carrito(self):
        """Actualizar la vista del carrito"""
        # Limpiar carrito
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        # Agregar productos del carrito
        total = 0
        for item in self.carrito:
            self.tree_carrito.insert('', 'end', values=(
                item['producto_nombre'],
                item['cantidad'],
                f"${item['precio_unitario']:.0f}",
                f"${item['subtotal']:.0f}"
            ))
            total += item['subtotal']
        
        # Actualizar total
        self.total_var.set(f"Total: ${total:,.0f}")
    
    def quitar_del_carrito(self):
        """Quitar producto seleccionado del carrito"""
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para quitar")
            return
        
        # Obtener índice del producto seleccionado
        indice = self.tree_carrito.index(seleccion[0])
        
        # Confirmar eliminación
        producto_nombre = self.carrito[indice]['producto_nombre']
        respuesta = messagebox.askyesno("Confirmar", f"¿Quitar {producto_nombre} del carrito?")
        
        if respuesta:
            # Quitar del carrito
            del self.carrito[indice]
            # Actualizar vista
            self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpiar todo el carrito"""
        if self.carrito:
            respuesta = messagebox.askyesno("Confirmar", "¿Limpiar todo el carrito?")
            if respuesta:
                self.carrito.clear()
                self.actualizar_carrito()
    
    def procesar_venta(self):
        """Procesar la venta actual"""
        try:
            # Validar que hay productos en el carrito
            if not self.carrito:
                messagebox.showwarning("Advertencia", "Agregue productos al carrito antes de procesar la venta")
                return
            
            # Validar que hay cliente seleccionado
            if not self.cliente_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return
            
            # Obtener ID del cliente
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            
            # Preparar detalles de venta
            detalles_venta = []
            for item in self.carrito:
                detalles_venta.append({
                    'producto_id': item['producto_id'],
                    'cantidad': item['cantidad'],
                    'precio_unitario': item['precio_unitario']
                })
            
            # Obtener observaciones
            observaciones = self.observaciones_var.get()
            
            # Crear la venta
            if self.controller.crear_venta(cliente_id, detalles_venta, observaciones):
                # Limpiar formulario
                self.limpiar_formulario()
                # Actualizar lista de ventas
                self.cargar_ventas()
                # Recargar productos (por si cambió el stock)
                self.cargar_datos_iniciales()
                self.actualizar_combobox_productos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")
    
    def actualizar_combobox_productos(self):
        """Actualizar el combobox de productos"""
        productos_nombres = [f"{p.id} - {p.nombre} (Stock: {p.stock}) - ${p.precio_venta:.0f}" 
                           for p in self.productos_disponibles]
        
        # Buscar el combobox y actualizar sus valores
        for widget in self.ventana.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Nueva Venta":
                for fila in widget.winfo_children():
                    if isinstance(fila, tk.Frame):
                        for child in fila.winfo_children():
                            if isinstance(child, ttk.Combobox) and len(child['values']) > 10:  # Es el combobox de productos
                                child['values'] = productos_nombres
                                break
    
    def cargar_ventas(self):
        """Cargar ventas en la lista"""
        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener ventas
        ventas = self.controller.obtener_todas_ventas()
        
        # Agregar ventas a la lista
        for venta in ventas:
            cliente_nombre = getattr(venta, 'cliente_nombre', 'Cliente no especificado')
            fecha_formateada = venta.fecha_venta[:16] if venta.fecha_venta else 'N/A'  # Solo fecha y hora
            
            self.tree.insert('', 'end', values=(
                venta.id,
                cliente_nombre,
                f"${venta.total:,.0f}",
                fecha_formateada,
                venta.observaciones or 'Sin observaciones'
            ))
    
    def ver_detalle_venta(self):
        """Ver detalle de la venta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver su detalle")
            return
        
        item = self.tree.item(seleccion[0])
        venta_id = item['values'][0]
        
        # Obtener venta completa con detalles
        venta = self.controller.obtener_venta_por_id(venta_id)
        if not venta:
            messagebox.showerror("Error", "No se pudo obtener el detalle de la venta")
            return
        
        # Crear ventana de detalle
        self.mostrar_detalle_venta(venta)
    
    def cargar_clientes_combo(self):
        """Cargar clientes en el combobox - solo clientes activos"""
        try:
            from models.cliente import Cliente
        
            # Obtener solo clientes que existen en la base de datos
            clientes = Cliente.obtener_todos()
        
            if clientes:
                # Crear lista con formato: "ID - Nombre Apellido"
                clientes_opciones = [f"{cliente.id} - {cliente.nombre} {cliente.apellido}" for cliente in clientes]
                self.cliente_combo['values'] = clientes_opciones
            else:
                self.cliente_combo['values'] = []
            
            # Limpiar selección actual si el cliente no existe
            if self.cliente_var.get():
                cliente_actual = self.cliente_var.get()
                if cliente_actual not in clientes_opciones:
                    self.cliente_var.set("")
                
        except Exception as e:
            print(f"Error al cargar clientes en combo: {str(e)}")
            self.cliente_combo['values'] = []
    
    def mostrar_detalle_venta(self, venta):
        """Mostrar ventana con detalle de la venta"""
        detalle_ventana = tk.Toplevel(self.ventana)
        detalle_ventana.title(f"Detalle de Venta #{venta.id}")
        detalle_ventana.geometry("600x500")
        detalle_ventana.configure(bg='#ecf0f1')
        
        # Información general
        info_frame = tk.LabelFrame(detalle_ventana, text="Información General", 
                                 font=("Arial", 12, "bold"), bg='#ecf0f1')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(info_frame, text=f"ID Venta: {venta.id}", font=("Arial", 10, "bold"), bg='#ecf0f1').pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Cliente: {getattr(venta, 'cliente_nombre', 'N/A')}", font=("Arial", 10), bg='#ecf0f1').pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Fecha: {venta.fecha_venta}", font=("Arial", 10), bg='#ecf0f1').pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Total: ${venta.total:,.0f}", font=("Arial", 12, "bold"), bg='#ecf0f1', fg='#27ae60').pack(anchor='w', padx=10, pady=2)
        if venta.observaciones:
            tk.Label(info_frame, text=f"Observaciones: {venta.observaciones}", font=("Arial", 10), bg='#ecf0f1').pack(anchor='w', padx=10, pady=2)
        
        # Detalles de productos
        detalles_frame = tk.LabelFrame(detalle_ventana, text="Productos Vendidos", 
                                     font=("Arial", 12, "bold"), bg='#ecf0f1')
        detalles_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para detalles
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        tree_detalle = ttk.Treeview(detalles_frame, columns=columns, show='headings')
        
        tree_detalle.heading('Producto', text='Producto')
        tree_detalle.heading('Cantidad', text='Cantidad')
        tree_detalle.heading('Precio Unit.', text='Precio Unit.')
        tree_detalle.heading('Subtotal', text='Subtotal')
        
        tree_detalle.column('Producto', width=250)
        tree_detalle.column('Cantidad', width=100)
        tree_detalle.column('Precio Unit.', width=120)
        tree_detalle.column('Subtotal', width=120)
        
        # Agregar detalles
        for detalle in venta.detalles:
            tree_detalle.insert('', 'end', values=(
                getattr(detalle, 'producto_nombre', f'Producto ID: {detalle.producto_id}'),
                detalle.cantidad,
                f"${detalle.precio_unitario:,.0f}",
                f"${detalle.subtotal:,.0f}"
            ))
        
        tree_detalle.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botón cerrar
        tk.Button(detalle_ventana, text="Cerrar", bg='#95a5a6', fg='white',
                 command=detalle_ventana.destroy, font=("Arial", 10, "bold")).pack(pady=10)
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.cliente_var.set('')
        self.producto_var.set('')
        self.cantidad_var.set('')
        self.precio_var.set('')
        self.observaciones_var.set('')
        self.carrito.clear()
        self.actualizar_carrito()
    
    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()# Validar selecciones
            