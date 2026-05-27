from models.game_progress import GameProgress
from models.inventory import Inventory
from utils.pokeapi import PokeAPI
from config.database import db

class ShopController:
    """Controlador para las compras en la tienda"""
    
    COSTO_POKEMON = 10
    COSTO_BOOST = 3
    BOOST_MULTIPLIER = 2.0
    BOOST_MINUTES = 5
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.progress = GameProgress.get_by_user_id(user_id)
        print(f"🛒 ShopController inicializado para user_id={user_id}")
        print(f"   Progreso cargado: rebirths={self.progress.cantidad_rebirths if self.progress else 'None'}")
    
    def buy_random_pokemon(self):
        """Compra un pokémon aleatorio"""
        print(f"📱 Intentando comprar Pokémon...")
        print(f"   Rebirths actuales: {self.progress.cantidad_rebirths if self.progress else 'None'}")
        print(f"   Costo: {self.COSTO_POKEMON}")
        
        if not self.progress:
            print("❌ No hay progreso cargado")
            return False, "Error: No se pudo cargar el progreso del juego.", None
        
        if self.progress.cantidad_rebirths < self.COSTO_POKEMON:
            print(f"❌ Rebirths insuficientes: {self.progress.cantidad_rebirths} < {self.COSTO_POKEMON}")
            return False, f"Necesitas {self.COSTO_POKEMON} rebirths. Tienes: {self.progress.cantidad_rebirths}", None
        
        # Obtener pokémon aleatorio
        print("🌐 Llamando a PokéAPI...")
        pokemon = PokeAPI.get_random_pokemon()
        if not pokemon:
            print("❌ Error al obtener pokémon de la API")
            return False, "Error al obtener pokémon. Intenta de nuevo.", None
        
        print(f"✅ Pokémon obtenido: {pokemon['name']} (ID: {pokemon['id']})")
        
        # Gastar rebirths
        print(f"💎 Gastando {self.COSTO_POKEMON} rebirths...")
        if not self.progress.spend_rebirths(self.COSTO_POKEMON):
            print("❌ Error al gastar rebirths")
            return False, "Error al gastar rebirths.", None
        
        print(f"✅ Rebirths gastados. Ahora tienes: {self.progress.cantidad_rebirths}")
        
        # Guardar en inventario
        print("💾 Guardando en inventario...")
        item = Inventory(
            id_usuario=self.user_id,
            tipo='pokemon',
            item_id=pokemon['id'],
            nombre=pokemon['name'],
            cantidad=1
        )
        if item.save():
            print(f"✅ Pokémon guardado en inventario")
        else:
            print("❌ Error al guardar en inventario")
            return False, "Error al guardar en inventario.", None
        
        return True, f"¡{pokemon['name']} guardado!", pokemon
    
    def buy_boost(self):
        """Compra un boost x2"""
        print(f"📱 Intentando comprar Boost...")
        print(f"   Rebirths actuales: {self.progress.cantidad_rebirths if self.progress else 'None'}")
        print(f"   Costo: {self.COSTO_BOOST}")
        
        if not self.progress:
            print("❌ No hay progreso cargado")
            return False, "Error: No se pudo cargar el progreso del juego."
        
        if self.progress.cantidad_rebirths < self.COSTO_BOOST:
            print(f"❌ Rebirths insuficientes: {self.progress.cantidad_rebirths} < {self.COSTO_BOOST}")
            return False, f"Necesitas {self.COSTO_BOOST} rebirths. Tienes: {self.progress.cantidad_rebirths}"
        
        # Gastar rebirths
        print(f"💎 Gastando {self.COSTO_BOOST} rebirths...")
        if not self.progress.spend_rebirths(self.COSTO_BOOST):
            print("❌ Error al gastar rebirths")
            return False, "Error al gastar rebirths."
        
        print(f"✅ Rebirths gastados. Ahora tienes: {self.progress.cantidad_rebirths}")
        
        # Guardar en inventario
        print("💾 Guardando boost en inventario...")
        item = Inventory(
            id_usuario=self.user_id,
            tipo='boost',
            item_id='boost_x2',
            nombre='Boost x2 (5 min)',
            cantidad=1
        )
        if item.save():
            print(f"✅ Boost guardado en inventario")
        else:
            print("❌ Error al guardar en inventario")
            return False, "Error al guardar en inventario."
        
        return True, "Boost guardado en inventario"
    
    def use_boost(self):
        """Usa un boost del inventario"""
        print(f"⚡ Intentando usar boost del inventario...")
        
        boosts = Inventory.get_boosts_count(self.user_id)
        print(f"   Boosts en inventario: {boosts}")
        
        if boosts == 0:
            print("❌ No hay boosts en inventario")
            return False, "No tienes boosts en tu inventario."
        
        # Activar boost
        print("🚀 Activando boost de tienda...")
        self.progress.activate_shop_boost(self.BOOST_MULTIPLIER, self.BOOST_MINUTES)
        
        # Quitar del inventario
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
                print(f"✅ Boost consumido del inventario")
            except Exception as e:
                print(f"❌ Error usando boost: {e}")
                db.rollback()
            finally:
                cursor.close()
        
        boost_info = self.progress.get_boost_info()
        total_min = (boost_info["tienda_boost_time"] // 60) + 1
        
        return True, f"¡Boost x2 activado! Tiempo total: {total_min} minutos"
    
    @staticmethod
    def get_inventory(user_id):
        """Obtiene el inventario del usuario"""
        inventory = Inventory.get_by_user_id(user_id)
        print(f"📦 Inventario obtenido: {len(inventory)} items")
        return inventory
    
    @staticmethod
    def get_pokemon_count(user_id):
        return Inventory.get_pokemon_count(user_id)
    
    @staticmethod
    def get_boosts_count(user_id):
        return Inventory.get_boosts_count(user_id)