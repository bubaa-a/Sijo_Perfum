"""
Controlador para gestión de cuentas corrientes
"""
from models.cuenta_corriente import CuentaCorriente
from models.cliente import Cliente
from tkinter import messagebox

class CuentaController:
    def __init__(self):
        """Inicializar controlador de cuentas"""
        pass
    
    def registrar_abono(self, cliente_id, monto, metodo_pago, descripcion="", recibo_numero=""):
        """Registrar un abono del cliente"""
        try:
            # Validaciones
            if monto <= 0:
                return False, "El monto debe ser mayor a 0"
            
            # Crear cuenta si no existe
            CuentaCorriente.crear_cuenta_si_no_existe(cliente_id)
            
            # Registrar abono
            cuenta = CuentaCorriente(cliente_id)
            exito, mensaje = cuenta.registrar_abono(monto, metodo_pago, descripcion, recibo_numero)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                return True, mensaje
            else:
                messagebox.showerror("Error", mensaje)
                return False, mensaje
                
        except Exception as e:
            mensaje = f"Error al registrar abono: {str(e)}"
            messagebox.showerror("Error", mensaje)
            return False, mensaje
    
    def obtener_cuenta_cliente(self, cliente_id):
        """Obtener información de cuenta de un cliente"""
        try:
            # Crear cuenta si no existe
            CuentaCorriente.crear_cuenta_si_no_existe(cliente_id)
            
            cuenta = CuentaCorriente(cliente_id)
            return cuenta.obtener_cuenta()
            
        except Exception as e:
            print(f"Error al obtener cuenta: {str(e)}")
            return None
    
    def obtener_historial_cliente(self, cliente_id):
        """Obtener historial completo del cliente"""
        try:
            cuenta = CuentaCorriente(cliente_id)
            
            return {
                'movimientos': cuenta.obtener_historial_movimientos(),
                'abonos': cuenta.obtener_historial_abonos(),
                'cuenta_info': cuenta.obtener_cuenta()
            }
            
        except Exception as e:
            print(f"Error al obtener historial: {str(e)}")
            return None
    
    def obtener_resumen_cuentas(self):
        """Obtener resumen de todas las cuentas"""
        try:
            cuentas = CuentaCorriente.obtener_todas_las_cuentas()
            
            total_clientes_deuda = len(cuentas)
            total_deuda_pendiente = sum(cuenta[4] for cuenta in cuentas)  # saldo_pendiente
            total_deuda_acumulada = sum(cuenta[3] for cuenta in cuentas)  # saldo_total
            
            return {
                'cuentas': cuentas,
                'total_clientes_deuda': total_clientes_deuda,
                'total_deuda_pendiente': total_deuda_pendiente,
                'total_deuda_acumulada': total_deuda_acumulada
            }
            
        except Exception as e:
            print(f"Error al obtener resumen: {str(e)}")
            return {
                'cuentas': [],
                'total_clientes_deuda': 0,
                'total_deuda_pendiente': 0,
                'total_deuda_acumulada': 0
            }
    
    def agregar_venta_a_cuenta(self, cliente_id, monto_venta, descripcion="Venta", venta_id=None):
        """Agregar una venta a la cuenta corriente del cliente"""
        try:
            # Crear cuenta si no existe
            CuentaCorriente.crear_cuenta_si_no_existe(cliente_id)
            
            # Agregar deuda
            cuenta = CuentaCorriente(cliente_id)
            return cuenta.agregar_deuda(monto_venta, descripcion, venta_id)
            
        except Exception as e:
            print(f"Error al agregar venta a cuenta: {str(e)}")
            return False
    
    def obtener_clientes_con_deuda(self):
        """Obtener lista de clientes con deuda pendiente"""
        try:
            return CuentaCorriente.obtener_cuentas_con_saldo()
        except Exception as e:
            print(f"Error al obtener clientes con deuda: {str(e)}")
            return []
    
    def validar_abono(self, cliente_id, monto):
        """Validar si el abono es válido"""
        try:
            cuenta_info = self.obtener_cuenta_cliente(cliente_id)
            if not cuenta_info:
                return False, "Cliente no tiene cuenta corriente"
            
            if monto <= 0:
                return False, "El monto debe ser mayor a 0"
            
            if monto > cuenta_info['saldo_pendiente']:
                return False, f"El abono (${monto:,.0f}) supera la deuda pendiente (${cuenta_info['saldo_pendiente']:,.0f})"
            
            return True, "Abono válido"
            
        except Exception as e:
            return False, f"Error de validación: {str(e)}"