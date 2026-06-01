from datetime import datetime, timedelta
from models.databaseModel import db


class ProgresoController:

    def obtener_progreso(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return self._default_progreso()
        try:
            cursor.execute("SELECT * FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
            if not row:
                cursor.execute("INSERT INTO progreso_juego (id_usuario) VALUES (%s)", (id_usuario,))
                db.commit()
                return self._default_progreso()
            return self._calcular_estado(row)
        except Exception as e:
            print(f"Error obteniendo progreso: {e}")
            return self._default_progreso()
        finally:
            cursor.close()

    def agregar_clicks(self, id_usuario):
        # SELECT en cursor propio, luego UPDATE en cursor nuevo para evitar "Unread result"
        cursor = db.get_cursor()
        if not cursor:
            return
        try:
            cursor.execute("SELECT multiplicador_activo, fin_boost FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            print(f"Error agregando clicks: {e}")
            return
        finally:
            cursor.close()

        if not row:
            return
        ahora = datetime.now()
        fin_boost = row.get("fin_boost")
        boost_activo = fin_boost is not None and fin_boost > ahora
        multiplicador = float(row["multiplicador_activo"]) if boost_activo else 1.0
        incremento = max(1, int(multiplicador))

        cursor2 = db.get_cursor()
        if not cursor2:
            return
        try:
            cursor2.execute(
                """UPDATE progreso_juego 
                   SET clicks_actuales = clicks_actuales + %s,
                       clicks_totales = clicks_totales + %s
                   WHERE id_usuario = %s""",
                (incremento, incremento, id_usuario)
            )
            db.commit()
        except Exception as e:
            print(f"Error agregando clicks: {e}")
            db.rollback()
        finally:
            cursor2.close()

    def realizar_rebirth(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión"
        try:
            cursor.execute("SELECT clicks_actuales, costo_siguiente_rebirth FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            print(f"Error en rebirth: {e}")
            return False, "Error al realizar rebirth"
        finally:
            cursor.close()

        if not row:
            return False, "Progreso no encontrado"
        if row["clicks_actuales"] < row["costo_siguiente_rebirth"]:
            return False, f"Necesitas {row['costo_siguiente_rebirth']:,} clicks"

        nuevo_costo = int(row["costo_siguiente_rebirth"] * 1.5)
        fin_boost = datetime.now() + timedelta(minutes=5)

        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión"
        try:
            cursor2.execute(
                """UPDATE progreso_juego 
                   SET clicks_actuales = 0,
                       cantidad_rebirths = cantidad_rebirths + 1,
                       costo_siguiente_rebirth = %s,
                       multiplicador_activo = multiplicador_activo + 0.25,
                       fin_boost = %s
                   WHERE id_usuario = %s""",
                (nuevo_costo, fin_boost, id_usuario)
            )
            db.commit()
            return True, "¡Rebirth realizado! Boost x1.25 activo por 5 min"
        except Exception as e:
            db.rollback()
            print(f"Error en rebirth: {e}")
            return False, "Error al realizar rebirth"
        finally:
            cursor2.close()

    def comprar_boost_tienda(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión"
        try:
            cursor.execute("SELECT cantidad_rebirths FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            return False, "Error al comprar boost"
        finally:
            cursor.close()

        if not row or row["cantidad_rebirths"] < 3:
            return False, "Necesitas 3 rebirths"

        fin_boost = datetime.now() + timedelta(minutes=5)
        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión"
        try:
            cursor2.execute(
                """UPDATE progreso_juego 
                   SET cantidad_rebirths = cantidad_rebirths - 3,
                       multiplicador_activo = multiplicador_activo + 1,
                       fin_boost = %s
                   WHERE id_usuario = %s""",
                (fin_boost, id_usuario)
            )
            db.commit()
            return True, "¡Boost x2 activo por 5 min!"
        except Exception as e:
            db.rollback()
            return False, "Error al comprar boost"
        finally:
            cursor2.close()

    def comprar_pokemon(self, id_usuario):
        from utils.pokeapi import PokeAPI
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión", None
        try:
            cursor.execute("SELECT cantidad_rebirths FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            print(f"Error comprando pokémon: {e}")
            return False, "Error al comprar pokémon", None
        finally:
            cursor.close()

        if not row or row["cantidad_rebirths"] < 10:
            return False, "Necesitas 10 rebirths", None

        pokemon = PokeAPI.get_random_pokemon()
        if not pokemon:
            return False, "Error obteniendo pokémon de la API", None

        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión", None
        try:
            cursor2.execute(
                "UPDATE progreso_juego SET cantidad_rebirths = cantidad_rebirths - 10 WHERE id_usuario = %s",
                (id_usuario,)
            )
            cursor2.execute(
                """INSERT INTO pokemones_obtenidos (id_usuario, pokemon_api_id, nombre_personalizado)
                   VALUES (%s, %s, %s)""",
                (id_usuario, pokemon["id"], pokemon["name"])
            )
            db.commit()
            return True, f"¡Obtuviste a {pokemon['name']}!", pokemon
        except Exception as e:
            db.rollback()
            print(f"Error comprando pokémon: {e}")
            return False, "Error al comprar pokémon", None
        finally:
            cursor2.close()

    def obtener_inventario(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return []
        try:
            cursor.execute(
                """SELECT po.pokemon_api_id as item_id, po.nombre_personalizado as nombre,
                          COUNT(*) as cantidad, 'pokemon' as tipo
                   FROM pokemones_obtenidos po
                   WHERE po.id_usuario = %s
                   GROUP BY po.pokemon_api_id, po.nombre_personalizado""",
                (id_usuario,)
            )
            rows = cursor.fetchall()
            return [_InventarioItem(r) for r in rows]
        except Exception as e:
            print(f"Error obteniendo inventario: {e}")
            return []
        finally:
            cursor.close()

    def _calcular_estado(self, row):
        ahora = datetime.now()
        fin_boost = row.get("fin_boost")
        boost_activo = fin_boost is not None and fin_boost > ahora
        tiempo_restante = max(0, int((fin_boost - ahora).total_seconds())) if boost_activo else 0
        multiplicador = float(row["multiplicador_activo"]) if boost_activo else 1.0
        rebirths = row["cantidad_rebirths"]
        return {
            "clicks_actuales": row["clicks_actuales"],
            "clicks_totales": row["clicks_totales"],
            "cantidad_rebirths": rebirths,
            "costo_siguiente_rebirth": row["costo_siguiente_rebirth"],
            "multiplicador_activo": multiplicador,
            "boost_activo": boost_activo,
            "boost_tiempo_restante": tiempo_restante,
            "puede_rebirth": row["clicks_actuales"] >= row["costo_siguiente_rebirth"],
            "boost_info": {
                "rebirth_boost_active": boost_activo,
                "rebirth_boost_time": tiempo_restante,
                "tienda_boost_active": False,
                "tienda_boost_time": 0,
                "total_multiplier": multiplicador,
            }
        }

    def _default_progreso(self):
        return {
            "clicks_actuales": 0, "clicks_totales": 0,
            "cantidad_rebirths": 0, "costo_siguiente_rebirth": 100,
            "multiplicador_activo": 1.0, "boost_activo": False,
            "boost_tiempo_restante": 0, "puede_rebirth": False,
            "boost_info": {
                "rebirth_boost_active": False, "rebirth_boost_time": 0,
                "tienda_boost_active": False, "tienda_boost_time": 0,
                "total_multiplier": 1.0,
            }
        }


class _InventarioItem:
    def __init__(self, row):
        self.item_id = row["item_id"]
        self.nombre = row["nombre"]
        self.cantidad = row["cantidad"]
        self.tipo = row["tipo"]
