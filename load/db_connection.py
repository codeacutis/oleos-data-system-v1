import mysql.connector
import os

def get_connection():
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "root"),
            database=os.environ.get("DB_NAME", "db_oleos")
        )
        return mydb
    except mysql.connector.Error as erro:
        print("Erro ao conectar com o banco:", erro)
        return None

