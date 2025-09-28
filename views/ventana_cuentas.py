"""
Ventana para gestión de cuentas corrientes - Versión completa funcional
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cuenta_controller import CuentaController

class VentanaCuentas:
    def __init__(self, parent):
        self.parent = parent
        self.controller = CuentaController()
        self.ventana = None
        self.notebook = None
        self.crear_ventana()
    
    def crear_ventana(self):
        """Crear ventana de cuentas corrientes"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Cuentas Corrientes")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg='#f5f6fa')
        
        # Modal
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Crear interfaz
        self.crear_header()
        self.crear_pestanas()
        
        # Cargar datos
        self.cargar_datos_iniciales()
    
    def crear_header(self):
        """Crear header"""
        header = tk.Frame(self.ventana, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        tk.Label(header, text="CUENTAS CORRIENTES", 
                font=("Segoe UI", 20, "bold"), fg='white', bg='#2c3e50').pack(side='left', padx=30, pady=20)
        
        # Botones
        botones_frame = tk.Frame(header, bg='#2c3e50')
        botones_frame.pack(side='right', padx=30, pady=15)
        
        btn_style = {'font': ('Segoe UI', 10, 'bold'), 'relief': 'flat', 'cursor': 'hand2', 'padx': 15, 'pady': 8}
        
        tk.Button(botones_frame, text="Actualizar", bg='#27ae60', fg='white',
                 command=self.cargar_datos_iniciales, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Resumen", bg='#3498db', fg='white',
                 command=self.mostrar_resumen, **btn_style).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="Cerrar", bg='#e74c3c', fg='white',
                 command=self.cerrar_ventana, **btn_style).pack(side='left', padx=5)
    
    def crear_pestanas(self):
        """Crear pestañas"""
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pestaña 1: Lista de cuentas
        self.crear_pestana_cuentas()
        
        # Pestaña 2: Registrar abono
        self.crear_pestana_abonos()
        
        # Pestaña 3: Historial
        self.crear_pestana_historial()
    
    def crear_pestana_cuentas(self):
        """Crear pestaña de lista de cuentas"""
        frame_cuentas = ttk.Frame(self.notebook)
        self.notebook.add(frame_cuentas, text="Lista de Cuentas")
        
        # Filtros
        filtros_frame = tk.Frame(frame_cuentas, bg='white', relief='solid', bd=1)
        filtros_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(filtros_frame, text="Filtrar por:", font=("Segoe UI", 10, "bold"), 
                bg='white').pack(side='left', padx=10, pady=10)
        
        self.filtro_var = tk.StringVar(value="Todos")
        filtros = ["Todos", "Con deuda", "Al día"]
        for filtro in filtros:
            tk.Radiobutton(filtros_frame, text=filtro, variable=self.filtro_var, value=filtro,
                          bg='white', command=self.filtrar_cuentas).pack(side='left', padx=10)
        
        # Tabla de cuentas
        self.crear_tabla_cuentas(frame_cuentas)
    
    def crear_tabla_cuentas(self, parent):
        """Crear tabla de cuentas"""
        tabla_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        tabla_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Cuentas.Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Cuentas.Treeview.Heading", font=("Segoe UI", 11, "bold"))
        
        # Treeview
        columns = ('cliente', 'deuda_total', 'saldo_pendiente', 'estado', 'ultima_act')
        self.tree_cuentas = ttk.Treeview(tabla_frame, columns=columns, show='headings', 
                                        style="Cuentas.Treeview", height=20)
        
        # Headers
        self.tree_cuentas.heading('cliente', text='Cliente')
        self.tree_cuentas.heading('deuda_total', text='Deuda Total')
        self.tree_cuentas.heading('saldo_pendiente', text='Saldo Pendiente')
        self.tree_cuentas.heading('estado', text='Estado')
        self.tree_cuentas.heading('ultima_act', text='Última Actualización')
        
        # Columnas
        self.tree_cuentas.column('cliente', width=300, anchor='w')
        self.tree_cuentas.column('deuda_total', width=150, anchor='e')
        self.tree_cuentas.column('saldo_pendiente', width=150, anchor='e')
        self.tree_cuentas.column('estado', width=100, anchor='center')
        self.tree_cuentas.column('ultima_act', width=180, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree_cuentas.yview)
        self.tree_cuentas.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree_cuentas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Evento doble clic
        self.tree_cuentas.bind('<Double-1>', self.ver_detalle_cuenta)
    
    def crear_pestana_abonos(self):
        """Crear pestaña para registrar abonos"""
        frame_abonos = ttk.Frame(self.notebook)
        self.notebook.add(frame_abonos, text="Registrar Abono")
        
        # Formulario
        form_frame = tk.LabelFrame(frame_abonos, text="Nuevo Abono", 
                                  font=("Segoe UI", 12, "bold"), bg='#f5f6fa')
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Variables
        self.cliente_abono_var = tk.StringVar()
        self.monto_abono_var = tk.StringVar()
        self.metodo_pago_var = tk.StringVar(value="Efectivo")
        self.descripcion_abono_var = tk.StringVar()
        self.recibo_var = tk.StringVar()
        
        # Fila 1: Cliente
        fila1 = tk.Frame(form_frame, bg='#f5f6fa')
        fila1.pack(fill='x', padx=20, pady=10)
        
        tk.Label(fila1, text="Cliente:", font=("Segoe UI", 10), bg='#f5f6fa').pack(side='left')
        
        # Combobox de clientes
        self.cliente_combo = ttk.Combobox(fila1, textvariable=self.cliente_abono_var, 
                                         width=50, state="readonly")
        self.cliente_combo.pack(side='left', padx=10)
        self.cliente_combo.bind('<<ComboboxSelected>>', self.cliente_seleccionado)
        
        # Fila 2: Monto y método
        fila2 = tk.Frame(form_frame, bg='#f5f6fa')
        fila2.pack(fill='x', padx=20, pady=10)
        
        tk.Label(fila2, text="Monto:", font=("Segoe UI", 10), bg='#f5f6fa').pack(side='left')
        tk.Entry(fila2, textvariable=self.monto_abono_var, font=("Segoe UI", 10), width=15).pack(side='left', padx=10)
        
        tk.Label(fila2, text="Método:", font=("Segoe UI", 10), bg='#f5f6fa').pack(side='left', padx=(20, 5))
        metodos = ["Efectivo", "Transferencia", "Cheque", "Tarjeta"]
        metodo_combo = ttk.Combobox(fila2, textvariable=self.metodo_pago_var, values=metodos, width=15)
        metodo_combo.pack(side='left', padx=5)
        
        # Fila 3: Descripción y recibo
        fila3 = tk.Frame(form_frame, bg='#f5f6fa')
        fila3.pack(fill='x', padx=20, pady=10)
        
        tk.Label(fila3, text="Descripción:", font=("Segoe UI", 10), bg='#f5f6fa').pack(side='left')
        tk.Entry(fila3, textvariable=self.descripcion_abono_var, font=("Segoe UI", 10), width=25).pack(side='left', padx=10)
        
        tk.Label(fila3, text="N° Recibo:", font=("Segoe UI", 10), bg='#f5f6fa').pack(side='left', padx=(20, 5))
        tk.Entry(fila3, textvariable=self.recibo_var, font=("Segoe UI", 10), width=15).pack(side='left', padx=5)
        
        # Información del cliente seleccionado
        self.info_cliente_frame = tk.Frame(frame_abonos, bg='#ecf0f1', relief='solid', bd=1)
        self.info_cliente_frame.pack(fill='x', padx=20, pady=10)
        
        self.info_cliente_label = tk.Label(self.info_cliente_frame, 
                                          text="Seleccione un cliente para ver su información", 
                                          font=("Segoe UI", 12), bg='#ecf0f1', fg='#7f8c8d')
        self.info_cliente_label.pack(pady=20)
        
        # Botones
        botones_frame = tk.Frame(frame_abonos, bg='#f5f6fa')
        botones_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(botones_frame, text="REGISTRAR ABONO", bg='#27ae60', fg='white',
                 command=self.registrar_abono, font=("Segoe UI", 12, "bold"), 
                 padx=30, pady=10).pack(side='left', padx=10)
        
        tk.Button(botones_frame, text="Limpiar", bg='#95a5a6', fg='white',
                 command=self.limpiar_formulario_abono, font=("Segoe UI", 10, "bold"), 
                 padx=20, pady=10).pack(side='left', padx=10)
    
    def crear_pestana_historial(self):
        """Crear pestaña de historial"""
        frame_historial = ttk.Frame(self.notebook)
        self.notebook.add(frame_historial, text="Historial")
        
        # Selector de cliente
        selector_frame = tk.Frame(frame_historial, bg='white', relief='solid', bd=1)
        selector_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(selector_frame, text="Ver historial de:", font=("Segoe UI", 11, "bold"), 
                bg='white').pack(side='left', padx=10, pady=10)
        
        self.cliente_historial_var = tk.StringVar()
        
        # Obtener todos los clientes
        from models.cliente import Cliente
        clientes = Cliente.obtener_todos()
        clientes_opciones = [f"{c.id} - {c.nombre} {c.apellido}" for c in clientes]
        
        cliente_historial_combo = ttk.Combobox(selector_frame, textvariable=self.cliente_historial_var, 
                                              values=clientes_opciones, width=40, state="readonly")
        cliente_historial_combo.pack(side='left', padx=10, pady=10)
        cliente_historial_combo.bind('<<ComboboxSelected>>', self.cargar_historial_cliente)
        
        # Área de historial
        self.historial_frame = tk.Frame(frame_historial, bg='#f5f6fa')
        self.historial_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mensaje inicial
        tk.Label(self.historial_frame, text="Seleccione un cliente para ver su historial", 
                font=("Segoe UI", 14), bg='#f5f6fa', fg='#7f8c8d').pack(expand=True)
    
    def cargar_datos_iniciales(self):
        """Cargar datos iniciales"""
        try:
            # Asegurar que todos los clientes tengan cuenta corriente
            self.crear_cuentas_silenciosamente()
            
            # Cargar datos
            self.cargar_tabla_cuentas()
            self.actualizar_combo_clientes_abono()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def crear_cuentas_silenciosamente(self):
        """Crear cuentas corrientes para clientes que no las tienen (sin mostrar mensajes)"""
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
            print("DEBUG: Iniciando carga de tabla...")
            
            # Limpiar tabla
            for item in self.tree_cuentas.get_children():
                self.tree_cuentas.delete(item)
            
            # Crear cuentas silenciosamente para todos los clientes
            from models.cliente import Cliente
            from models.cuenta_corriente import CuentaCorriente
            
            clientes = Cliente.obtener_todos()
            print(f"DEBUG: Encontrados {len(clientes)} clientes")
            
            # Asegurar que todos tengan cuenta corriente
            for cliente in clientes:
                CuentaCorriente.crear_cuenta_si_no_existe(cliente.id)
            
            # Cargar cada cliente individualmente
            for cliente in clientes:
                try:
                    # Obtener información de cuenta del cliente
                    cuenta_info = self.controller.obtener_cuenta_cliente(cliente.id)
                    
                    if cuenta_info:
                        deuda_total = cuenta_info['saldo_total']
                        saldo_pendiente = cuenta_info['saldo_pendiente']
                        fecha_actualizacion = cuenta_info.get('fecha_ultima_actualizacion', 'N/A')
                    else:
                        deuda_total = 0
                        saldo_pendiente = 0
                        fecha_actualizacion = 'N/A'
                    
                    # Determinar estado
                    if saldo_pendiente == 0:
                        estado = "Al día"
                        tag = 'al_dia'
                    elif saldo_pendiente > 0:
                        estado = "Con deuda"
                        tag = 'con_deuda'
                    else:
                        estado = "Error"
                        tag = 'error'
                    
                    # Formatear fecha
                    fecha_formateada = fecha_actualizacion[:16] if fecha_actualizacion != 'N/A' else 'N/A'
                    
                    # Insertar fila
                    self.tree_cuentas.insert('', 'end', values=(
                        f"{cliente.nombre} {cliente.apellido}",
                        f"${deuda_total:,.0f}",
                        f"${saldo_pendiente:,.0f}",
                        estado,
                        fecha_formateada
                    ), tags=(tag,))
                    
                    print(f"DEBUG: Agregado {cliente.nombre} {cliente.apellido} - ${saldo_pendiente:,.0f}")
                    
                except Exception as e:
                    print(f"DEBUG: Error al procesar cliente {cliente.nombre}: {str(e)}")
                    # Insertar con valores por defecto si hay error
                    self.tree_cuentas.insert('', 'end', values=(
                        f"{cliente.nombre} {cliente.apellido}",
                        "$0",
                        "$0",
                        "Al día",
                        "N/A"
                    ), tags=('al_dia',))
            
            # Configurar colores
            self.tree_cuentas.tag_configure('al_dia', background='#d5f4e6')
            self.tree_cuentas.tag_configure('con_deuda', background='#fff3cd')
            self.tree_cuentas.tag_configure('error', background='#f8d7da')
            
            print(f"DEBUG: Carga completa, {len(self.tree_cuentas.get_children())} filas en tabla")
            
        except Exception as e:
            print(f"ERROR al cargar tabla: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def filtrar_cuentas(self):
        """Filtrar cuentas según selección"""
        try:
            filtro = self.filtro_var.get()
            print(f"DEBUG: Filtrando por: {filtro}")
            
            # Limpiar tabla
            for item in self.tree_cuentas.get_children():
                self.tree_cuentas.delete(item)
            
            if filtro == "Todos":
                # Cargar todos los datos
                self.cargar_tabla_cuentas()
                return
            
            # Para filtros específicos
            from models.cliente import Cliente
            from models.cuenta_corriente import CuentaCorriente
            
            clientes = Cliente.obtener_todos()
            
            for cliente in clientes:
                # Asegurar cuenta corriente
                CuentaCorriente.crear_cuenta_si_no_existe(cliente.id)
                
                # Obtener información de cuenta
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
                
                # Determinar estado
                estado = "Al día" if saldo_pendiente == 0 else "Con deuda"
                tag = 'al_dia' if saldo_pendiente == 0 else 'con_deuda'
                
                # Insertar fila
                self.tree_cuentas.insert('', 'end', values=(
                    f"{cliente.nombre} {cliente.apellido}",
                    f"${deuda_total:,.0f}",
                    f"${saldo_pendiente:,.0f}",
                    estado,
                    fecha[:16] if fecha != 'N/A' else 'N/A'
                ), tags=(tag,))
            
            # Configurar colores
            self.tree_cuentas.tag_configure('al_dia', background='#d5f4e6')
            self.tree_cuentas.tag_configure('con_deuda', background='#fff3cd')
            
            print(f"DEBUG: Filtro aplicado, {len(self.tree_cuentas.get_children())} filas mostradas")
            
        except Exception as e:
            print(f"ERROR al filtrar: {str(e)}")
            # Como fallback, cargar todos
            self.cargar_tabla_cuentas()
    
    def actualizar_combo_clientes_abono(self):
        """Actualizar combo de clientes para abonos - solo clientes activos"""
        try:
            # Obtener solo clientes que existen y tienen deuda
            clientes_deuda = []
        
            # Obtener cuentas con saldo pendiente
            cuentas_con_saldo = self.controller.obtener_clientes_con_deuda()
        
            # Verificar que los clientes aún existan en la base de datos
            from models.cliente import Cliente
            clientes_existentes = Cliente.obtener_todos()
            ids_existentes = [c.id for c in clientes_existentes]
        
            # Filtrar solo clientes que existen
            for cuenta in cuentas_con_saldo:
                if cuenta[0] in ids_existentes:  # cuenta[0] es el cliente_id
                    clientes_deuda.append(cuenta)
        
            if clientes_deuda:
                clientes_opciones = [f"{c[0]} - {c[1]} {c[2]} (Debe: ${c[3]:,.0f})" for c in clientes_deuda]
            else:
                # Si no hay clientes con deuda, mostrar todos los clientes existentes
                clientes_opciones = [f"{c.id} - {c.nombre} {c.apellido} (Sin deuda)" for c in clientes_existentes]
        
            self.cliente_combo['values'] = clientes_opciones
        
            # Limpiar selección si el cliente ya no existe
            if self.cliente_abono_var.get():
                seleccion_actual = self.cliente_abono_var.get()
                if seleccion_actual not in clientes_opciones:
                    self.cliente_abono_var.set("")
                    self.info_cliente_label.config(text="Seleccione un cliente para ver su información", fg='#7f8c8d')
        
        except Exception as e:
            print(f"Error al actualizar combo: {str(e)}")
            self.cliente_combo['values'] = []
    
    def cliente_seleccionado(self, event):
        """Cuando se selecciona un cliente para abono"""
        seleccion = self.cliente_abono_var.get()
        if seleccion:
            cliente_id = int(seleccion.split(' - ')[0])
            
            # Obtener información de la cuenta
            cuenta_info = self.controller.obtener_cuenta_cliente(cliente_id)
            
            if cuenta_info:
                info_text = f"""Cliente: {cuenta_info['nombre_cliente']}
Deuda Total: ${cuenta_info['saldo_total']:,.0f}
Saldo Pendiente: ${cuenta_info['saldo_pendiente']:,.0f}
Última Actualización: {cuenta_info['fecha_ultima_actualizacion'][:16] if cuenta_info['fecha_ultima_actualizacion'] else 'N/A'}"""
                
                self.info_cliente_label.config(text=info_text, fg='#2c3e50', justify='left')
            else:
                self.info_cliente_label.config(text="Error al cargar información del cliente", fg='#e74c3c')
    
    def registrar_abono(self):
        """Registrar un abono"""
        try:
            # Validar campos
            if not self.cliente_abono_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return
            
            if not self.monto_abono_var.get():
                messagebox.showwarning("Advertencia", "Ingrese el monto del abono")
                return
            
            # Obtener datos
            seleccion = self.cliente_abono_var.get()
            cliente_id = int(seleccion.split(' - ')[0])
            monto = float(self.monto_abono_var.get())
            metodo_pago = self.metodo_pago_var.get()
            descripcion = self.descripcion_abono_var.get()
            recibo = self.recibo_var.get()
            
            # Registrar abono
            exito, mensaje = self.controller.registrar_abono(
                cliente_id, monto, metodo_pago, descripcion, recibo
            )
            
            if exito:
                # Obtener nombre del cliente
                try:
                    # Extraer nombre del cliente de la selección
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
                
                # Limpiar formulario
                self.limpiar_formulario_abono()
                
                # Actualizar datos
                self.cargar_datos_iniciales()
                
                # Mensaje de confirmación
                messagebox.showinfo("Éxito", 
                                  f"Abono registrado correctamente\n\n" +
                                  f"Cliente: {cliente_nombre}\n" +
                                  f"Monto: ${monto:,.0f}\n" +
                                  f"Método: {metodo_pago}")
            
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar abono: {str(e)}")
    
    def limpiar_formulario_abono(self):
        """Limpiar formulario de abono"""
        self.cliente_abono_var.set('')
        self.monto_abono_var.set('')
        self.metodo_pago_var.set('Efectivo')
        self.descripcion_abono_var.set('')
        self.recibo_var.set('')
        self.info_cliente_label.config(text="Seleccione un cliente para ver su información", fg='#7f8c8d')
    
    def cargar_historial_cliente(self, event):
        """Cargar historial de un cliente específico"""
        seleccion = self.cliente_historial_var.get()
        if not seleccion:
            return
        
        cliente_id = int(seleccion.split(' - ')[0])
        
        # Limpiar frame anterior
        for widget in self.historial_frame.winfo_children():
            widget.destroy()
        
        # Obtener historial
        historial = self.controller.obtener_historial_cliente(cliente_id)
        
        if not historial:
            tk.Label(self.historial_frame, text="No se pudo cargar el historial", 
                    font=("Segoe UI", 12), bg='#f5f6fa', fg='#e74c3c').pack(expand=True)
            return
        
        # Información de cuenta
        cuenta_info = historial['cuenta_info']
        if cuenta_info:
            info_frame = tk.LabelFrame(self.historial_frame, text="Información de Cuenta", 
                                     font=("Segoe UI", 12, "bold"), bg='#f5f6fa')
            info_frame.pack(fill='x', padx=10, pady=10)
            
            info_grid = tk.Frame(info_frame, bg='#f5f6fa')
            info_grid.pack(fill='x', padx=20, pady=15)
            
            # Tarjetas de información
            tarjetas = [
                ("Deuda Total", f"${cuenta_info['saldo_total']:,.0f}", "#3498db"),
                ("Saldo Pendiente", f"${cuenta_info['saldo_pendiente']:,.0f}", "#e74c3c"),
                ("Estado", "Al día" if cuenta_info['saldo_pendiente'] == 0 else "Con deuda", 
                 "#27ae60" if cuenta_info['saldo_pendiente'] == 0 else "#f39c12")
            ]
            
            for i, (titulo, valor, color) in enumerate(tarjetas):
                tarjeta = tk.Frame(info_grid, bg=color, relief='flat', bd=0, width=150, height=80)
                tarjeta.grid(row=0, column=i, padx=10, pady=5)
                tarjeta.pack_propagate(False)
                
                tk.Label(tarjeta, text=valor, font=("Segoe UI", 14, "bold"), 
                        bg=color, fg='white').pack(expand=True)
                tk.Label(tarjeta, text=titulo, font=("Segoe UI", 9), 
                        bg=color, fg='white').pack()
        
        # Historial de movimientos
        mov_frame = tk.LabelFrame(self.historial_frame, text="Historial de Movimientos", 
                                font=("Segoe UI", 12, "bold"), bg='#f5f6fa')
        mov_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabla de movimientos
        columns = ('fecha', 'tipo', 'monto', 'descripcion')
        tree_mov = ttk.Treeview(mov_frame, columns=columns, show='headings', height=12)
        
        tree_mov.heading('fecha', text='Fecha')
        tree_mov.heading('tipo', text='Tipo')
        tree_mov.heading('monto', text='Monto')
        tree_mov.heading('descripcion', text='Descripción')
        
        tree_mov.column('fecha', width=150, anchor='center')
        tree_mov.column('tipo', width=100, anchor='center')
        tree_mov.column('monto', width=120, anchor='e')
        tree_mov.column('descripcion', width=300, anchor='w')
        
        # Cargar movimientos
        movimientos = historial['movimientos']
        for mov in movimientos:
            tipo = mov[0]
            monto = mov[1]
            descripcion = mov[2]
            fecha = mov[3][:16] if mov[3] else 'N/A'
            
            # Color según tipo
            tag = 'cargo' if tipo == 'CARGO' else 'abono'
            tipo_text = "Cargo" if tipo == 'CARGO' else "Abono"
            
            tree_mov.insert('', 'end', values=(
                fecha,
                tipo_text,
                f"${monto:,.0f}",
                descripcion
            ), tags=(tag,))
        
        # Configurar colores
        tree_mov.tag_configure('cargo', background='#ffebee')
        tree_mov.tag_configure('abono', background='#e8f5e8')
        
        # Scrollbar
        scroll_mov = ttk.Scrollbar(mov_frame, orient='vertical', command=tree_mov.yview)
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
        
        # Buscar cliente por nombre para obtener ID
        from models.cliente import Cliente
        clientes = Cliente.obtener_todos()
        cliente_id = None
        
        for cliente in clientes:
            if f"{cliente.nombre} {cliente.apellido}" == nombre_cliente:
                cliente_id = cliente.id
                break
        
        if cliente_id:
            # Cambiar a pestaña de historial y seleccionar cliente
            self.notebook.select(2)  # Pestaña de historial
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