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
        cursor = db.get_cursor()
        if not cursor:
            return
        try:
            cursor.execute("SELECT multiplicador_activo, fin_boost, fin_boost_tienda FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            print(f"Error agregando clicks: {e}")
            return
        finally:
            cursor.close()

        if not row:
            return
        ahora = datetime.now()
        rebirth_activo = row.get("fin_boost") is not None and row["fin_boost"] > ahora
        tienda_activo = row.get("fin_boost_tienda") is not None and row["fin_boost_tienda"] > ahora
        multiplicador = float(row["multiplicador_activo"]) if rebirth_activo else 1.0
        if tienda_activo:
            multiplicador += 1.0
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
            progreso = cursor.fetchone()
            cursor.execute("SELECT costo_rebirths, nombre_producto FROM tienda WHERE categoria = 'boost' LIMIT 1")
            producto = cursor.fetchone()
        except Exception as e:
            return False, "Error al comprar boost"
        finally:
            cursor.close()

        if not producto:
            return False, "Producto no disponible"
        if not progreso or progreso["cantidad_rebirths"] < producto["costo_rebirths"]:
            return False, f"Necesitas {producto['costo_rebirths']} rebirths"

        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión"
        try:
            cursor2.execute(
                """UPDATE progreso_juego
                   SET cantidad_rebirths = cantidad_rebirths - %s,
                       boost_tienda_pendiente = boost_tienda_pendiente + 1
                   WHERE id_usuario = %s""",
                (producto["costo_rebirths"], id_usuario)
            )
            db.commit()
            return True, f"¡{producto['nombre_producto']} comprado! Úsalo desde el inventario."
        except Exception as e:
            db.rollback()
            return False, "Error al comprar boost"
        finally:
            cursor2.close()

    def usar_boost_tienda(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión"
        try:
            cursor.execute("SELECT boost_tienda_pendiente FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
        except Exception as e:
            return False, "Error al usar boost"
        finally:
            cursor.close()

        if not row or row["boost_tienda_pendiente"] < 1:
            return False, "No tienes boosts disponibles"

        fin_boost_tienda = datetime.now() + timedelta(minutes=5)
        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión"
        try:
            cursor2.execute(
                """UPDATE progreso_juego
                   SET boost_tienda_pendiente = boost_tienda_pendiente - 1,
                       fin_boost_tienda = %s
                   WHERE id_usuario = %s""",
                (fin_boost_tienda, id_usuario)
            )
            db.commit()
            return True, "¡Boost x2 activo por 5 min!"
        except Exception as e:
            db.rollback()
            return False, "Error al usar boost"
        finally:
            cursor2.close()

    def comprar_pokemon(self, id_usuario):
        from utils.pokeapi import PokeAPI
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión", None
        try:
            cursor.execute("SELECT cantidad_rebirths FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            progreso = cursor.fetchone()
            cursor.execute("SELECT costo_rebirths FROM tienda WHERE categoria = 'pokemon' LIMIT 1")
            producto = cursor.fetchone()
        except Exception as e:
            print(f"Error comprando pokémon: {e}")
            return False, "Error al comprar pokémon", None
        finally:
            cursor.close()

        if not producto:
            return False, "Producto no disponible", None
        if not progreso or progreso["cantidad_rebirths"] < producto["costo_rebirths"]:
            return False, f"Necesitas {producto['costo_rebirths']} rebirths", None

        pokemon = PokeAPI.get_random_pokemon()
        if not pokemon:
            return False, "Error obteniendo pokémon de la API", None

        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión", None
        try:
            cursor2.execute(
                "UPDATE progreso_juego SET cantidad_rebirths = cantidad_rebirths - %s WHERE id_usuario = %s",
                (producto["costo_rebirths"], id_usuario)
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

    def obtener_productos_tienda(self):
        cursor = db.get_cursor()
        if not cursor:
            return []
        try:
            cursor.execute("SELECT * FROM tienda ORDER BY id_producto")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo tienda: {e}")
            return []
        finally:
            cursor.close()

    def obtener_inventario(self, id_usuario):
        cursor = db.get_cursor()
        if not cursor:
            return []
        try:
            cursor.execute(
                """SELECT po.pokemon_api_id as item_id, po.nombre_personalizado as nombre,
                          COUNT(*) as cantidad, 'pokemon' as tipo,
                          MAX(po.nivel) as nivel, MAX(po.esta_equipado) as esta_equipado
                   FROM pokemones_obtenidos po
                   WHERE po.id_usuario = %s
                   GROUP BY po.pokemon_api_id, po.nombre_personalizado""",
                (id_usuario,)
            )
            items = [_InventarioItem(r) for r in cursor.fetchall()]

            cursor.execute("SELECT fin_boost_tienda, boost_tienda_pendiente FROM progreso_juego WHERE id_usuario = %s", (id_usuario,))
            prog = cursor.fetchone()
            if prog:
                # Boost activo (corriendo)
                if prog["fin_boost_tienda"] and prog["fin_boost_tienda"] > datetime.now():
                    secs = int((prog["fin_boost_tienda"] - datetime.now()).total_seconds())
                    items.append(_InventarioItem({
                        "item_id": -1, "nombre": f"Boost x2 activo ({secs // 60}m {secs % 60}s)",
                        "cantidad": 1, "tipo": "boost_activo"
                    }))
                # Boosts pendientes (sin usar)
                pendientes = prog.get("boost_tienda_pendiente") or 0
                if pendientes > 0:
                    items.append(_InventarioItem({
                        "item_id": 0, "nombre": "Boost x2 (5 min)",
                        "cantidad": pendientes, "tipo": "boost"
                    }))
            return items
        except Exception as e:
            print(f"Error obteniendo inventario: {e}")
            return []
        finally:
            cursor.close()

    def _calcular_estado(self, row):
        ahora = datetime.now()

        fin_boost = row.get("fin_boost")
        rebirth_activo = fin_boost is not None and fin_boost > ahora
        rebirth_tiempo = max(0, int((fin_boost - ahora).total_seconds())) if rebirth_activo else 0

        fin_boost_tienda = row.get("fin_boost_tienda")
        tienda_activo = fin_boost_tienda is not None and fin_boost_tienda > ahora
        tienda_tiempo = max(0, int((fin_boost_tienda - ahora).total_seconds())) if tienda_activo else 0

        multiplicador = float(row["multiplicador_activo"]) if rebirth_activo else 1.0
        if tienda_activo:
            multiplicador += 1.0

        boost_activo = rebirth_activo or tienda_activo
        return {
            "clicks_actuales": row["clicks_actuales"],
            "clicks_totales": row["clicks_totales"],
            "cantidad_rebirths": row["cantidad_rebirths"],
            "costo_siguiente_rebirth": row["costo_siguiente_rebirth"],
            "multiplicador_activo": multiplicador,
            "boost_activo": boost_activo,
            "boost_tiempo_restante": max(rebirth_tiempo, tienda_tiempo),
            "puede_rebirth": row["clicks_actuales"] >= row["costo_siguiente_rebirth"],
            "boost_info": {
                "rebirth_boost_active": rebirth_activo,
                "rebirth_boost_time": rebirth_tiempo,
                "tienda_boost_active": tienda_activo,
                "tienda_boost_time": tienda_tiempo,
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
        self.nivel = row.get("nivel", 1)
        self.esta_equipado = bool(row.get("esta_equipado", False))
