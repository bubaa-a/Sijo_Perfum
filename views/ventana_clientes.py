"""
Ventana para gestión de clientes - Diseño Moderno Mejorado con CustomTkinter
Versión con estilos unificados
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.cliente_controller import ClienteController
from config.estilos import (Colores, Fuentes, Espaciado, Dimensiones,
                            Iconos, obtener_color_hover, estilo_entry, estilo_card)

class VentanaClientes:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ClienteController()
        self.ventana = None
        self.tree = None
        self.style = ttk.Style()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.crear_ventana()

    def crear_ventana(self):
        """Crear la ventana de clientes con diseño moderno"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Gestión de Clientes - Sistema Empresarial Pro")
        self.ventana.geometry("1500x900")
        self.ventana.configure(bg=Colores.BG_PRIMARY)

        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        self.crear_header_moderno()
        self.crear_contenido_principal()
        self.cargar_clientes()

    def crear_header_moderno(self):
        """Crear header moderno con CustomTkinter"""
        header_frame = ctk.CTkFrame(
            self.ventana,
            fg_color=(Colores.PRIMARY_START, Colores.PRIMARY_END),
            height=Dimensiones.FOOTER_HEIGHT,
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{Iconos.CLIENTES} GESTIÓN DE CLIENTES",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.LARGE, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        )
        title_label.grid(row=0, column=0, sticky='w', padx=Espaciado.XL, pady=Espaciado.MEDIO)

        # Container para barra de búsqueda con icono
        search_container = ctk.CTkFrame(
            header_frame,
            fg_color=Colores.BG_SECONDARY,
            corner_radius=Dimensiones.RADIUS_SMALL,
            height=Dimensiones.ENTRY_HEIGHT
        )
        search_container.grid(row=0, column=1, sticky='e', padx=Espaciado.XL, pady=Espaciado.MEDIO)

        # Icono de búsqueda
        search_icon = ctk.CTkLabel(
            search_container,
            text=Iconos.BUSCAR,
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO),
            text_color=Colores.TEXT_SECONDARY,
            fg_color="transparent"
        )
        search_icon.pack(side='left', padx=(Espaciado.PEQUENO, 0))

        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', self.buscar_clientes)

        search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.buscar_var,
            placeholder_text="Buscar cliente...",
            width=240,
            height=Dimensiones.ENTRY_HEIGHT,
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.NORMAL),
            corner_radius=0,
            border_width=0,
            fg_color=Colores.BG_SECONDARY,
            text_color=Colores.TEXT_PRIMARY
        )
        search_entry.pack(side='left', padx=(0, Espaciado.PEQUENO))

    def crear_contenido_principal(self):
        """Crear contenido principal"""
        main_container = ctk.CTkFrame(self.ventana, fg_color=Colores.BG_PRIMARY, corner_radius=0)
        main_container.grid(row=1, column=0, sticky='nsew', padx=Espaciado.MEDIO, pady=Espaciado.MEDIO)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        self.crear_formulario_moderno(main_container)
        self.crear_lista_moderna(main_container)
        self.crear_botones_modernos(main_container)

    def crear_formulario_moderno(self, parent):
        """Crear formulario moderno con CustomTkinter"""
        form_frame = ctk.CTkFrame(parent, **estilo_card())
        form_frame.grid(row=0, column=0, sticky='ew', pady=(0, Espaciado.NORMAL))

        # Header del formulario
        form_header = ctk.CTkFrame(
            form_frame,
            fg_color=Colores.PRIMARY_START,
            height=45,
            corner_radius=Dimensiones.RADIUS_NORMAL
        )
        form_header.pack(fill='x', padx=2, pady=2)
        form_header.pack_propagate(False)

        ctk.CTkLabel(
            form_header,
            text=f"{Iconos.EDITAR} Información del Cliente",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(pady=Espaciado.PEQUENO)

        # Contenido del formulario
        content_frame = ctk.CTkFrame(form_frame, fg_color=Colores.BG_CARD)
        content_frame.pack(fill='both', padx=Espaciado.MEDIO, pady=Espaciado.NORMAL)

        # Variables
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.ciudad_var = tk.StringVar()

        # Grid compacto - 4 columnas
        # Fila 1
        ctk.CTkLabel(
            content_frame,
            text="Nombre:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=0, column=0, sticky='w', pady=(0, Espaciado.MINI))

        ctk.CTkEntry(
            content_frame,
            textvariable=self.nombre_var,
            width=140,
            **estilo_entry()
        ).grid(row=1, column=0, padx=(0, Espaciado.PEQUENO), pady=(0, Espaciado.PEQUENO))

        ctk.CTkLabel(
            content_frame,
            text="Apellido:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=0, column=1, sticky='w', pady=(0, Espaciado.MINI))

        ctk.CTkEntry(
            content_frame,
            textvariable=self.apellido_var,
            width=140,
            **estilo_entry()
        ).grid(row=1, column=1, padx=(0, Espaciado.PEQUENO), pady=(0, Espaciado.PEQUENO))

        ctk.CTkLabel(
            content_frame,
            text=f"{Iconos.TELEFONO} Teléfono:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=0, column=2, sticky='w', pady=(0, Espaciado.MINI))

        ctk.CTkEntry(
            content_frame,
            textvariable=self.telefono_var,
            width=120,
            **estilo_entry()
        ).grid(row=1, column=2, padx=(0, Espaciado.PEQUENO), pady=(0, Espaciado.PEQUENO))

        ctk.CTkLabel(
            content_frame,
            text=f"{Iconos.UBICACION} Ciudad:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=0, column=3, sticky='w', pady=(0, Espaciado.MINI))

        ciudad_combo = ctk.CTkComboBox(
            content_frame,
            variable=self.ciudad_var,
            width=120,
            height=Dimensiones.ENTRY_HEIGHT_SMALL,
            corner_radius=Dimensiones.RADIUS_SMALL,
            values=['Santiago', 'Valparaíso', 'Concepción', 'La Serena', 'Antofagasta', 'Copiapo', 'Otra']
        )
        ciudad_combo.grid(row=1, column=3, pady=(0, Espaciado.PEQUENO))

        # Fila 2
        ctk.CTkLabel(
            content_frame,
            text=f"{Iconos.EMAIL} Email:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, Espaciado.MINI))

        ctk.CTkEntry(
            content_frame,
            textvariable=self.email_var,
            width=288,
            **estilo_entry()
        ).grid(row=3, column=0, columnspan=2, padx=(0, Espaciado.PEQUENO), pady=(0, Espaciado.PEQUENO))

        ctk.CTkLabel(
            content_frame,
            text=f"{Iconos.UBICACION} Dirección:",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).grid(row=2, column=2, columnspan=2, sticky='w', pady=(0, Espaciado.MINI))

        ctk.CTkEntry(
            content_frame,
            textvariable=self.direccion_var,
            width=248,
            **estilo_entry()
        ).grid(row=3, column=2, columnspan=2, pady=(0, Espaciado.PEQUENO))

        self.modo_edicion = False
        self.cliente_editando_id = None

    def crear_lista_moderna(self, parent):
        """Crear lista moderna con CustomTkinter"""
        list_frame = ctk.CTkFrame(parent, **estilo_card())
        list_frame.grid(row=1, column=0, sticky='nsew', pady=(0, Espaciado.PEQUENO))
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Header
        header_container = ctk.CTkFrame(list_frame, fg_color=Colores.BG_CARD, height=45)
        header_container.pack(fill='x', padx=Espaciado.NORMAL, pady=(Espaciado.PEQUENO, 0))
        header_container.pack_propagate(False)

        ctk.CTkLabel(
            header_container,
            text=f"{Iconos.REPORTES} Lista de Clientes",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MEDIANO, Fuentes.BOLD),
            text_color=Colores.PRIMARY_START
        ).pack(side='left', pady=Espaciado.MUY_PEQUENO)

        ctk.CTkLabel(
            header_container,
            text="💡 Doble clic para editar",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.ITALIC),
            text_color=Colores.TEXT_SECONDARY
        ).pack(side='right', pady=Espaciado.MUY_PEQUENO)

        # Divisor
        ctk.CTkFrame(list_frame, fg_color=Colores.BORDER_LIGHT, height=2).pack(
            fill='x', padx=Espaciado.NORMAL, pady=(0, Espaciado.PEQUENO))

        # Container del treeview
        tree_container = tk.Frame(list_frame, bg=Colores.BG_CARD)
        tree_container.pack(fill='both', expand=True, padx=Espaciado.PEQUENO, pady=Espaciado.PEQUENO)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configurar estilo
        self.style.configure("Clientes.Treeview",
                           background=Colores.BG_SECONDARY,
                           foreground=Colores.TEXT_PRIMARY,
                           fieldbackground=Colores.BG_SECONDARY,
                           font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO),
                           rowheight=28)

        self.style.configure("Clientes.Treeview.Heading",
                           background=Colores.SECONDARY,
                           foreground=Colores.TEXT_WHITE,
                           font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
                           relief='flat',
                           borderwidth=0)

        self.style.map('Clientes.Treeview',
                      background=[('selected', Colores.PRIMARY_START)],
                      foreground=[('selected', Colores.TEXT_WHITE)])

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Ciudad', 'Total Compras')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                style="Clientes.Treeview")

        headers = {
            'ID': ('ID', 50),
            'Nombre': ('Nombre', 140),
            'Apellido': ('Apellido', 140),
            'Teléfono': ('Teléfono', 110),
            'Email': ('Email', 200),
            'Ciudad': ('Ciudad', 110),
            'Total Compras': ('Total Compras', 120)
        }

        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center' if col in ['ID', 'Total Compras'] else 'w')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.tree.bind('<Double-1>', self.seleccionar_cliente)

    def crear_botones_modernos(self, parent):
        """Crear botones modernos con CustomTkinter"""
        buttons_frame = ctk.CTkFrame(parent, fg_color=Colores.BG_PRIMARY)
        buttons_frame.grid(row=2, column=0, sticky='ew', pady=(Espaciado.MUY_PEQUENO, Espaciado.PEQUENO))

        botones_config = [
            (f"{Iconos.GUARDAR} Guardar", Colores.INFO, self.guardar_cliente),
            (f"{Iconos.EDITAR} Editar", Colores.WARNING, self.editar_cliente),
            (f"{Iconos.ELIMINAR} Eliminar", Colores.DANGER, self.eliminar_cliente),
            (f"{Iconos.ACTUALIZAR} Actualizar", Colores.ACTIVO, self.cargar_clientes),
            (f"{Iconos.CERRAR} Cerrar", Colores.GRIS_MEDIO, self.cerrar_ventana)
        ]

        for texto, color, comando in botones_config:
            btn = ctk.CTkButton(
                buttons_frame,
                text=texto,
                fg_color=color,
                hover_color=obtener_color_hover(color),
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO, Fuentes.BOLD),
                width=Dimensiones.BUTTON_WIDTH_NORMAL,
                height=Dimensiones.BUTTON_HEIGHT_NORMAL,
                corner_radius=Dimensiones.RADIUS_NORMAL,
                border_width=0,
                command=comando
            )
            btn.pack(side='left', padx=Espaciado.MUY_PEQUENO)

    def cargar_clientes(self):
        """Cargar clientes en la lista"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            from models.cliente import Cliente
            clientes = Cliente.obtener_todos()

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

        for item in self.tree.get_children():
            self.tree.delete(item)

        if termino.strip():
            clientes = self.controller.buscar_clientes(termino)
        else:
            from models.cliente import Cliente
            clientes = Cliente.obtener_todos()

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

            self.nombre_var.set(valores[1])
            self.apellido_var.set(valores[2])
            self.telefono_var.set(valores[3])
            self.email_var.set(valores[4])
            self.ciudad_var.set(valores[5])

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
            if self.controller.actualizar_cliente(self.cliente_editando_id, datos):
                self.cargar_clientes()
                self.limpiar_formulario()
                self.modo_edicion = False
                self.cliente_editando_id = None
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
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
        messagebox.showinfo("Modo Edición", f"Editando: {valores[1]} {valores[2]}\nModifique los datos y presione Guardar")

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
