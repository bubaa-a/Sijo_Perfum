"""
Controlador para la lógica de negocio de clientes
"""
from models.cliente import Cliente
from tkinter import messagebox
import re

class ClienteController:
    def __init__(self):
        """Inicializar el controlador de clientes"""
        pass
    
    def crear_cliente(self, datos):
        """
        Crear un nuevo cliente con validación mejorada
        datos: diccionario con los datos del cliente
        """
        try:
            print(f"CONTROLLER DEBUG: Creando cliente con datos: {datos}")
        
            # Validar datos
            errores = self.validar_datos_cliente(datos)
            if errores:
                messagebox.showerror("Error de validación", "\n".join(errores))
                return False
        
            # Crear el cliente
            cliente = Cliente(
                nombre=datos['nombre'],
                apellido=datos['apellido'],
                telefono=datos['telefono'],
                email=datos['email'],
                direccion=datos['direccion'],
                ciudad=datos['ciudad']
            )
        
            print("CONTROLLER DEBUG: Objeto cliente creado, guardando...")
        
            # Guardar en la base de datos
            if cliente.guardar():
                print("CONTROLLER DEBUG: Cliente guardado en BD")
            
                # Obtener el ID del cliente recién creado
                clientes = Cliente.obtener_todos()
                cliente_nuevo = None
                for c in clientes:
                    if (c.nombre == datos['nombre'] and 
                        c.apellido == datos['apellido'] and 
                        c.telefono == datos['telefono']):
                        cliente_nuevo = c
                        break
            
                # Crear cuenta corriente automáticamente
                if cliente_nuevo:
                    from models.cuenta_corriente import CuentaCorriente
                    CuentaCorriente.crear_cuenta_si_no_existe(cliente_nuevo.id)
                    print(f"CONTROLLER DEBUG: Cuenta corriente creada para cliente ID: {cliente_nuevo.id}")
            
                # NO mostrar messagebox aquí para evitar conflictos
                print(f"CONTROLLER DEBUG: Cliente '{cliente.nombre_completo()}' creado correctamente")
                return True
            else:
                messagebox.showerror("Error", "No se pudo guardar el cliente en la base de datos")
                return False
            
        except Exception as e:
            print(f"CONTROLLER ERROR: {str(e)}")
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")
            return False
    
    def actualizar_cliente(self, cliente_id, datos):
        """Actualizar un cliente existente"""
        try:
            # Buscar el cliente
            cliente = Cliente.buscar_por_id(cliente_id)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado")
                return False
            
            # Validar datos
            errores = self.validar_datos_cliente(datos)
            if errores:
                messagebox.showerror("Error de validación", "\n".join(errores))
                return False
            
            # Actualizar datos
            cliente.nombre = datos['nombre']
            cliente.apellido = datos['apellido']
            cliente.telefono = datos['telefono']
            cliente.email = datos['email']
            cliente.direccion = datos['direccion']
            cliente.ciudad = datos['ciudad']
            
            # Guardar cambios
            if cliente.actualizar():
                messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre_completo()}' actualizado correctamente")
                return True
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")
            return False
    
    def eliminar_cliente(self, cliente_id):
        """
        Eliminar cliente y sus datos relacionados
        """
        try:
            # Verificar si el cliente tiene ventas
            from models.venta import Venta
            ventas_cliente = Venta.obtener_por_cliente(cliente_id)
        
            if ventas_cliente:
                respuesta = messagebox.askyesno(
                    "Cliente con ventas",
                    f"Este cliente tiene {len(ventas_cliente)} venta(s) registrada(s).\n\n" +
                    "¿Desea eliminarlo de todas formas?\n" +
                    "(Se mantendrán las ventas pero sin cliente asociado)"
                )
                if not respuesta:
                    return False
        
            # Verificar si tiene cuenta corriente con deuda
            from controllers.cuenta_controller import CuentaController
            cuenta_controller = CuentaController()
            cuenta_info = cuenta_controller.obtener_cuenta_cliente(cliente_id)
        
            if cuenta_info and cuenta_info['saldo_pendiente'] > 0:
                respuesta = messagebox.askyesno(
                    "Cliente con deuda pendiente",
                    f"Este cliente tiene una deuda pendiente de ${cuenta_info['saldo_pendiente']:,.0f}\n\n" +
                    "¿Desea eliminarlo de todas formas?\n" +
                    "(Se perderá el registro de la deuda)"
                )
                if not respuesta:
                    return False
        
            # Proceder con eliminación
            cliente = Cliente.buscar_por_id(cliente_id)
            if cliente and cliente.eliminar():
                messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre_completo()}' eliminado correctamente")
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
                return False
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
            return False
    
    def buscar_clientes(self, termino):
        """Buscar clientes por nombre, apellido, teléfono o email"""
        try:
            clientes = self.obtener_todos_clientes()
            termino = termino.lower()
            
            clientes_filtrados = [
                c for c in clientes 
                if (termino in c.nombre.lower() or 
                    termino in c.apellido.lower() or
                    termino in c.telefono.lower() or
                    termino in c.email.lower())
            ]
            
            return clientes_filtrados
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar clientes: {str(e)}")
            return []
    
    def validar_datos_cliente(self, datos):
        """Validar los datos del cliente"""
        errores = []
        
        # Validar nombre
        if not datos.get('nombre', '').strip():
            errores.append("El nombre del cliente es obligatorio")
        
        # Validar apellido
        if not datos.get('apellido', '').strip():
            errores.append("El apellido del cliente es obligatorio")
        
        # Validar teléfono
        telefono = datos.get('telefono', '').strip()
        if telefono and not self.validar_telefono(telefono):
            errores.append("El formato del teléfono no es válido")
        
        # Validar email
        email = datos.get('email', '').strip()
        if email and not self.validar_email(email):
            errores.append("El formato del email no es válido")
        
        return errores
    
    def validar_email(self, email):
        """Validar formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_telefono(self, telefono):
        """Validar formato de teléfono"""
        # Remover espacios y caracteres especiales
        telefono_limpio = re.sub(r'[^\d+]', '', telefono)
        
        # Patrones válidos
        patrones = [
            r'^\+56\d{8,9}$',  # +56XXXXXXXX
            r'^56\d{8,9}$',    # 56XXXXXXXX
            r'^\d{8,9}$'       # XXXXXXXX
        ]
        
        return any(re.match(patron, telefono_limpio) for patron in patrones)
    
    def obtener_estadisticas_clientes(self):
        """Obtener estadísticas generales de clientes"""
        try:
            clientes = self.obtener_todos_clientes()
            
            total_clientes = len(clientes)
            
            # Clientes con compras
            clientes_con_compras = 0
            total_ventas = 0
            
            for cliente in clientes:
                compras = cliente.calcular_total_compras()
                if compras > 0:
                    clientes_con_compras += 1
                    total_ventas += compras
            
            promedio_compra = total_ventas / clientes_con_compras if clientes_con_compras > 0 else 0
            
            return {
                'total_clientes': total_clientes,
                'clientes_con_compras': clientes_con_compras,
                'total_ventas': total_ventas,
                'promedio_compra': promedio_compra
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {str(e)}")
            return {
                'total_clientes': 0,
                'clientes_con_compras': 0,
                'total_ventas': 0,
                'promedio_compra': 0
            }
    
    def obtener_mejores_clientes(self, limite=10):
        """Obtener los mejores clientes por total de compras"""
        try:
            clientes = self.obtener_todos_clientes()
            
            # Calcular total de compras para cada cliente
            clientes_con_total = []
            for cliente in clientes:
                total_compras = cliente.calcular_total_compras()
                if total_compras > 0:
                    clientes_con_total.append((cliente, total_compras))
            
            # Ordenar por total de compras (descendente)
            clientes_con_total.sort(key=lambda x: x[1], reverse=True)
            
            # Retornar solo los primeros 'limite'
            return clientes_con_total[:limite]
            
        except Exception as e:
            print(f"Error al obtener mejores clientes: {str(e)}")
            return []