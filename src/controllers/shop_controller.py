from models.game_progress import GameProgress
from models.inventory import Inventory
from utils.pokeapi import PokeAPI

class ShopController:
    """Controlador para las compras en la tienda"""
    
    COSTO_POKEMON = 10      # Rebirths necesarios para comprar pokémon
    COSTO_BOOST = 3         # Rebirths necesarios para comprar boost
    BOOST_MULTIPLIER = 2.0  # x2
    BOOST_MINUTES = 5       # 5 minutos
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.progress = GameProgress.get_by_user_id(user_id)
    
    def buy_random_pokemon(self):
        """
        Compra un pokémon aleatorio
        
        Returns:
            tuple[bool, str, dict]: (éxito, mensaje, datos_pokemon)
        """
        # Verificar rebirths suficientes
        if not self.progress or self.progress.cantidad_rebirths < self.COSTO_POKEMON:
            return False, f"Necesitas {self.COSTO_POKEMON} rebirths. Tienes: {self.progress.cantidad_rebirths if self.progress else 0}", None
        
        # Obtener pokémon aleatorio
        pokemon = PokeAPI.get_random_pokemon()
        if not pokemon:
            return False, "Error al obtener pokémon. Intenta de nuevo.", None
        
        # Gastar rebirths
        if not self.progress.spend_rebirths(self.COSTO_POKEMON):
            return False, "Error al gastar rebirths.", None
        
        # Guardar en inventario
        item = Inventory(
            id_usuario=self.user_id,
            tipo='pokemon',
            item_id=pokemon['id'],
            nombre=pokemon['name'],
            cantidad=1
        )
        item.save()
        
        return True, f"¡Has obtenido a {pokemon['name']}!", pokemon
    
    def buy_boost(self):
        """
        Compra un boost x2 de 5 minutos
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        # Verificar rebirths suficientes
        if not self.progress or self.progress.cantidad_rebirths < self.COSTO_BOOST:
            return False, f"Necesitas {self.COSTO_BOOST} rebirths. Tienes: {self.progress.cantidad_rebirths if self.progress else 0}"
        
        # Gastar rebirths
        if not self.progress.spend_rebirths(self.COSTO_BOOST):
            return False, "Error al gastar rebirths."
        
        # Guardar en inventario
        item = Inventory(
            id_usuario=self.user_id,
            tipo='boost',
            item_id='boost_x2',
            nombre='Boost x2 (5 min)',
            cantidad=1
        )
        item.save()
        
        return True, "¡Boost x2 guardado en tu inventario!"
    
    def use_boost(self):
        """
        Usa un boost del inventario
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        # Verificar si hay boosts en inventario
        boosts = Inventory.get_boosts_count(self.user_id)
        if boosts == 0:
            return False, "No tienes boosts en tu inventario."
        
        # Activar boost
        self.progress.activate_boost(self.BOOST_MULTIPLIER, self.BOOST_MINUTES)
        
        # Quitar del inventario (reducir cantidad)
        cursor = db.get_cursor()
        if cursor:
            try:
                query = """
                    UPDATE inventario SET cantidad = cantidad - 1 
                    WHERE id_usuario = %s AND tipo = 'boost' AND cantidad > 0
                    LIMIT 1
                """
                cursor.execute(query, (self.user_id,))
                db.commit()
            except Exception as e:
                print(f"Error usando boost: {e}")
                db.rollback()
            finally:
                cursor.close()
        
        return True, f"¡Boost x{self.BOOST_MULTIPLIER} activado por {self.BOOST_MINUTES} minutos!"
    
    @staticmethod
    def get_inventory(user_id):
        """Obtiene el inventario del usuario"""
        return Inventory.get_by_user_id(user_id)
    
    @staticmethod
    def get_pokemon_count(user_id):
        """Obtiene cantidad de pokémon en inventario"""
        return Inventory.get_pokemon_count(user_id)
    
    @staticmethod
    def get_boosts_count(user_id):
        """Obtiene cantidad de boosts en inventario"""
        return Inventory.get_boosts_count(user_id)