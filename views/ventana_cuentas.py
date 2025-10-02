"""
Ventana para gestión de cuentas corrientes - Diseño Moderno con CustomTkinter
Versión con estilos unificados
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.cuenta_controller import CuentaController
from config.estilos import (Colores, Fuentes, Espaciado, Dimensiones,
                            Iconos, obtener_color_hover)

class VentanaCuentas:
    def __init__(self, parent):
        self.parent = parent
        self.controller = CuentaController()
        self.ventana = None
        self.notebook = None
        self.crear_ventana()

    def crear_ventana(self):
        """Crear ventana de cuentas corrientes con CustomTkinter"""
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Cuentas Corrientes - Sistema Pro")
        self.ventana.geometry("1500x900")
        self.ventana.configure(bg=Colores.BG_PRIMARY)

        # Modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()

        # Grid principal
        self.ventana.grid_rowconfigure(1, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)

        # Crear interfaz
        self.crear_header()
        self.crear_contenido_principal()

        # Cargar datos
        self.cargar_datos_iniciales()

    def crear_header(self):
        """Crear header con CustomTkinter y gradiente"""
        # Header con gradiente
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
        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.grid(row=0, column=0, sticky='w', padx=Espaciado.XXL, pady=Espaciado.MEDIO)

        ctk.CTkLabel(
            titulo_frame,
            text=f"{Iconos.CUENTAS} CUENTAS CORRIENTES",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.XL, Fuentes.BOLD),
            text_color=Colores.TEXT_WHITE
        ).pack(anchor='w')

        ctk.CTkLabel(
            titulo_frame,
            text="Gestión de créditos y pagos de clientes",
            font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.PEQUENO),
            text_color='#e8eaf6'
        ).pack(anchor='w', pady=(3, 0))

        # Botones derecha
        botones_frame = ctk.CTkFrame(header, fg_color="transparent")
        botones_frame.grid(row=0, column=1, sticky='e', padx=Espaciado.XXL, pady=Espaciado.MEDIO)

        btn_configs = [
            (f"{Iconos.ACTUALIZAR} Actualizar", Colores.ACTIVO, self.cargar_datos_iniciales),
            (f"{Iconos.REPORTES} Resumen", '#9b59b6', self.mostrar_resumen),
            (f"{Iconos.CERRAR} Cerrar", Colores.DANGER, self.cerrar_ventana)
        ]

        for texto, color, comando in btn_configs:
            btn = ctk.CTkButton(
                botones_frame,
                text=texto,
                fg_color=color,
                hover_color=obtener_color_hover(color),
                font=(Fuentes.FAMILIA_PRINCIPAL, Fuentes.MUY_PEQUENO, Fuentes.BOLD),
                width=130,
                height=Dimensiones.BUTTON_HEIGHT_NORMAL,
                corner_radius=Dimensiones.RADIUS_NORMAL,
                command=comando
            )
            btn.pack(side='left', padx=Espaciado.MUY_PEQUENO)

    def _darken_color(self, color):
        """Oscurecer color para efecto hover"""
        colors = {
            '#10ac84': '#0e9670',
            '#9b59b6': '#8e44ad',
            '#ff3838': '#e62020'
        }
        return colors.get(color, color)

    def crear_contenido_principal(self):
        """Crear contenido principal con pestañas modernas"""
        # Container principal
        main_container = ctk.CTkFrame(self.ventana, fg_color='#f0f2f5', corner_radius=0)
        main_container.grid(row=1, column=0, sticky='nsew', padx=25, pady=20)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Crear pestañas con ttk.Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)

        # Configurar estilo del notebook
        style = ttk.Style()
        style.configure('TNotebook', background='#f0f2f5', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 11, 'bold'))

        # Pestaña 1: Lista de cuentas
        self.crear_pestana_cuentas()

        # Pestaña 2: Registrar abono
        self.crear_pestana_abonos()

        # Pestaña 3: Historial
        self.crear_pestana_historial()

    def crear_pestana_cuentas(self):
        """Crear pestaña de lista de cuentas con diseño moderno"""
        # Frame principal
        frame_cuentas = ctk.CTkFrame(self.notebook, fg_color='white', corner_radius=0)
        self.notebook.add(frame_cuentas, text="  📋 Lista de Cuentas  ")

        # Panel de filtros y búsqueda
        filtros_card = ctk.CTkFrame(frame_cuentas, fg_color='#f8f9fa', corner_radius=12,
                                   border_width=1, border_color='#e9ecef')
        filtros_card.pack(fill='x', padx=20, pady=20)

        # Container interno de filtros
        filtros_content = ctk.CTkFrame(filtros_card, fg_color='transparent')
        filtros_content.pack(fill='x', padx=20, pady=15)

        # Sección izquierda - Filtros
        filtros_left = ctk.CTkFrame(filtros_content, fg_color='transparent')
        filtros_left.pack(side='left', fill='y')

        ctk.CTkLabel(filtros_left, text="🔍 Filtrar:",
                    font=("Segoe UI", 12, "bold"),
                    text_color='#667eea').pack(side='left', padx=(0, 15))

        self.filtro_var = tk.StringVar(value="Todos")
        filtros = [("Todos", "Todos"), ("Con deuda", "Con deuda"), ("Al día", "Al día")]

        for texto, valor in filtros:
            rb = ctk.CTkRadioButton(filtros_left, text=texto,
                                   variable=self.filtro_var, value=valor,
                                   font=("Segoe UI", 10),
                                   command=self.filtrar_cuentas,
                                   fg_color='#667eea',
                                   hover_color='#5568d3')
            rb.pack(side='left', padx=8)

        # Sección derecha - Búsqueda
        buscar_outer_frame = ctk.CTkFrame(filtros_content, fg_color='transparent')
        buscar_outer_frame.pack(side='right', padx=10)

        # Container para barra de búsqueda con icono
        search_container = ctk.CTkFrame(
            buscar_outer_frame,
            fg_color=Colores.BG_SECONDARY,
            corner_radius=Dimensiones.RADIUS_SMALL,
            height=36
        )
        search_container.pack(side='left')

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
        self.buscar_var.trace('w', self.buscar_cuentas)

        search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.buscar_var,
            placeholder_text="Buscar cliente...",
            font=("Segoe UI", 11),
            width=240,
            height=36,
            corner_radius=0,
            border_width=0,
            fg_color=Colores.BG_SECONDARY,
            text_color=Colores.TEXT_PRIMARY
        )
        search_entry.pack(side='left', padx=(0, Espaciado.PEQUENO))

        # Divisor
        ctk.CTkFrame(frame_cuentas, fg_color='#e9ecef', height=2).pack(fill='x', padx=20, pady=(0, 20))

        # Tabla de cuentas
        self.crear_tabla_cuentas(frame_cuentas)

    def crear_tabla_cuentas(self, parent):
        """Crear tabla de cuentas moderna"""
        tabla_frame = ctk.CTkFrame(parent, fg_color='white', corner_radius=0)
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Configurar estilo
        style = ttk.Style()
        style.configure("Cuentas.Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       font=("Segoe UI", 10),
                       rowheight=38)

        style.configure("Cuentas.Treeview.Heading",
                       background="#667eea",
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       relief='flat')

        style.map('Cuentas.Treeview',
                 background=[('selected', '#667eea')],
                 foreground=[('selected', 'white')])

        # Treeview
        columns = ('cliente', 'deuda_total', 'saldo_pendiente', 'estado', 'ultima_act')
        self.tree_cuentas = ttk.Treeview(tabla_frame, columns=columns, show='headings',
                                        style="Cuentas.Treeview", height=18)

        # Headers
        self.tree_cuentas.heading('cliente', text='👤 Cliente')
        self.tree_cuentas.heading('deuda_total', text='💰 Deuda Total')
        self.tree_cuentas.heading('saldo_pendiente', text='📊 Saldo Pendiente')
        self.tree_cuentas.heading('estado', text='📍 Estado')
        self.tree_cuentas.heading('ultima_act', text='🕐 Última Actualización')

        # Columnas
        self.tree_cuentas.column('cliente', width=350, anchor='w')
        self.tree_cuentas.column('deuda_total', width=160, anchor='center')
        self.tree_cuentas.column('saldo_pendiente', width=180, anchor='center')
        self.tree_cuentas.column('estado', width=140, anchor='center')
        self.tree_cuentas.column('ultima_act', width=220, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree_cuentas.yview)
        self.tree_cuentas.configure(yscrollcommand=scrollbar.set)

        self.tree_cuentas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Evento doble clic
        self.tree_cuentas.bind('<Double-1>', self.ver_detalle_cuenta)

    def crear_pestana_abonos(self):
        """Crear pestaña para registrar abonos moderna"""
        # Frame principal
        frame_abonos = ctk.CTkFrame(self.notebook, fg_color='white', corner_radius=0)
        self.notebook.add(frame_abonos, text="  💵 Registrar Abono  ")

        # Card del formulario
        form_card = ctk.CTkFrame(frame_abonos, fg_color='white', corner_radius=12,
                                border_width=1, border_color='#e9ecef')
        form_card.pack(fill='x', padx=30, pady=30)

        # Header del formulario
        header_form = ctk.CTkFrame(form_card, fg_color='#667eea', height=60, corner_radius=10)
        header_form.pack(fill='x', padx=2, pady=2)
        header_form.pack_propagate(False)

        ctk.CTkLabel(header_form, text="💳 Nuevo Abono",
                    font=("Segoe UI", 16, "bold"),
                    text_color='white').pack(expand=True)

        # Contenido del formulario
        form_content = ctk.CTkFrame(form_card, fg_color='white')
        form_content.pack(fill='x', padx=30, pady=25)

        # Variables
        self.cliente_abono_var = tk.StringVar()
        self.monto_abono_var = tk.StringVar()
        self.metodo_pago_var = tk.StringVar(value="Efectivo")
        self.descripcion_abono_var = tk.StringVar()
        self.recibo_var = tk.StringVar()

        # Generar número de recibo automáticamente
        self.generar_numero_recibo_abono()

        # Grid para campos
        form_content.grid_columnconfigure(1, weight=1)
        form_content.grid_columnconfigure(3, weight=1)

        row = 0

        # Cliente (ancho completo)
        ctk.CTkLabel(form_content, text="👤 Cliente:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').grid(row=row, column=0, sticky='w', pady=(0, 5))

        self.cliente_combo = ttk.Combobox(form_content, textvariable=self.cliente_abono_var,
                                         state="readonly", font=("Segoe UI", 10), width=70)
        self.cliente_combo.grid(row=row+1, column=0, columnspan=4, sticky='ew', pady=(0, 20))
        self.cliente_combo.bind('<<ComboboxSelected>>', self.cliente_seleccionado)
        row += 2

        # Monto y Método (dos columnas)
        ctk.CTkLabel(form_content, text="💵 Monto:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').grid(row=row, column=0, sticky='w', pady=(0, 5))

        monto_entry = ctk.CTkEntry(form_content, textvariable=self.monto_abono_var,
                                  font=("Segoe UI", 11),
                                  width=250, height=36,
                                  corner_radius=8,
                                  border_width=1,
                                  border_color='#dee2e6')
        monto_entry.grid(row=row+1, column=0, sticky='w', pady=(0, 20))

        ctk.CTkLabel(form_content, text="💳 Método de Pago:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').grid(row=row, column=2, sticky='w', padx=(30, 0), pady=(0, 5))

        metodos = ["Efectivo", "Transferencia", "Cheque", "Tarjeta"]
        metodo_combo = ttk.Combobox(form_content, textvariable=self.metodo_pago_var,
                                    values=metodos, font=("Segoe UI", 10), width=28)
        metodo_combo.grid(row=row+1, column=2, sticky='w', padx=(30, 0), pady=(0, 20))
        row += 2

        # Descripción y Recibo (dos columnas)
        ctk.CTkLabel(form_content, text="📝 Descripción:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').grid(row=row, column=0, sticky='w', pady=(0, 5))

        desc_entry = ctk.CTkEntry(form_content, textvariable=self.descripcion_abono_var,
                                 font=("Segoe UI", 11),
                                 width=250, height=36,
                                 corner_radius=8,
                                 border_width=1,
                                 border_color='#dee2e6')
        desc_entry.grid(row=row+1, column=0, sticky='w', pady=(0, 20))

        ctk.CTkLabel(form_content, text="🧾 N° Recibo:",
                    font=("Segoe UI", 11, "bold"),
                    text_color='#667eea').grid(row=row, column=2, sticky='w', padx=(30, 0), pady=(0, 5))

        recibo_entry = ctk.CTkEntry(form_content, textvariable=self.recibo_var,
                                   font=("Segoe UI", 11, "bold"),
                                   width=250, height=36,
                                   corner_radius=8,
                                   border_width=1,
                                   border_color='#dee2e6',
                                   state='readonly',
                                   fg_color='#f8f9fa',
                                   text_color='#667eea')
        recibo_entry.grid(row=row+1, column=2, sticky='w', padx=(30, 0), pady=(0, 20))

        # Panel de información del cliente
        info_card = ctk.CTkFrame(frame_abonos, fg_color='#f8f9fa', corner_radius=12,
                                border_width=1, border_color='#e9ecef')
        info_card.pack(fill='x', padx=30, pady=(0, 20))

        self.info_cliente_label = ctk.CTkLabel(info_card,
                                              text="ℹ️  Seleccione un cliente para ver su información",
                                              font=("Segoe UI", 12),
                                              text_color='#6c757d')
        self.info_cliente_label.pack(pady=25, padx=20)

        # Botones
        botones_frame = ctk.CTkFrame(frame_abonos, fg_color='white')
        botones_frame.pack(fill='x', padx=30, pady=(0, 30))

        btn_registrar = ctk.CTkButton(botones_frame, text="✓ REGISTRAR ABONO",
                                      fg_color='#10ac84',
                                      hover_color='#0e9670',
                                      font=("Segoe UI", 12, "bold"),
                                      width=200, height=42,
                                      corner_radius=10,
                                      command=self.registrar_abono)
        btn_registrar.pack(side='left', padx=10)

        btn_limpiar = ctk.CTkButton(botones_frame, text="🗑️ Limpiar",
                                    fg_color='#9b59b6',
                                    hover_color='#8e44ad',
                                    font=("Segoe UI", 11, "bold"),
                                    width=150, height=42,
                                    corner_radius=10,
                                    command=self.limpiar_formulario_abono)
        btn_limpiar.pack(side='left', padx=10)

    def crear_pestana_historial(self):
        """Crear pestaña de historial moderna"""
        # Frame principal
        frame_historial = ctk.CTkFrame(self.notebook, fg_color='white', corner_radius=0)
        self.notebook.add(frame_historial, text="  📜 Historial  ")

        # Selector de cliente
        selector_card = ctk.CTkFrame(frame_historial, fg_color='#f8f9fa', corner_radius=12,
                                    border_width=1, border_color='#e9ecef')
        selector_card.pack(fill='x', padx=30, pady=30)

        selector_content = ctk.CTkFrame(selector_card, fg_color='transparent')
        selector_content.pack(fill='x', padx=25, pady=20)

        ctk.CTkLabel(selector_content, text="📊 Seleccionar Cliente:",
                    font=("Segoe UI", 13, "bold"),
                    text_color='#667eea').pack(side='left', padx=(0, 15))

        self.cliente_historial_var = tk.StringVar()

        # Obtener clientes
        from models.cliente import Cliente
        clientes = Cliente.obtener_todos()
        clientes_opciones = [f"{c.id} - {c.nombre} {c.apellido}" for c in clientes]

        cliente_historial_combo = ttk.Combobox(selector_content,
                                              textvariable=self.cliente_historial_var,
                                              values=clientes_opciones,
                                              width=50,
                                              state="readonly",
                                              font=("Segoe UI", 11))
        cliente_historial_combo.pack(side='left', ipady=6)
        cliente_historial_combo.bind('<<ComboboxSelected>>', self.cargar_historial_cliente)

        # Área de historial
        self.historial_frame = ctk.CTkFrame(frame_historial, fg_color='white')
        self.historial_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        # Mensaje inicial
        ctk.CTkLabel(self.historial_frame,
                    text="📋 Seleccione un cliente para ver su historial de movimientos",
                    font=("Segoe UI", 14),
                    text_color='#6c757d').pack(expand=True)

    def cargar_datos_iniciales(self):
        """Cargar datos iniciales"""
        try:
            self.crear_cuentas_silenciosamente()
            self.cargar_tabla_cuentas()
            self.actualizar_combo_clientes_abono()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def crear_cuentas_silenciosamente(self):
        """Crear cuentas corrientes para clientes que no las tienen"""
        try:
            from models.cliente import Cliente
            from models.cuenta_corriente import CuentaCorriente

            clientes = Cliente.obtener_todos()
            for cliente in clientes:
                CuentaCorriente.crear_cuenta_si_no_existe(cliente.id)
        except Exception as e:
            print(f"Error al crear cuentas: {str(e)}")

    def cargar_tabla_cuentas(self):
        """Cargar datos en la tabla de cuentas"""
        try:
            # Limpiar tabla
            for item in self.tree_cuentas.get_children():
                self.tree_cuentas.delete(item)

            # Obtener cuentas con saldo
            from models.cuenta_corriente import CuentaCorriente
            cuentas_con_saldo = CuentaCorriente.obtener_todas_las_cuentas()

            for cuenta in cuentas_con_saldo:
                try:
                    cliente_id, nombre, apellido, saldo_total, saldo_pendiente, fecha_actualizacion = cuenta

                    if saldo_pendiente > 0:
                        estado = "Con deuda"
                        tag = 'con_deuda'
                    else:
                        estado = "Al día"
                        tag = 'al_dia'

                    fecha_formateada = fecha_actualizacion[:16] if fecha_actualizacion else 'N/A'

                    self.tree_cuentas.insert('', 'end', values=(
                        f"{nombre} {apellido}",
                        f"${saldo_total:,.0f}",
                        f"${saldo_pendiente:,.0f}",
                        estado,
                        fecha_formateada
                    ), tags=(tag,))

                except Exception as e:
                    print(f"Error al procesar cuenta: {str(e)}")

            # Configurar colores
            self.tree_cuentas.tag_configure('al_dia', background='#d4edda', foreground='#155724')
            self.tree_cuentas.tag_configure('con_deuda', background='#fff3cd', foreground='#856404')

        except Exception as e:
            print(f"ERROR al cargar tabla: {str(e)}")

    def filtrar_cuentas(self):
        """Filtrar cuentas según selección"""
        try:
            filtro = self.filtro_var.get()

            # Limpiar tabla
            for item in self.tree_cuentas.get_children():
                self.tree_cuentas.delete(item)

            if filtro == "Todos":
                self.cargar_tabla_cuentas()
                return

            from models.cliente import Cliente
            from models.cuenta_corriente import CuentaCorriente

            clientes = Cliente.obtener_todos()

            for cliente in clientes:
                CuentaCorriente.crear_cuenta_si_no_existe(cliente.id)
                cuenta_info = self.controller.obtener_cuenta_cliente(cliente.id)

                if cuenta_info:
                    saldo_pendiente = cuenta_info['saldo_pendiente']
                    deuda_total = cuenta_info['saldo_total']
                    fecha = cuenta_info.get('fecha_ultima_actualizacion', 'N/A')
                else:
                    saldo_pendiente = 0
                    deuda_total = 0
                    fecha = 'N/A'

                # Aplicar filtro
                if filtro == "Con deuda" and saldo_pendiente <= 0:
                    continue
                elif filtro == "Al día" and saldo_pendiente > 0:
                    continue

                estado = "Al día" if saldo_pendiente == 0 else "Con deuda"
                tag = 'al_dia' if saldo_pendiente == 0 else 'con_deuda'

                self.tree_cuentas.insert('', 'end', values=(
                    f"{cliente.nombre} {cliente.apellido}",
                    f"${deuda_total:,.0f}",
                    f"${saldo_pendiente:,.0f}",
                    estado,
                    fecha[:16] if fecha != 'N/A' else 'N/A'
                ), tags=(tag,))

            self.tree_cuentas.tag_configure('al_dia', background='#d4edda', foreground='#155724')
            self.tree_cuentas.tag_configure('con_deuda', background='#fff3cd', foreground='#856404')

        except Exception as e:
            print(f"ERROR al filtrar: {str(e)}")
            self.cargar_tabla_cuentas()

    def buscar_cuentas(self, *args):
        """Buscar cuentas por nombre de cliente"""
        try:
            termino = self.buscar_var.get().lower()
            filtro = self.filtro_var.get()

            # Limpiar tabla
            for item in self.tree_cuentas.get_children():
                self.tree_cuentas.delete(item)

            from models.cliente import Cliente
            from models.cuenta_corriente import CuentaCorriente

            clientes = Cliente.obtener_todos()

            for cliente in clientes:
                if termino.strip():
                    nombre_completo = f"{cliente.nombre} {cliente.apellido}".lower()
                    if termino not in nombre_completo:
                        continue

                CuentaCorriente.crear_cuenta_si_no_existe(cliente.id)
                cuenta_info = self.controller.obtener_cuenta_cliente(cliente.id)

                if cuenta_info:
                    saldo_pendiente = cuenta_info['saldo_pendiente']
                    deuda_total = cuenta_info['saldo_total']
                    fecha = cuenta_info.get('fecha_ultima_actualizacion', 'N/A')
                else:
                    saldo_pendiente = 0
                    deuda_total = 0
                    fecha = 'N/A'

                if filtro == "Con deuda" and saldo_pendiente <= 0:
                    continue
                elif filtro == "Al día" and saldo_pendiente > 0:
                    continue

                estado = "Con deuda" if saldo_pendiente > 0 else "Al día"
                tag = 'con_deuda' if saldo_pendiente > 0 else 'al_dia'

                self.tree_cuentas.insert('', 'end', values=(
                    f"{cliente.nombre} {cliente.apellido}",
                    f"${deuda_total:,.0f}",
                    f"${saldo_pendiente:,.0f}",
                    estado,
                    fecha[:16] if fecha != 'N/A' else 'N/A'
                ), tags=(tag,))

            self.tree_cuentas.tag_configure('al_dia', background='#d4edda', foreground='#155724')
            self.tree_cuentas.tag_configure('con_deuda', background='#fff3cd', foreground='#856404')

        except Exception as e:
            print(f"ERROR al buscar: {str(e)}")
            self.cargar_tabla_cuentas()

    def actualizar_combo_clientes_abono(self):
        """Actualizar combo de clientes para abonos"""
        try:
            from models.cliente import Cliente
            clientes_existentes = Cliente.obtener_todos()

            cuentas_con_saldo = self.controller.obtener_clientes_con_deuda()
            ids_existentes = [c.id for c in clientes_existentes]

            clientes_deuda = []
            for cuenta in cuentas_con_saldo:
                if cuenta[0] in ids_existentes:
                    clientes_deuda.append(cuenta)

            if clientes_deuda:
                clientes_opciones = [f"{c[0]} - {c[1]} {c[2]} (Debe: ${c[3]:,.0f})" for c in clientes_deuda]
            else:
                clientes_opciones = [f"{c.id} - {c.nombre} {c.apellido} (Sin deuda)" for c in clientes_existentes]

            self.cliente_combo['values'] = clientes_opciones

            if self.cliente_abono_var.get():
                seleccion_actual = self.cliente_abono_var.get()
                if seleccion_actual not in clientes_opciones:
                    self.cliente_abono_var.set("")
                    self.info_cliente_label.configure(text="ℹ️  Seleccione un cliente para ver su información",
                                                     text_color='#6c757d')

        except Exception as e:
            print(f"Error al actualizar combo: {str(e)}")
            self.cliente_combo['values'] = []

    def cliente_seleccionado(self, event):
        """Cuando se selecciona un cliente para abono"""
        seleccion = self.cliente_abono_var.get()
        if seleccion:
            cliente_id = int(seleccion.split(' - ')[0])
            cuenta_info = self.controller.obtener_cuenta_cliente(cliente_id)

            if cuenta_info:
                info_text = f"""📌 Cliente: {cuenta_info['nombre_cliente']}
