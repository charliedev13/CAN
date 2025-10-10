"""
Modulo meteo_callbacks – Gestisce la sezione meteo e la cache con OpenWeather.

Contiene:
- la funzione di aggiornamento del meteo regionale
- la logica di caching con thread daemon

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
import time
import threading
import requests
from dash import Input, Output, html
from ..app import app
from ..api import WEATHER_API_KEY

# Cache meteo e lock
meteo_cache = {}
CACHE_TTL = 3600 # 1 ora in secondi
meteo_lock = threading.Lock()

REGIONE_TO_CITY = {
    "Piemonte": "Torino",
    "Valle d'Aosta": "Aosta",
    "Lombardia": "Milano",
    "Trentino-Alto Adige": "Trento",
    "Veneto": "Venezia",
    "Friuli-Venezia Giulia": "Trieste",
    "Liguria": "Genova",
    "Emilia-Romagna": "Bologna",
    "Toscana": "Firenze",
    "Umbria": "Perugia",
    "Marche": "Ancona",
    "Lazio": "Roma",
    "Abruzzo": "L'Aquila",
    "Molise": "Campobasso",
    "Campania": "Napoli",
    "Puglia": "Bari",
    "Basilicata": "Potenza",
    "Calabria": "Catanzaro",
    "Sicilia": "Palermo",
    "Sardegna": "Cagliari"
}

# Funzione emoji in base al meteo
def meteo_emoji(description: str):
    d = description.lower()
    
    if "sereno" in d or "clear" in d:
        return "☀️"
    elif "poche nuvole" in d or "nubi sparse" in d or "nuvoloso" in d or "cielo coperto" in d or "cloud" in d:
        return "☁️"
    elif "pioggia" in d or "rain" in d or "rovesci" in d:
        return "🌧️"
    elif "temporale" in d or "storm" in d:
        return "⛈️"
    elif "neve" in d or "snow" in d:
        return "❄️"
    elif "nebbia" in d or "foschia" in d or "fog" in d or "mist" in d:
        return "🌫️"
    elif "vento" in d or "wind" in d:
        return "💨"
    elif "sole" in d and ("nuvole" in d or "cloud" in d):
        return "🌤️"
    else:
        return "🌡️"

@app.callback(
    Output("meteo-container", "children"),
    Input("regione-dropdown", "value")
)
def update_meteo(selected_region):
    with meteo_lock:
        dati = meteo_cache.get(selected_region, {"temp": "N/A", "desc": "Dati non disponibili", "emoji": "🌡️"})
    temp = dati["temp"]
    desc = dati["desc"]
    emoji = dati["emoji"]

    return html.Div([
        html.H4("Meteo", className="text-center mb-1"),
        html.H5(selected_region, className="text-center subhead mb-2"),
        html.Div([
            html.Span(f"{emoji} ", style={"fontSize": "32px", "marginRight": "10px"}),
            html.Span(f"{temp}°C – {desc.capitalize()}", style={"fontSize": "18px"})
        ], style={"textAlign": "center"})
    ], style={"marginBottom": "20px"})

def aggiorna_cache_meteo():
    """Aggiorna il meteo di tutte le regioni ogni ora."""
    while True:
        now = time.time()
        for region, city in REGIONE_TO_CITY.items():
            try:
                city_url = city.replace(" ", "")
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city_url},IT&units=metric&appid={WEATHER_API_KEY}&lang=it"
                resp = requests.get(url).json()
                temp = resp["main"]["temp"]
                desc = resp["weather"][0]["description"]
                emoji = meteo_emoji(desc)
                with meteo_lock:
                    meteo_cache[region] = {
                        "timestamp": now,
                        "temp": temp,
                        "desc": desc,
                        "emoji": emoji
                    }
                print(f"[API] Cache aggiornata per {region}: {temp}°C, {desc}")
            except Exception as e:
                print(f"[API] Errore aggiornando meteo per {region}: {e}")
        time.sleep(CACHE_TTL)  # 1 ora

# Avvio del thread daemon
threading.Thread(target=aggiorna_cache_meteo, daemon=True).start()
