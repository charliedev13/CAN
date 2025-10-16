"""
Modulo auth_utils – Funzioni di supporto per l'autenticazione utenti.

Gestisce:
- Hash e verifica delle password con bcrypt
- Caricamento e salvataggio degli utenti su file JSON
"""

import json
from passlib.context import CryptContext
from pathlib import Path

# 🔐 Contesto di hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📂 Percorso assoluto del file utenti (all’interno della stessa cartella del modulo)
USERS_FILE = Path(__file__).resolve().parent / "users.json"


# ---------------------------------------------------------
# FUNZIONI DI HASH PASSWORD
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Crea l'hash sicuro della password (tagliando a 72 byte per compatibilità bcrypt).
    """
    # Bcrypt accetta max 72 byte -> tagliamo se necessario
    safe_password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(safe_password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se la password in chiaro combacia con l'hash salvato.
    """
    safe_password = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(safe_password, hashed_password)



# ---------------------------------------------------------
# FUNZIONI DI GESTIONE UTENTI
# ---------------------------------------------------------

def load_users() -> dict:
    """
    Carica gli utenti dal file JSON.
    Se il file non esiste o è vuoto, restituisce un dizionario vuoto.
    """
    try:
        if USERS_FILE.exists() and USERS_FILE.stat().st_size > 0:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}
    except (json.JSONDecodeError, FileNotFoundError):
        # se il file esiste ma non è leggibile o formattato male
        return {}


def save_users(users: dict):
    """
    Salva gli utenti nel file JSON.
    """
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
