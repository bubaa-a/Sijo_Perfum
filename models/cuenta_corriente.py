"""
Modelo para gestión de cuentas corrientes
"""
from config.database import DatabaseManager
from datetime import datetime

class CuentaCorriente:
    def __init__(self, cliente_id=None):
        self.id = None
        self.cliente_id = cliente_id
        self.saldo_total = 0.0  # Total de deuda acumulada
        self.saldo_pendiente = 0.0  # Lo que aún debe
        self.fecha_ultima_actualizacion = None
        self.activa = True
        self.db = DatabaseManager()
    
    def crear_cuenta(self):
        """Crear cuenta corriente para un cliente"""
        query = '''
            INSERT INTO cuentas_corrientes (cliente_id, saldo_total, saldo_pendiente)
            VALUES (?, 0, 0)
        '''
        resultado = self.db.ejecutar_consulta(query, (self.cliente_id,))
        return resultado is not None
    
    def agregar_deuda(self, monto, descripcion="Venta", venta_id=None):
        """Agregar deuda por una venta"""
        try:
            # Actualizar cuenta corriente
            query_update = '''
                UPDATE cuentas_corrientes 
                SET saldo_total = saldo_total + ?,
                    saldo_pendiente = saldo_pendiente + ?,
                    fecha_ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE cliente_id = ?
            '''
            self.db.ejecutar_consulta(query_update, (monto, monto, self.cliente_id))
            
            # Registrar movimiento
            query_movimiento = '''
                INSERT INTO movimientos_cuenta 
                (cliente_id, tipo_movimiento, monto, descripcion, venta_id)
                VALUES (?, 'CARGO', ?, ?, ?)
            '''
            self.db.ejecutar_consulta(query_movimiento, 
                                    (self.cliente_id, monto, descripcion, venta_id))
            
            return True
        except Exception as e:
            print(f"Error al agregar deuda: {str(e)}")
            return False
    
    def registrar_abono(self, monto, metodo_pago="Efectivo", descripcion="", recibo_numero=""):
        """Registrar un abono/pago"""
        try:
            # Validar que no se abone más de lo que debe
            cuenta_actual = self.obtener_cuenta()
            if not cuenta_actual:
                return False, "Cuenta no encontrada"
            
            if monto > cuenta_actual['saldo_pendiente']:
                return False, f"El abono (${monto:,.0f}) es mayor al saldo pendiente (${cuenta_actual['saldo_pendiente']:,.0f})"
            
            # Registrar abono
            query_abono = '''
                INSERT INTO abonos 
                (cliente_id, monto_abono, metodo_pago, descripcion, recibo_numero)
                VALUES (?, ?, ?, ?, ?)
            '''
            self.db.ejecutar_consulta(query_abono, 
                                    (self.cliente_id, monto, metodo_pago, descripcion, recibo_numero))
            
            # Actualizar saldo pendiente
            query_update = '''
                UPDATE cuentas_corrientes 
                SET saldo_pendiente = saldo_pendiente - ?,
                    fecha_ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE cliente_id = ?
            '''
            self.db.ejecutar_consulta(query_update, (monto, self.cliente_id))
            
            # Registrar movimiento
            query_movimiento = '''
                INSERT INTO movimientos_cuenta 
                (cliente_id, tipo_movimiento, monto, descripcion)
                VALUES (?, 'ABONO', ?, ?)
            '''
            descripcion_mov = f"Abono {metodo_pago}" + (f" - {descripcion}" if descripcion else "")
            self.db.ejecutar_consulta(query_movimiento, 
                                    (self.cliente_id, monto, descripcion_mov))
            
            return True, "Abono registrado correctamente"
            
        except Exception as e:
            print(f"Error al registrar abono: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def obtener_cuenta(self):
        """Obtener información de la cuenta corriente"""
        query = '''
            SELECT cc.*, c.nombre, c.apellido
            FROM cuentas_corrientes cc
            JOIN clientes c ON cc.cliente_id = c.id
            WHERE cc.cliente_id = ? AND cc.activa = 1
        '''
        resultado = self.db.ejecutar_consulta(query, (self.cliente_id,))
        
        if resultado and len(resultado) > 0:
            fila = resultado[0]
            return {
                'id': fila[0],
                'cliente_id': fila[1],
                'saldo_total': fila[2],
                'saldo_pendiente': fila[3],
                'fecha_ultima_actualizacion': fila[4],
                'activa': fila[5],
                'nombre_cliente': f"{fila[6]} {fila[7]}"
            }
        return None
    
    def obtener_historial_movimientos(self, limite=50):
        """Obtener historial de movimientos"""
        query = '''
            SELECT tipo_movimiento, monto, descripcion, fecha_movimiento, venta_id
            FROM movimientos_cuenta
            WHERE cliente_id = ?
            ORDER BY fecha_movimiento DESC
            LIMIT ?
        '''
        resultados = self.db.ejecutar_consulta(query, (self.cliente_id, limite))
        return resultados or []
    
    def obtener_historial_abonos(self, limite=20):
        """Obtener historial de abonos"""
        query = '''
            SELECT monto_abono, metodo_pago, descripcion, recibo_numero, fecha_abono
            FROM abonos
            WHERE cliente_id = ?
            ORDER BY fecha_abono DESC
            LIMIT ?
        '''
        resultados = self.db.ejecutar_consulta(query, (self.cliente_id, limite))
        return resultados or []
    
    @staticmethod
    def obtener_todas_las_cuentas():
        """Obtener todas las cuentas corrientes activas"""
        db = DatabaseManager()
        query = '''
            SELECT cc.cliente_id, c.nombre, c.apellido, cc.saldo_total, 
                   cc.saldo_pendiente, cc.fecha_ultima_actualizacion
            FROM cuentas_corrientes cc
            JOIN clientes c ON cc.cliente_id = c.id
            WHERE cc.activa = 1 AND cc.saldo_pendiente > 0
            ORDER BY cc.saldo_pendiente DESC
        '''
        resultados = db.ejecutar_consulta(query)
        return resultados or []
    
    @staticmethod
    def obtener_cuentas_con_saldo():
        """Obtener solo cuentas con saldo pendiente"""
        db = DatabaseManager()
        query = '''
            SELECT cc.cliente_id, c.nombre, c.apellido, cc.saldo_pendiente
            FROM cuentas_corrientes cc
            JOIN clientes c ON cc.cliente_id = c.id
            WHERE cc.activa = 1 AND cc.saldo_pendiente > 0
            ORDER BY cc.saldo_pendiente DESC
        '''
        resultados = db.ejecutar_consulta(query)
        return resultados or []
    
    @staticmethod
    def crear_cuenta_si_no_existe(cliente_id):
        """Crear cuenta si no existe para el cliente"""
        db = DatabaseManager()
        
        # Verificar si ya existe
        query_check = "SELECT id FROM cuentas_corrientes WHERE cliente_id = ?"
        resultado = db.ejecutar_consulta(query_check, (cliente_id,))
        
        if not resultado:
            # Crear nueva cuenta
            query_create = '''
                INSERT INTO cuentas_corrientes (cliente_id, saldo_total, saldo_pendiente)
                VALUES (?, 0, 0)
            '''
            db.ejecutar_consulta(query_create, (cliente_id,))
            return True
        return False

    def revertir_cargo_venta(self, monto_venta, venta_id):
        """Revertir el cargo de una venta eliminada"""
        try:
            # Revertir saldos en cuenta corriente
            query_update = '''
                UPDATE cuentas_corrientes
                SET saldo_total = saldo_total - ?,
                    saldo_pendiente = saldo_pendiente - ?,
                    fecha_ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE cliente_id = ?
            '''
            self.db.ejecutar_consulta(query_update, (monto_venta, monto_venta, self.cliente_id))

            # Eliminar movimiento asociado a la venta
            query_delete_mov = '''
                DELETE FROM movimientos_cuenta
                WHERE cliente_id = ? AND venta_id = ?
            '''
            self.db.ejecutar_consulta(query_delete_mov, (self.cliente_id, venta_id))

            return True

        except Exception as e:
            print(f"Error al revertir cargo de venta: {str(e)}")
            return False

    def eliminar_cuenta_vacia(self):
        """Eliminar cuenta corriente si tiene saldo cero"""
        try:
            # Verificar que realmente tenga saldo cero
            cuenta_info = self.obtener_cuenta()
            if cuenta_info and cuenta_info['saldo_pendiente'] == 0 and cuenta_info['saldo_total'] == 0:

                # Eliminar movimientos históricos
                query_movimientos = "DELETE FROM movimientos_cuenta WHERE cliente_id = ?"
                self.db.ejecutar_consulta(query_movimientos, (self.cliente_id,))

                # Eliminar abonos históricos
                query_abonos = "DELETE FROM abonos WHERE cliente_id = ?"
                self.db.ejecutar_consulta(query_abonos, (self.cliente_id,))

                # Eliminar cuenta corriente
                query_cuenta = "DELETE FROM cuentas_corrientes WHERE cliente_id = ?"
                self.db.ejecutar_consulta(query_cuenta, (self.cliente_id,))

                print(f"DEBUG: Cuenta corriente del cliente {self.cliente_id} eliminada completamente")
                return True

            return False

        except Exception as e:
            print(f"Error al eliminar cuenta vacía: {str(e)}")
            return False