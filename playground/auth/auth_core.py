# gestione autenticazione (JWT, login, reset password)
import jwt
import json
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from auth_utils import hash_password, verify_password, load_users, save_users
from pathlib import Path

# Carico configurazione

config_path = Path(__file__).resolve().parent / "auth_config.json"
with open(config_path) as f:
    config = json.load(f)


SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
RESET_CODE_EXPIRE_MINUTES = config["RESET_CODE_EXPIRE_MINUTES"]

# Configurazione email
mail_conf = ConnectionConfig(
    MAIL_USERNAME=config["MAIL_USERNAME"],
    MAIL_PASSWORD=config["MAIL_PASSWORD"],
    MAIL_FROM=config["MAIL_FROM"],
    MAIL_PORT=config["MAIL_PORT"],
    MAIL_SERVER=config["MAIL_SERVER"],
    MAIL_STARTTLS=config["MAIL_STARTTLS"],
    MAIL_SSL_TLS=config["MAIL_SSL_TLS"],
    USE_CREDENTIALS=config.get("USE_CREDENTIALS", True)
)

# --- JWT ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Genera un token di accesso standard"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(username: str):
    """Genera un token JWT temporaneo per il reset password"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_CODE_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire, "type": "reset"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_reset_token(token: str):
    """Decodifica e valida il token JWT di reset"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# --- REGISTER / LOGIN ---
def register_user(username: str, password: str, email: str):
    print("DEBUG register_user:", username, email)
    users = load_users()
    if username in users:
        return {"error": "Utente già registrato"}
    users[username] = {
        "password": hash_password(password),
        "email": email
    }
    save_users(users)
    return {"msg": "Registrazione completata"}

def login_user(username: str, password: str):
    users = load_users()
    if username not in users or not verify_password(password, users[username]["password"]):
        return {"error": "Credenziali non valide"}
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- RESET PASSWORD VIA EMAIL ---
async def request_password_reset(username: str):
    """Invia via email il link con token JWT per resettare la password"""
    users = load_users()
    if username not in users:
        return {"error": "Utente non trovato"}

    token = create_reset_token(username)
    reset_link = f"http://localhost:8000/reset-page?token={token}"

    message = MessageSchema(
        subject="Reset Password",
        recipients=[users[username]["email"]],
        body=f"""
        Ciao {username},

        Per reimpostare la password clicca sul seguente link:
        {reset_link}

        Il link scade tra {RESET_CODE_EXPIRE_MINUTES} minuti.
        """,
        subtype="plain"
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)

    return {"msg": "Email di reset inviata"}

def reset_password(token: str, new_password: str):
    """Reimposta la password se il token JWT è valido"""
    username = decode_reset_token(token)
    if not username:
        return {"error": "Token non valido o scaduto"}

    users = load_users()
    if username not in users:
        return {"error": "Utente non trovato"}

    users[username]["password"] = hash_password(new_password)
    save_users(users)
    return {"msg": "Password aggiornata con successo"}
