"""
Ventana para gestión de clientes - Diseño moderno y funcional
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
        """Crear la ventana de clientes con diseño moderno"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Clientes - Sistema Empresarial Pro")
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

        # Cargar clientes
        self.cargar_clientes()

    def crear_header_moderno(self):
        """Crear header atractivo con búsqueda"""
        # Header principal
        header_frame = tk.Frame(self.ventana, bg='#27ae60', height=100)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Icono y título
        title_frame = tk.Frame(header_frame, bg='#27ae60')
        title_frame.grid(row=0, column=0, sticky='w', padx=30, pady=20)

        # Título principal
        tk.Label(title_frame, text="👥 CLIENTES",
                font=("Segoe UI", 24, "bold"), fg='white', bg='#27ae60').pack()

        # Subtítulo
        tk.Label(title_frame, text="Administración completa de clientes",
                font=("Segoe UI", 12), fg='#d5f4e6', bg='#27ae60').pack()

        # Panel de búsqueda
        search_frame = tk.Frame(header_frame, bg='#2ecc71')
        search_frame.grid(row=0, column=1, sticky='e', padx=30, pady=20)

        tk.Label(search_frame, text="Buscar Cliente:",
                font=("Segoe UI", 11, "bold"), fg='white', bg='#2ecc71').pack()

        # Entry de búsqueda con estilo
        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_clientes)

        search_entry = tk.Entry(search_frame, textvariable=self.buscar_var,
                               font=("Segoe UI", 12), width=30, relief='flat',
                               bg='white', fg='#27ae60', insertbackground='#27ae60')
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

        # Crear lista de clientes
        self.crear_lista_moderna(main_container)

        # Crear botones
        self.crear_botones_modernos(main_container)

    def crear_formulario_moderno(self, parent):
        """Crear formulario atractivo"""
        # Frame del formulario
        form_frame = tk.LabelFrame(parent, text="  👤 Información del Cliente  ",
                                  font=("Segoe UI", 14, "bold"), fg='#2c3e50',
                                  bg='white', relief='raised', bd=2)
        form_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        form_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Variables del formulario
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()

        # Estilo para labels y entries
        label_style = {'font': ('Segoe UI', 10, 'bold'), 'fg': '#34495e', 'bg': 'white'}
        entry_style = {'font': ('Segoe UI', 11), 'relief': 'solid', 'bd': 1, 'bg': '#f8f9fa'}

        # Primera fila
        tk.Label(form_frame, text="Nombre:", **label_style).grid(
            row=0, column=0, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.nombre_var, width=25, **entry_style).grid(
            row=1, column=0, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Apellido:", **label_style).grid(
            row=0, column=1, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.apellido_var, width=25, **entry_style).grid(
            row=1, column=1, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Teléfono:", **label_style).grid(
            row=0, column=2, sticky='w', padx=15, pady=(15, 5))
        tk.Entry(form_frame, textvariable=self.telefono_var, width=20, **entry_style).grid(
            row=1, column=2, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Ciudad:", **label_style).grid(
            row=0, column=3, sticky='w', padx=15, pady=(15, 5))
        ciudad_combo = ttk.Combobox(form_frame, textvariable=self.ciudad_var, width=18,
                                   font=('Segoe UI', 11))
        ciudad_combo['values'] = ('Santiago', 'Valparaíso', 'Concepción', 'La Serena', 'Antofagasta', 'Copiapo', 'Otra')
        ciudad_combo.grid(row=1, column=3, sticky='ew', padx=15, pady=(0, 15))

        # Segunda fila
        tk.Label(form_frame, text="Email:", **label_style).grid(
            row=2, column=0, columnspan=2, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.email_var, width=40, **entry_style).grid(
            row=3, column=0, columnspan=2, sticky='ew', padx=15, pady=(0, 15))

        tk.Label(form_frame, text="Dirección:", **label_style).grid(
            row=2, column=2, columnspan=2, sticky='w', padx=15, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.direccion_var, width=40, **entry_style).grid(
            row=3, column=2, columnspan=2, sticky='ew', padx=15, pady=(0, 15))

        # Variables para modo edición
        self.modo_edicion = False
        self.cliente_editando_id = None

    def crear_lista_moderna(self, parent):
        """Crear lista atractiva de clientes"""
        # Frame de la lista
        list_frame = tk.LabelFrame(parent, text="  📊 Lista de Clientes  ",
                                  font=("Segoe UI", 14, "bold"), fg='#2c3e50',
                                  bg='white', relief='raised', bd=2)
        list_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 15))
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Info header
        info_frame = tk.Frame(list_frame, bg='white')
        info_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=10)

        tk.Label(info_frame, text="💡 Haga doble clic en un cliente para editarlo",
                font=("Segoe UI", 10, "italic"), fg='#7f8c8d', bg='white').pack(side='left')

        # Container del treeview
        tree_container = tk.Frame(list_frame, bg='white')
        tree_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configurar estilo moderno
        style = ttk.Style()
        style.configure("Clientes.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=35)
        style.configure("Clientes.Treeview.Heading",
                       background="#27ae60",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Ciudad', 'Total Compras')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="Clientes.Treeview")

        # Configurar columnas
        headers = {
            'ID': ('ID', 60),
            'Nombre': ('Nombre', 150),
            'Apellido': ('Apellido', 150),
            'Teléfono': ('Teléfono', 120),
            'Email': ('Email', 220),
            'Ciudad': ('Ciudad', 120),
            'Total Compras': ('Total Compras', 140)
        }

        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center' if col in ['ID', 'Total Compras'] else 'w')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout para scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        # Eventos
        self.tree.bind('<Double-1>', self.seleccionar_cliente)

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
        crear_boton("Nuevo", "#27ae60", self.nuevo_cliente, "➕")
        crear_boton("Guardar", "#3498db", self.guardar_cliente, "💾")
        crear_boton("Editar", "#f39c12", self.editar_cliente, "✏️")
        crear_boton("Eliminar", "#e74c3c", self.eliminar_cliente, "🗑️")
        crear_boton("Actualizar", "#34495e", self.cargar_clientes, "🔄")
        crear_boton("Cerrar", "#95a5a6", self.cerrar_ventana, "❌")

    def darken_color(self, color):
        """Oscurecer un color para efecto hover"""
        color_map = {
            "#27ae60": "#219a52",
            "#3498db": "#2980b9",
            "#f39c12": "#e67e22",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad",
            "#34495e": "#2c3e50",
            "#95a5a6": "#7f8c8d"
        }
        return color_map.get(color, color)

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
                try:
                    total_compras = cliente.calcular_total_compras()
                except:
                    total_compras = 0

                self.tree.insert('', 'end', values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.apellido,
                    cliente.telefono,
                    cliente.email,
                    cliente.ciudad,
                    f"${total_compras:,.0f}" if total_compras > 0 else "$0"
                ))

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
            try:
                total_compras = cliente.calcular_total_compras()
            except:
                total_compras = 0

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
                self.direccion_var.set(cliente.direccion or "")

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
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            # Crear nuevo cliente
            if self.controller.crear_cliente(datos):
                self.cargar_clientes()
                self.limpiar_formulario()
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
        messagebox.showinfo("Modo Edición", f"Editando: {valores[1]} {valores[2]}\\nModifique los datos y presione Guardar")

    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return

        try:
            item = self.tree.item(seleccion[0])
            cliente_id = item['values'][0]
            cliente_nombre = f"{item['values'][1]} {item['values'][2]}"

            if messagebox.askyesno("Confirmar", f"¿Eliminar el cliente '{cliente_nombre}'?"):
                if self.controller.eliminar_cliente(cliente_id):
                    self.cargar_clientes()
                    self.limpiar_formulario()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")


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