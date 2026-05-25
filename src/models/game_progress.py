from config.database import db
from datetime import datetime, timedelta

class GameProgress:
    """Modelo para el progreso del juego (clicks y rebirths)"""
    
    def __init__(self, id_progreso=None, id_usuario=None, clicks_actuales=0, 
                 clicks_totales=0, cantidad_rebirths=0, costo_siguiente_rebirth=100,
                 multiplicador_activo=1.0, fin_boost=None):
        self.id_progreso = id_progreso
        self.id_usuario = id_usuario
        self.clicks_actuales = clicks_actuales
        self.clicks_totales = clicks_totales
        self.cantidad_rebirths = cantidad_rebirths
        self.costo_siguiente_rebirth = costo_siguiente_rebirth
        self.multiplicador_activo = multiplicador_activo
        # Convertir fin_boost de string a datetime si es necesario
        if isinstance(fin_boost, str):
            self.fin_boost = datetime.fromisoformat(fin_boost)
        else:
            self.fin_boost = fin_boost
    
    def save(self):
        """Guarda o actualiza el progreso en la base de datos"""
        cursor = db.get_cursor()
        if not cursor:
            return False
        
        try:
            if self.id_progreso:
                query = """
                    UPDATE progreso_juego 
                    SET clicks_actuales = %s, clicks_totales = %s, 
                        cantidad_rebirths = %s, costo_siguiente_rebirth = %s,
                        multiplicador_activo = %s, fin_boost = %s
                    WHERE id_progreso = %s
                """
                cursor.execute(query, (
                    self.clicks_actuales, self.clicks_totales,
                    self.cantidad_rebirths, self.costo_siguiente_rebirth,
                    self.multiplicador_activo, self.fin_boost,
                    self.id_progreso
                ))
            else:
                query = """
                    INSERT INTO progreso_juego 
                    (id_usuario, clicks_actuales, clicks_totales, cantidad_rebirths, 
                     costo_siguiente_rebirth, multiplicador_activo, fin_boost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    self.id_usuario, self.clicks_actuales, self.clicks_totales,
                    self.cantidad_rebirths, self.costo_siguiente_rebirth,
                    self.multiplicador_activo, self.fin_boost
                ))
                self.id_progreso = cursor.lastrowid
            
            db.commit()
            return True
        except Exception as e:
            print(f"Error saving game progress: {e}")
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
                # Verificar si el boost expiró
                progress.check_boost()
                return progress
            
            # Si no existe, crear uno nuevo
            progress = GameProgress(id_usuario=user_id)
            progress.save()
            return progress
        except Exception as e:
            print(f"Error getting game progress: {e}")
            return None
        finally:
            cursor.close()
    
    def check_boost(self):
        """Verifica si el boost ha expirado y lo desactiva"""
        if self.fin_boost and datetime.now() > self.fin_boost:
            self.multiplicador_activo = 1.0
            self.fin_boost = None
            self.save()
    
    def get_effective_multiplier(self):
        """Obtiene el multiplicador efectivo (verificando boost)"""
        self.check_boost()
        return self.multiplicador_activo
    
    def click(self):
        """Realiza un click (suma con multiplicador)"""
        # Verificar boost antes de calcular
        multiplier = self.get_effective_multiplier()
        clicks_ganados = int(1 * multiplier)
        
        self.clicks_actuales += clicks_ganados
        self.clicks_totales += clicks_ganados
        return clicks_ganados
    
    def can_rebirth(self):
        """Verifica si puede hacer rebirth"""
        return self.clicks_actuales >= self.costo_siguiente_rebirth
    
    def do_rebirth(self):
        """
        Realiza un rebirth:
        - Gasta los clicks necesarios
        - Reinicia los clicks actuales a 0
        - Activa boost de x1.25 por 5 minutos
        - Aumenta el costo del siguiente rebirth en 50%
        """
        if not self.can_rebirth():
            return False
        
        # Gastar clicks
        self.clicks_actuales -= self.costo_siguiente_rebirth
        
        # Aumentar rebirths
        self.cantidad_rebirths += 1
        
        # Activar boost temporal de 5 minutos con x1.25
        self.multiplicador_activo = 1.25
        self.fin_boost = datetime.now() + timedelta(minutes=5)
        
        # Aumentar costo del siguiente rebirth (50% más)
        self.costo_siguiente_rebirth = int(self.costo_siguiente_rebirth * 1.5)
        
        self.save()
        return True
    
    def get_boost_time_remaining(self):
        """Obtiene el tiempo restante del boost en segundos"""
        self.check_boost()
        if self.fin_boost and self.multiplicador_activo > 1.0:
            remaining = (self.fin_boost - datetime.now()).total_seconds()
            return max(0, int(remaining))
        return 0
    
    def get_stats(self):
        """Obtiene estadísticas formateadas"""
        self.check_boost()
        boost_remaining = self.get_boost_time_remaining()
        
        return {
            "clicks_actuales": self.clicks_actuales,
            "clicks_totales": self.clicks_totales,
            "cantidad_rebirths": self.cantidad_rebirths,
            "costo_siguiente_rebirth": self.costo_siguiente_rebirth,
            "multiplicador_activo": self.multiplicador_activo,
            "puede_rebirth": self.can_rebirth(),
            "boost_activo": self.multiplicador_activo > 1.0,
            "boost_tiempo_restante": boost_remaining
        }