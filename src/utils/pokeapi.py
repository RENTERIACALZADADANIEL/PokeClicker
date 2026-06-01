import requests
import random

class PokeAPI:
    
    BASE_URL = "https://pokeapi.co/api/v2"
    TOTAL_POKEMON = 898  # Número total de pokémon en la API
    
    @staticmethod
    def get_random_pokemon():
    
        try:
            # Elegir ID aleatorio
            pokemon_id = random.randint(1, PokeAPI.TOTAL_POKEMON)
            
            
            response = requests.get(
                f"{PokeAPI.BASE_URL}/pokemon/{pokemon_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": data["id"],
                    "name": data["name"].capitalize(),
                    "sprite": data["sprites"]["front_default"] or data["sprites"]["other"]["official-artwork"]["front_default"],
                    "types": [t["type"]["name"] for t in data["types"]]
                }
            return None
        except Exception as e:
            print(f"Error obteniendo pokémon: {e}")
            return None