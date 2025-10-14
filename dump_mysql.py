# questo script esegue un dump del database MySQL "CAN_DB" ogni 15 minuti,
# salvando il dump in un file SQL principale e creando copie di backup con timestamp
# nella cartella "backupSQL". 

import os
import subprocess
import time
from datetime import datetime

# --- CONFIG ---
DB_USER = "root"
DB_PASSWORD = "Hfdfzbhvd.665root"
DB_NAME = "CAN_DB"
CONTAINER_HOST = "127.0.0.1"
DB_PORT = "3306"

# Percorsi dinamici
BASE_DIR = os.path.dirname(__file__)
BACKUP_DIR = os.path.join(BASE_DIR, "backupSQL")
MAIN_DUMP_FILE = os.path.join(BASE_DIR, "DB", "can_dump.sql")

# Assicura che la cartella backup esista
os.makedirs(BACKUP_DIR, exist_ok=True)

# Trova il comando mysqldump
MYSQLDUMP_PATH = subprocess.getoutput("which mysqldump")
if not MYSQLDUMP_PATH:
    raise FileNotFoundError("❌ Comando 'mysqldump' non trovato. Installa il MySQL client.")

print(f"✅ mysqldump trovato in: {MYSQLDUMP_PATH}")
print(f"✅ File principale: {MAIN_DUMP_FILE}")
print(f"✅ Cartella backup: {BACKUP_DIR}")

def esegui_dump():
    """Esegue il dump e aggiorna sia il file principale che il backup timestampato."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_{timestamp}.sql")

    cmd = [
        MYSQLDUMP_PATH,
        f"-u{DB_USER}",
        f"-p{DB_PASSWORD}",
        f"-h{CONTAINER_HOST}",
        f"-P{DB_PORT}",
        DB_NAME
    ]

    # Dump principale
    with open(MAIN_DUMP_FILE, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"✅ File principale aggiornato: {MAIN_DUMP_FILE}")

    # Copia di backup
    with open(backup_file, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"💾 Backup salvato: {backup_file}")

if __name__ == "__main__":
    print("🕒 Avvio dump automatico ogni 15 minuti...")
    while True:
        try:
            esegui_dump()
        except Exception as e:
            print(f"❌ Errore durante il dump: {e}")
        time.sleep(15 * 60)