import subprocess
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

db_informations = {
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "PORT": str(os.environ.get("DB_PORT", 3306)),
    "USER": os.environ.get("DB_USER", "root"),
    "PASSWORD": os.environ.get("DB_PASSWORD", "root"),
    "DATABASE": os.environ.get("DB_NAME", "db_oleos")
}

resultado = subprocess.run([r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
                            "-h", db_informations["HOST"],
                            "-P", db_informations["PORT"],
                            "-u", db_informations["USER"],
                            "-p" + db_informations["PASSWORD"],
                            db_informations["DATABASE"]
                            ], capture_output=True)

today = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

with open(f"backups/db_oleos_{today}.sql", "wb") as f:
    f.write(resultado.stdout)
    print(f"Backup realizado com sucesso! Arquivo salvo: db_oleos_{today}.sql")


