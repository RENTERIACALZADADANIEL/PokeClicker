import mysql.connector

class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="3306",
            user="root",
            password="",
            database="poke_clicker"
        )