"""
Modulo api – Gestisce le richieste al backend FastAPI e restituisce
DataFrame Pandas con i dati richiesti.

Questo modulo centralizza tutte le chiamate REST ai vari endpoint:
regioni, morfologia, assorbimenti, mix energetico, edifici, industria e azioni.

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import threading

# --- CONFIGURAZIONE BASE ---
BASE_URL = "http://backend:8000"
from pathlib import Path
from dotenv import load_dotenv

# Caricamento sicuro del file .env indipendentemente dalla working directory
env_path = Path(__file__).resolve().parent / "meteo.env"
load_dotenv(dotenv_path=env_path)
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
meteo_lock = threading.Lock()

# ===========================
# FUNZIONI DI RICHIESTA DATI
# ===========================

def get_regioni():
    """Restituisce il DataFrame con tutte le regioni italiane."""
    try:
        resp = requests.get(f"{BASE_URL}/regioni").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando regioni: {e}")
        return pd.DataFrame()


def get_morfologia():
    """Restituisce i dati sulla morfologia del suolo."""
    try:
        resp = requests.get(f"{BASE_URL}/morfologia").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando morfologia: {e}")
        return pd.DataFrame()


def get_assorbimenti():
    """Restituisce i dati sugli assorbimenti regionali."""
    try:
        resp = requests.get(f"{BASE_URL}/assorbimenti").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando assorbimenti: {e}")
        return pd.DataFrame()

def get_emissioni():
    """Restituisce i dati sulle emissioni totali regionali."""
    try:
        resp = requests.get(f"{BASE_URL}/emissioni").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando emissioni totali: {e}")
        return pd.DataFrame()

def get_mix():
    """Restituisce i dati del mix energetico regionale."""
    try:
        resp = requests.get(f"{BASE_URL}/mix").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando mix: {e}")
        return pd.DataFrame()


def get_edifici():
    """Restituisce i dati energetici e ambientali sugli edifici."""
    try:
        resp = requests.get(f"{BASE_URL}/edifici").json()
        df = pd.DataFrame(resp)
        regioni = get_regioni()
        return df.merge(regioni, on="id_regione", how="inner", validate="one_to_one").rename(columns={"nome": "Regione"})
    except Exception as e:
        print(f"[API] Errore caricando edifici: {e}")
        return pd.DataFrame()


def get_industria():
    """Restituisce i dati sulle emissioni e l’energia del settore industriale."""
    try:
        resp = requests.get(f"{BASE_URL}/industria").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando industria: {e}")
        return pd.DataFrame()


def get_azioni():
    """Restituisce i dati sulle azioni positive regionali (FER, auto, risparmi)."""
    try:
        resp = requests.get(f"{BASE_URL}/azioni").json()
        return pd.DataFrame(resp)
    except Exception as e:
        print(f"[API] Errore caricando azioni: {e}")
        return pd.DataFrame()


# ===========================
# UTILITÀ AGGIUNTIVE
# ===========================

def check_api_connection():
    """Verifica che il backend FastAPI sia raggiungibile."""
    try:
        resp = requests.get(BASE_URL)
        if resp.status_code == 200:
            print("[API] Connessione al backend OK ✅")
        else:
            print(f"[API] Backend risponde con codice {resp.status_code}")
    except Exception as e:
        print(f"[API] Errore di connessione: {e}")
