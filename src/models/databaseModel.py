import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        try:
            if self.connection is not None:
                try:
                    self.connection.ping(reconnect=True, attempts=3, delay=1)
                except Exception:
                    self.connection = None
            if self.connection is None:
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', '127.0.0.1'),
                    port=int(os.getenv('DB_PORT', 3306)),
                    database=os.getenv('DB_NAME', 'poke_clicker'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASSWORD', '')
                )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
            return None

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None

    def get_cursor(self, dictionary=True):
        connection = self.connect()
        if connection:
            try:
                return connection.cursor(dictionary=dictionary)
            except Exception:
                self.connection = None
                connection = self.connect()
                if connection:
                    return connection.cursor(dictionary=dictionary)
        return None
    
    def commit(self):
        
        if self.connection and self.connection.is_connected():
            self.connection.commit()
    
    def rollback(self):
        
        if self.connection and self.connection.is_connected():
            self.connection.rollback()

db = Database()  