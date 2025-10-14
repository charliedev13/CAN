# Script per importare un file SQL in un database MySQL

import os
import subprocess

# --- CONFIG ---
DB_USER = "root"
DB_PASSWORD = "Hfdfzbhvd.665root"
DB_NAME = "CAN_DB"
CONTAINER_HOST = "127.0.0.1"
DB_PORT = "3306"

# Percorso del file SQL
BASE_DIR = os.path.dirname(__file__)
SQL_FILE = os.path.join(BASE_DIR, "DB", "can_dump.sql")

# Trova comando mysql
MYSQL_PATH = subprocess.getoutput("which mysql")
if not MYSQL_PATH:
    raise FileNotFoundError("❌ Comando 'mysql' non trovato. Installa il client MySQL.")

print(f"✅ mysql trovato in: {MYSQL_PATH}")
print(f"✅ File da importare: {SQL_FILE}")

# Esegui import
cmd = [
    MYSQL_PATH,
    f"-u{DB_USER}",
    f"-p{DB_PASSWORD}",
    f"-h{CONTAINER_HOST}",
    f"-P{DB_PORT}",
    DB_NAME
]

try:
    with open(SQL_FILE, "r") as f:
        subprocess.run(cmd, stdin=f, check=True)
    print(f"✅ Import completato nel database '{DB_NAME}'")
except subprocess.CalledProcessError as e:
    print(f"❌ Errore durante l'import: {e}")
except FileNotFoundError:
    print(f"❌ File SQL non trovato: {SQL_FILE}")