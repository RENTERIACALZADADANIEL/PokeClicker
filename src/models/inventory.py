from config.database import db
from datetime import datetime

class Inventory:
    """Modelo para el inventario de items/pokémon del usuario"""
    
    def __init__(self, id_item_inv=None, id_usuario=None, tipo=None, 
                 item_id=None, nombre=None, cantidad=1, fecha_obtencion=None):
        self.id_item_inv = id_item_inv
        self.id_usuario = id_usuario
        self.tipo = tipo              # 'pokemon' o 'boost'
        self.item_id = item_id        # ID del pokémon (API) o 'boost_x2'
        self.nombre = nombre          # Nombre del item
        self.cantidad = cantidad
        self.fecha_obtencion = fecha_obtencion or datetime.now()
    
    def save(self):
        """Guarda un item en el inventario"""
        cursor = db.get_cursor()
        if not cursor:
            return False
        
        try:
            # Verificar si ya existe el item
            query_check = """
                SELECT id_item_inv, cantidad FROM inventario 
                WHERE id_usuario = %s AND tipo = %s AND item_id = %s
            """
            cursor.execute(query_check, (self.id_usuario, self.tipo, str(self.item_id)))
            existing = cursor.fetchone()
            
            if existing:
                # Actualizar cantidad
                query = """
                    UPDATE inventario SET cantidad = cantidad + %s 
                    WHERE id_item_inv = %s
                """
                cursor.execute(query, (self.cantidad, existing['id_item_inv']))
            else:
                # Insertar nuevo
                query = """
                    INSERT INTO inventario (id_usuario, tipo, item_id, nombre, cantidad)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    self.id_usuario, self.tipo, str(self.item_id), 
                    self.nombre, self.cantidad
                ))
                self.id_item_inv = cursor.lastrowid
            
            db.commit()
            return True
        except Exception as e:
            print(f"Error saving inventory: {e}")
            db.rollback()
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_user_id(user_id):
        """Obtiene todos los items del inventario de un usuario"""
        cursor = db.get_cursor()
        if not cursor:
            return []
        
        try:
            query = """
                SELECT * FROM inventario 
                WHERE id_usuario = %s AND cantidad > 0
                ORDER BY fecha_obtencion DESC
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return [Inventory(**item) for item in results]
        except Exception as e:
            print(f"Error getting inventory: {e}")
            return []
        finally:
            cursor.close()
    
    @staticmethod
    def count_by_type(user_id, tipo):
        """Cuenta cuántos items de un tipo tiene el usuario"""
        cursor = db.get_cursor()
        if not cursor:
            return 0
        
        try:
            query = """
                SELECT SUM(cantidad) as total FROM inventario 
                WHERE id_usuario = %s AND tipo = %s
            """
            cursor.execute(query, (user_id, tipo))
            result = cursor.fetchone()
            return result['total'] if result and result['total'] else 0
        except Exception as e:
            print(f"Error counting inventory: {e}")
            return 0
        finally:
            cursor.close()
    
    @staticmethod
    def get_boosts_count(user_id):
        """Obtiene la cantidad de boosts en el inventario"""
        return Inventory.count_by_type(user_id, 'boost')
    
    @staticmethod
    def get_pokemon_count(user_id):
        """Obtiene la cantidad de pokémon en el inventario"""
        return Inventory.count_by_type(user_id, 'pokemon')