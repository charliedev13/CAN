"""
Modulo auth_app.py – Pagine HTML per l’autenticazione utenti (FastAPI + Jinja2).

Contiene le route per:
- Pagina login
- Pagina registrazione
- Pagina reset password

Autori: Team CAN – Carlotta Forlino, Andrea Calabrò, Nicolò Giraudo
Versione: 1.0.0
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["Pagine HTML autenticazione"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    """
    Mostra la pagina di login.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    """
    Mostra la pagina di registrazione.
    """
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/forgot-page", response_class=HTMLResponse)
def forgot_page(request: Request):
    """
    Mostra la pagina 'Password dimenticata'.
    """
    return templates.TemplateResponse("forgot.html", {"request": request})

@router.get("/reset-page", response_class=HTMLResponse)
def reset_page(request: Request):
    """
    Mostra la pagina di reset password.
    """
    return templates.TemplateResponse("reset.html", {"request": request})