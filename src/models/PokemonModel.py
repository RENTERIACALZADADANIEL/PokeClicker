from utils.pokeapi import PokeAPI


class PokemonModel:
    def get_random(self):
        return PokeAPI.get_random_pokemon()
