from config.database import db
from datetime import datetime, timedelta

class GameProgress:
    """Modelo para el progreso del juego (clicks y rebirths)"""
    
    def __init__(self, id_progreso=None, id_usuario=None, clicks_actuales=0, 
                 clicks_totales=0, cantidad_rebirths=0, costo_siguiente_rebirth=100,
                 multiplicador_activo=1.0, fin_boost=None, boost_tienda_fin=None):
        self.id_progreso = id_progreso
        self.id_usuario = id_usuario
        self.clicks_actuales = clicks_actuales
        self.clicks_totales = clicks_totales
        self.cantidad_rebirths = cantidad_rebirths
        self.costo_siguiente_rebirth = costo_siguiente_rebirth
        self.multiplicador_activo = multiplicador_activo
        
        if isinstance(fin_boost, str) and fin_boost:
            self.fin_boost = datetime.fromisoformat(fin_boost)
        else:
            self.fin_boost = fin_boost
        
        if isinstance(boost_tienda_fin, str) and boost_tienda_fin:
            self.boost_tienda_fin = datetime.fromisoformat(boost_tienda_fin)
        else:
            self.boost_tienda_fin = boost_tienda_fin
    
    def save(self):
        """Guarda o actualiza el progreso en la base de datos"""
        cursor = db.get_cursor()
        if not cursor:
            print("❌ save(): No se pudo obtener cursor")
            return False
        
        try:
            if self.id_progreso:
                query = """
                    UPDATE progreso_juego 
                    SET clicks_actuales = %s, clicks_totales = %s, 
                        cantidad_rebirths = %s, costo_siguiente_rebirth = %s,
                        multiplicador_activo = %s, fin_boost = %s, boost_tienda_fin = %s
                    WHERE id_progreso = %s
                """
                cursor.execute(query, (
                    self.clicks_actuales, self.clicks_totales,
                    self.cantidad_rebirths, self.costo_siguiente_rebirth,
                    self.multiplicador_activo, self.fin_boost, self.boost_tienda_fin,
                    self.id_progreso
                ))
            else:
                query = """
                    INSERT INTO progreso_juego 
                    (id_usuario, clicks_actuales, clicks_totales, cantidad_rebirths, 
                     costo_siguiente_rebirth, multiplicador_activo, fin_boost, boost_tienda_fin)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    self.id_usuario, self.clicks_actuales, self.clicks_totales,
                    self.cantidad_rebirths, self.costo_siguiente_rebirth,
                    self.multiplicador_activo, self.fin_boost, self.boost_tienda_fin
                ))
                self.id_progreso = cursor.lastrowid
            
            db.commit()
            return True
        except Exception as e:
            print(f"❌ save(): Error - {e}")
            db.rollback()
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_user_id(user_id):
        """Obtiene el progreso de un usuario"""
        cursor = db.get_cursor()
        if not cursor:
            return None
        
        try:
            query = "SELECT * FROM progreso_juego WHERE id_usuario = %s"
            cursor.execute(query, (user_id,))
            data = cursor.fetchone()
            
            if data:
                progress = GameProgress(**data)
                progress.check_boosts()
                return progress
            
            progress = GameProgress(id_usuario=user_id)
            progress.save()
            return progress
        except Exception as e:
            print(f"Error getting game progress: {e}")
            return None
        finally:
            cursor.close()
    
    def check_boosts(self):
        """Verifica si los boosts han expirado"""
        now = datetime.now()
        changed = False
        
        if self.fin_boost and now > self.fin_boost:
            self.fin_boost = None
            changed = True
        
        if self.boost_tienda_fin and now > self.boost_tienda_fin:
            self.boost_tienda_fin = None
            changed = True
        
        self._recalc_multiplier()
        
        if changed:
            self.save()
    
    def _recalc_multiplier(self):
        """Recalcula el multiplicador basado en boosts activos"""
        multiplier = 1.0
        now = datetime.now()
        
        if self.fin_boost and now <= self.fin_boost:
            multiplier += 0.25
        
        if self.boost_tienda_fin and now <= self.boost_tienda_fin:
            multiplier += 1.0
        
        self.multiplicador_activo = multiplier
    
    def get_effective_multiplier(self):
        """Obtiene el multiplicador efectivo"""
        self.check_boosts()
        return self.multiplicador_activo
    
    def click(self):
        """Realiza un click"""
        multiplier = self.get_effective_multiplier()
        clicks_ganados = int(1 * multiplier)
        self.clicks_actuales += clicks_ganados
        self.clicks_totales += clicks_ganados
        return clicks_ganados
    
    def can_rebirth(self):
        """Verifica si puede hacer rebirth"""
        return self.clicks_actuales >= self.costo_siguiente_rebirth
    
    def do_rebirth(self):
        """Realiza un rebirth"""
        if not self.can_rebirth():
            return False
        
        self.clicks_actuales -= self.costo_siguiente_rebirth
        self.cantidad_rebirths += 1
        
        now = datetime.now()
        if self.fin_boost and now <= self.fin_boost:
            self.fin_boost = self.fin_boost + timedelta(minutes=5)
        else:
            self.fin_boost = now + timedelta(minutes=5)
        
        self.costo_siguiente_rebirth = int(self.costo_siguiente_rebirth * 1.5)
        self._recalc_multiplier()
        self.save()
        return True
    
    def spend_rebirths(self, amount: int) -> bool:
        """Gasta rebirths para comprar items"""
        if self.cantidad_rebirths >= amount:
            self.cantidad_rebirths -= amount
            self.save()
            return True
        return False
    
    def activate_shop_boost(self, multiplier: float, minutes: int):
        """Activa un boost de tienda (acumulable en tiempo)"""
        now = datetime.now()
        if self.boost_tienda_fin and now <= self.boost_tienda_fin:
            self.boost_tienda_fin = self.boost_tienda_fin + timedelta(minutes=minutes)
        else:
            self.boost_tienda_fin = now + timedelta(minutes=minutes)
        
        self._recalc_multiplier()
        self.save()
    
    def get_boost_time_remaining(self):
        """Obtiene el tiempo restante del boost más largo en segundos"""
        self.check_boosts()
        remaining = 0
        now = datetime.now()
        
        if self.fin_boost and now <= self.fin_boost:
            remaining = max(remaining, int((self.fin_boost - now).total_seconds()))
        
        if self.boost_tienda_fin and now <= self.boost_tienda_fin:
            remaining = max(remaining, int((self.boost_tienda_fin - now).total_seconds()))
        
        return remaining
    
    def get_boost_info(self):
        """Obtiene información detallada de los boosts"""
        self.check_boosts()
        now = datetime.now()
        
        rebirth_remaining = 0
        tienda_remaining = 0
        
        if self.fin_boost and now <= self.fin_boost:
            rebirth_remaining = int((self.fin_boost - now).total_seconds())
        
        if self.boost_tienda_fin and now <= self.boost_tienda_fin:
            tienda_remaining = int((self.boost_tienda_fin - now).total_seconds())
        
        return {
            "rebirth_boost_active": rebirth_remaining > 0,
            "rebirth_boost_time": rebirth_remaining,
            "tienda_boost_active": tienda_remaining > 0,
            "tienda_boost_time": tienda_remaining,
            "total_multiplier": self.multiplicador_activo
        }
    
    def get_stats(self):
        """Obtiene estadísticas formateadas"""
        self.check_boosts()
        boost_info = self.get_boost_info()
        total_remaining = self.get_boost_time_remaining()
        
        return {
            "clicks_actuales": self.clicks_actuales,
            "clicks_totales": self.clicks_totales,
            "cantidad_rebirths": self.cantidad_rebirths,
            "costo_siguiente_rebirth": self.costo_siguiente_rebirth,
            "multiplicador_activo": self.multiplicador_activo,
            "puede_rebirth": self.can_rebirth(),
            "boost_activo": total_remaining > 0,
            "boost_tiempo_restante": total_remaining,
            "boost_info": boost_info
        }