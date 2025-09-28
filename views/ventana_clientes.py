"""
Ventana para gestión de clientes - Versión corregida
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController

class VentanaClientes:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ClienteController()
        self.ventana = None
        self.tree = None
        self.crear_ventana()
    
    def crear_ventana(self):
        """Crear la ventana de clientes"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Clientes")
        self.ventana.geometry("1300x700")
        self.ventana.configure(bg='#ecf0f1')
        
        # Hacer que la ventana sea modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Crear interfaz
        self.crear_toolbar()
        self.crear_formulario()
        self.crear_lista_clientes()
        self.crear_botones()
        
        # Cargar clientes
        self.cargar_clientes()
    
    def crear_toolbar(self):
        """Crear barra de herramientas"""
        toolbar_frame = tk.Frame(self.ventana, bg='#2ecc71', height=60)
        toolbar_frame.pack(fill='x', padx=5, pady=5)
        toolbar_frame.pack_propagate(False)
        
        # Título
        titulo = tk.Label(toolbar_frame, text="GESTIÓN DE CLIENTES", 
                         font=("Arial", 18, "bold"), fg='white', bg='#2ecc71')
        titulo.pack(side='left', padx=20, pady=15)
        
        # Buscador
        search_frame = tk.Frame(toolbar_frame, bg='#2ecc71')
        search_frame.pack(side='right', padx=20, pady=15)
        
        tk.Label(search_frame, text="Buscar:", font=("Arial", 10), 
                fg='white', bg='#2ecc71').pack(side='left', padx=(0, 5))
        
        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_clientes)
        
        buscar_entry = tk.Entry(search_frame, textvariable=self.buscar_var, 
                               font=("Arial", 10), width=25)
        buscar_entry.pack(side='left')
    
    def crear_formulario(self):
        """Crear formulario para agregar/editar clientes"""
        # Frame principal del formulario
        form_frame = tk.LabelFrame(self.ventana, text="Datos del Cliente", 
                                  font=("Arial", 12, "bold"), bg='#ecf0f1')
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Variables del formulario
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()
        
        # Primera fila
        fila1 = tk.Frame(form_frame, bg='#ecf0f1')
        fila1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila1, text="Nombre:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila1, textvariable=self.nombre_var, font=("Arial", 10), width=20).pack(side='left', padx=(5, 20))
        
        tk.Label(fila1, text="Apellido:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila1, textvariable=self.apellido_var, font=("Arial", 10), width=20).pack(side='left', padx=(5, 20))
        
        tk.Label(fila1, text="Teléfono:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila1, textvariable=self.telefono_var, font=("Arial", 10), width=15).pack(side='left', padx=5)
        
        # Segunda fila
        fila2 = tk.Frame(form_frame, bg='#ecf0f1')
        fila2.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila2, text="Email:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila2, textvariable=self.email_var, font=("Arial", 10), width=30).pack(side='left', padx=(5, 20))
        
        tk.Label(fila2, text="Ciudad:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        ciudades = ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco", "Rancagua", "Talca", "Otra"]
        ciudad_combo = ttk.Combobox(fila2, textvariable=self.ciudad_var, values=ciudades, width=15)
        ciudad_combo.pack(side='left', padx=5)
        
        # Tercera fila
        fila3 = tk.Frame(form_frame, bg='#ecf0f1')
        fila3.pack(fill='x', padx=10, pady=5)
        
        tk.Label(fila3, text="Dirección:", font=("Arial", 10), bg='#ecf0f1').pack(side='left')
        tk.Entry(fila3, textvariable=self.direccion_var, font=("Arial", 10), width=50).pack(side='left', padx=5)
    
    def crear_lista_clientes(self):
        """Crear lista de clientes con Treeview"""
        # Frame para la lista
        lista_frame = tk.LabelFrame(self.ventana, text="Lista de Clientes", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear Treeview
        columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Ciudad', 'Total Compras')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Ciudad', text='Ciudad')
        self.tree.heading('Total Compras', text='Total Compras')
        
        # Configurar ancho de columnas
        self.tree.column('ID', width=50)
        self.tree.column('Nombre', width=150)
        self.tree.column('Apellido', width=150)
        self.tree.column('Teléfono', width=120)
        self.tree.column('Email', width=200)
        self.tree.column('Ciudad', width=120)
        self.tree.column('Total Compras', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_cliente)
    
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
                 command=self.nuevo_cliente, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Guardar", bg='#3498db', fg='white',
                 command=self.guardar_cliente, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Editar", bg='#f39c12', fg='white',
                 command=self.editar_cliente, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Eliminar", bg='#e74c3c', fg='white',
                 command=self.eliminar_cliente, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Ver Historial", bg='#9b59b6', fg='white',
                 command=self.ver_historial, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Actualizar Lista", bg='#34495e', fg='white',
                 command=self.cargar_clientes, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Cerrar", bg='#95a5a6', fg='white',
                 command=self.cerrar_ventana, **btn_style).pack(side='right', padx=5)
        
        # Variable para modo edición
        self.modo_edicion = False
        self.cliente_editando_id = None
    
    def cargar_clientes(self):
        """Cargar clientes en la lista"""
        try:
            # Limpiar lista
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener clientes
            from models.cliente import Cliente
            clientes = Cliente.obtener_todos()
            
            # Agregar clientes a la lista
            for cliente in clientes:
                total_compras = cliente.calcular_total_compras()
                
                self.tree.insert('', 'end', values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.apellido,
                    cliente.telefono,
                    cliente.email,
                    cliente.ciudad,
                    f"${total_compras:,.0f}" if total_compras > 0 else "$0"
                ))
            
            # Forzar actualización visual
            self.tree.update_idletasks()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def buscar_clientes(self, *args):
        """Buscar clientes"""
        termino = self.buscar_var.get()
        
        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar clientes
        if termino.strip():
            clientes = self.controller.buscar_clientes(termino)
        else:
            from models.cliente import Cliente  
            clientes = Cliente.obtener_todos()
        
        # Mostrar resultados
        for cliente in clientes:
            total_compras = cliente.calcular_total_compras()
            
            self.tree.insert('', 'end', values=(
                cliente.id,
                cliente.nombre,
                cliente.apellido,
                cliente.telefono,
                cliente.email,
                cliente.ciudad,
                f"${total_compras:,.0f}" if total_compras > 0 else "$0"
            ))
    
    def seleccionar_cliente(self, event):
        """Manejar selección de cliente"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            
            # Llenar formulario
            self.nombre_var.set(valores[1])
            self.apellido_var.set(valores[2])
            self.telefono_var.set(valores[3])
            self.email_var.set(valores[4])
            self.ciudad_var.set(valores[5])
            
            # Obtener dirección del cliente
            from models.cliente import Cliente
            cliente = Cliente.buscar_por_id(valores[0])
            if cliente:
                self.direccion_var.set(cliente.direccion)
    
    def nuevo_cliente(self):
        """Preparar para nuevo cliente"""
        self.limpiar_formulario()
        self.modo_edicion = False
        self.cliente_editando_id = None
    
    def guardar_cliente(self):
        """Guardar cliente"""
        datos = {
            'nombre': self.nombre_var.get(),
            'apellido': self.apellido_var.get(),
            'telefono': self.telefono_var.get(),
            'email': self.email_var.get(),
            'direccion': self.direccion_var.get(),
            'ciudad': self.ciudad_var.get()
        }
        
        if self.modo_edicion and self.cliente_editando_id:
            # Actualizar cliente existente
            if self.controller.actualizar_cliente(self.cliente_editando_id, datos):
                self.cargar_clientes()
                self.limpiar_formulario()
                self.modo_edicion = False
                self.cliente_editando_id = None
        else:
            # Crear nuevo cliente
            if self.controller.crear_cliente(datos):
                self.cargar_clientes()
                self.limpiar_formulario()
                
                # Mostrar confirmación
                cliente_nombre = f"{datos['nombre']} {datos['apellido']}"
                messagebox.showinfo("Éxito", f"Cliente '{cliente_nombre}' creado correctamente")
    
    def editar_cliente(self):
        """Preparar para editar cliente"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        self.modo_edicion = True
        self.cliente_editando_id = valores[0]
        messagebox.showinfo("Modo Edición", f"Editando cliente: {valores[1]} {valores[2]}\nModifique los datos y haga clic en Guardar")
    
    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        cliente_id = item['values'][0]
        
        if self.controller.eliminar_cliente(cliente_id):
            self.cargar_clientes()
            self.limpiar_formulario()
    
    def ver_historial(self):
        """Ver historial de compras del cliente"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para ver su historial")
            return
        
        item = self.tree.item(seleccion[0])
        cliente_id = item['values'][0]
        cliente_nombre = f"{item['values'][1]} {item['values'][2]}"
        
        messagebox.showinfo("Historial de Compras", 
                           f"Historial de compras para: {cliente_nombre}\n\n" +
                           "Esta funcionalidad se implementará en el módulo de VENTAS.\n" +
                           "Podrá ver todas las compras realizadas por este cliente.")
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_var.set('')
        self.apellido_var.set('')
        self.telefono_var.set('')
        self.email_var.set('')
        self.direccion_var.set('')
        self.ciudad_var.set('')
    
    def cerrar_ventana(self):
        """Cerrar la ventana"""
        self.ventana.destroy()