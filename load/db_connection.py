import mysql.connector

def get_connection():
    try: 
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db_oleos"
        )

        if mydb.is_connected():
            cursor = mydb.cursor()
            cursor.execute("SELECT DATABASE();")
            linha = cursor.fetchone()
            print("Conectado ao banco de dados:", linha[0])
            return mydb 
        
    except mysql.connector.Error as erro:
        print("Error to connect with DB", erro)
        return None