💰 Deuda Total: ${cuenta_info['saldo_total']:,.0f}
📊 Saldo Pendiente: ${cuenta_info['saldo_pendiente']:,.0f}
🕐 Última Actualización: {cuenta_info['fecha_ultima_actualizacion'][:16] if cuenta_info['fecha_ultima_actualizacion'] else 'N/A'}"""

                self.info_cliente_label.configure(text=info_text, text_color='#2c3e50')
            else:
                self.info_cliente_label.configure(text="❌ Error al cargar información del cliente",
                                                 text_color='#dc3545')

    def registrar_abono(self):
        """Registrar un abono"""
        try:
            if not self.cliente_abono_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return

            if not self.monto_abono_var.get():
                messagebox.showwarning("Advertencia", "Ingrese el monto del abono")
                return

            seleccion = self.cliente_abono_var.get()
            cliente_id = int(seleccion.split(' - ')[0])
            monto = float(self.monto_abono_var.get())
            metodo_pago = self.metodo_pago_var.get()
            descripcion = self.descripcion_abono_var.get()
            recibo = self.recibo_var.get()

            exito, mensaje = self.controller.registrar_abono(
                cliente_id, monto, metodo_pago, descripcion, recibo
            )

            if exito:
                try:
                    partes = seleccion.split(' - ')
                    if len(partes) > 1:
                        nombre_parte = partes[1]
                        if '(' in nombre_parte:
                            cliente_nombre = nombre_parte.split(' (')[0]
                        else:
                            cliente_nombre = nombre_parte
                    else:
                        cliente_nombre = "Cliente"
                except:
                    cliente_nombre = "Cliente"

                self.limpiar_formulario_abono()
                self.cargar_datos_iniciales()

                messagebox.showinfo("Éxito",
                                  f"Abono registrado correctamente\n\n" +
                                  f"Cliente: {cliente_nombre}\n" +
                                  f"Monto: ${monto:,.0f}\n" +
                                  f"Método: {metodo_pago}")

        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar abono: {str(e)}")

    def generar_numero_recibo_abono(self):
        """Generar número de recibo automático para abonos"""
        try:
            numero_recibo = self.controller.generar_numero_recibo_abono()
            self.recibo_var.set(numero_recibo)
        except Exception as e:
            print(f"Error al generar número de recibo: {str(e)}")
            from datetime import datetime
            self.recibo_var.set(f"ABO-{datetime.now().strftime('%Y%m%d')}-0001")

    def limpiar_formulario_abono(self):
        """Limpiar formulario de abono"""
        self.cliente_abono_var.set('')
        self.monto_abono_var.set('')
        self.metodo_pago_var.set('Efectivo')
        self.descripcion_abono_var.set('')

        # Generar nuevo número de recibo
        self.generar_numero_recibo_abono()

        self.info_cliente_label.configure(text="ℹ️  Seleccione un cliente para ver su información",
                                         text_color='#6c757d')

    def cargar_historial_cliente(self, event):
        """Cargar historial de un cliente específico"""
        seleccion = self.cliente_historial_var.get()
        if not seleccion:
            return

        cliente_id = int(seleccion.split(' - ')[0])

        # Limpiar frame anterior
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        historial = self.controller.obtener_historial_cliente(cliente_id)

        if not historial:
            ctk.CTkLabel(self.historial_frame, text="❌ No se pudo cargar el historial",
                        font=("Segoe UI", 12),
                        text_color='#dc3545').pack(expand=True)
            return

        # Panel de información de cuenta
        cuenta_info = historial['cuenta_info']
        if cuenta_info:
            info_card = ctk.CTkFrame(self.historial_frame, fg_color='white', corner_radius=12,
                                    border_width=1, border_color='#e9ecef')
            info_card.pack(fill='x', padx=0, pady=(0, 20))

            header_info = ctk.CTkFrame(info_card, fg_color='#667eea', height=50, corner_radius=10)
            header_info.pack(fill='x', padx=2, pady=2)
            header_info.pack_propagate(False)

            ctk.CTkLabel(header_info, text="📊 Estado de Cuenta",
                        font=("Segoe UI", 14, "bold"),
                        text_color='white').pack(expand=True)

            # Cards de estadísticas
            stats_frame = ctk.CTkFrame(info_card, fg_color='white')
            stats_frame.pack(fill='x', padx=20, pady=20)

            tarjetas = [
                ("💰 Deuda Total", f"${cuenta_info['saldo_total']:,.0f}", "#9b59b6"),
                ("📊 Saldo Pendiente", f"${cuenta_info['saldo_pendiente']:,.0f}", "#ff6b6b"),
                ("📍 Estado", "✓ Al día" if cuenta_info['saldo_pendiente'] == 0 else "⚠ Con deuda",
                 "#10ac84" if cuenta_info['saldo_pendiente'] == 0 else "#f39c12")
            ]

            for i, (titulo, valor, color) in enumerate(tarjetas):
                card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10)
                card.pack(side='left', padx=10, fill='both', expand=True)

                ctk.CTkLabel(card, text=valor, font=("Segoe UI", 18, "bold"),
                            text_color='white').pack(pady=(15, 5))
                ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 10),
                            text_color='white').pack(pady=(0, 15))

        # Tabla de movimientos
        mov_card = ctk.CTkFrame(self.historial_frame, fg_color='white', corner_radius=12,
                               border_width=1, border_color='#e9ecef')
        mov_card.pack(fill='both', expand=True, padx=0)

        header_mov = ctk.CTkFrame(mov_card, fg_color='#667eea', height=50, corner_radius=10)
        header_mov.pack(fill='x', padx=2, pady=2)
        header_mov.pack_propagate(False)

        ctk.CTkLabel(header_mov, text="📜 Historial de Movimientos",
                    font=("Segoe UI", 14, "bold"),
                    text_color='white').pack(expand=True)

        # Treeview de movimientos
        tree_container = tk.Frame(mov_card, bg='white')
        tree_container.pack(fill='both', expand=True, padx=15, pady=15)

        style_hist = ttk.Style()
        style_hist.configure("Historial.Treeview",
                           background="#ffffff",
                           foreground="#2c3e50",
                           fieldbackground="#ffffff",
                           font=("Segoe UI", 10),
                           rowheight=35)

        style_hist.configure("Historial.Treeview.Heading",
                           background="#667eea",
                           foreground="white",
                           font=("Segoe UI", 11, "bold"))

        columns = ('fecha', 'tipo', 'monto', 'descripcion')
        tree_mov = ttk.Treeview(tree_container, columns=columns, show='headings',
                               height=12, style="Historial.Treeview")

        tree_mov.heading('fecha', text='📅 Fecha')
        tree_mov.heading('tipo', text='📌 Tipo')
        tree_mov.heading('monto', text='💵 Monto')
        tree_mov.heading('descripcion', text='📝 Descripción')

        tree_mov.column('fecha', width=160, anchor='center')
        tree_mov.column('tipo', width=110, anchor='center')
        tree_mov.column('monto', width=130, anchor='center')
        tree_mov.column('descripcion', width=320, anchor='w')

        # Cargar movimientos
        movimientos = historial['movimientos']
        for mov in movimientos:
            tipo = mov[0]
            monto = mov[1]
            descripcion = mov[2]
            fecha = mov[3][:16] if mov[3] else 'N/A'

            tag = 'cargo' if tipo == 'CARGO' else 'abono'
            tipo_text = "📤 Cargo" if tipo == 'CARGO' else "📥 Abono"

            tree_mov.insert('', 'end', values=(
                fecha,
                tipo_text,
                f"${monto:,.0f}",
                descripcion
            ), tags=(tag,))

        tree_mov.tag_configure('cargo', background='#ffe5e5', foreground='#c92a2a')
        tree_mov.tag_configure('abono', background='#d4edda', foreground='#155724')

        scroll_mov = ttk.Scrollbar(tree_container, orient='vertical', command=tree_mov.yview)
        tree_mov.configure(yscrollcommand=scroll_mov.set)

        tree_mov.pack(side='left', fill='both', expand=True)
        scroll_mov.pack(side='right', fill='y')

    def ver_detalle_cuenta(self, event):
        """Ver detalle de cuenta (doble clic)"""
        seleccion = self.tree_cuentas.selection()
        if not seleccion:
            return

        item = self.tree_cuentas.item(seleccion[0])
        nombre_cliente = item['values'][0]

        from models.cliente import Cliente
        clientes = Cliente.obtener_todos()
        cliente_id = None

        for cliente in clientes:
            if f"{cliente.nombre} {cliente.apellido}" == nombre_cliente:
                cliente_id = cliente.id
                break

        if cliente_id:
            self.notebook.select(2)
            self.cliente_historial_var.set(f"{cliente_id} - {nombre_cliente}")
            self.cargar_historial_cliente(None)

    def mostrar_resumen(self):
        """Mostrar resumen de cuentas corrientes"""
        resumen = self.controller.obtener_resumen_cuentas()

        resumen_text = f"""RESUMEN DE CUENTAS CORRIENTES

Clientes con deuda: {resumen['total_clientes_deuda']}
Total deuda pendiente: ${resumen['total_deuda_pendiente']:,.0f}
Total deuda acumulada: ${resumen['total_deuda_acumulada']:,.0f}
Total cobrado: ${resumen['total_deuda_acumulada'] - resumen['total_deuda_pendiente']:,.0f}

Estado general:
• Clientes al día: {len([c for c in resumen['cuentas'] if c[4] == 0])}
• Clientes con deuda: {len([c for c in resumen['cuentas'] if c[4] > 0])}
        """

        messagebox.showinfo("Resumen de Cuentas Corrientes", resumen_text)

    def cerrar_ventana(self):
        """Cerrar ventana"""
        self.ventana.destroy()
