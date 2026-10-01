import mysql.connector
import os
import time
from dotenv import load_dotenv

load_dotenv()

def get_connection(retries=5, delay=10):
    for attempt in range(1, retries + 1):
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
            print(f"Tentativa {attempt}/{retries} falhou: {erro}")
            if attempt < retries:
                print(f"Aguardando {delay}s para o banco acordar...")
                time.sleep(delay)
    print("Não foi possível conectar ao banco após todas as tentativas.")
    return None

