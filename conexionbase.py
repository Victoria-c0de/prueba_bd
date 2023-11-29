import mysql.connector

class BaseDatos():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="parkdb"
        )
        self.cursor = self.conn.cursor()