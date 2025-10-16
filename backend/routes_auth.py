"""
Modulo routes_auth.py – Gestione API di autenticazione per il progetto CAN.

Contiene le route per:
- Registrazione
- Login
- Richiesta reset password
- Reset password

Autori: Team CAN – Carlotta Forlino, Andrea Calabrò, Nicolò Giraudo
Versione: 1.0.0
"""

from fastapi import APIRouter, HTTPException, Form, status
from fastapi.responses import JSONResponse
from auth_core import register_user, login_user, request_password_reset, reset_password

router = APIRouter(
    prefix="/auth",
    tags=["Autenticazione API"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_route(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    """
    Registra un nuovo utente.
    """
    try:
        result = register_user(username, password, email)
        return JSONResponse(content={"message": "Utente registrato con successo", "data": result})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_route(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Effettua il login e restituisce il token JWT.
    """
    try:
        token = login_user(username, password)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/forgot-password")
def forgot_password_route(
    email: str = Form(...)
):
    """
    Invia un'email con il codice di reset password.
    """
    try:
        response = request_password_reset(email)
        return {"message": "Email di reset inviata (mock o reale)", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
def reset_password_route(
    email: str = Form(...),
    code: str = Form(...),
    new_password: str = Form(...)
):
    """
    Reimposta la password dopo aver ricevuto il codice di verifica.
    """
    try:
        result = reset_password(email, code, new_password)
        return {"message": "Password aggiornata con successo", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
