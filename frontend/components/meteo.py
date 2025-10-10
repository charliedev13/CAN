"""
Modulo meteo – Mostra i dati meteo aggiornati per la regione selezionata.

La sezione viene aggiornata tramite cache e API OpenWeather.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        html.Div(id="meteo-container"),
        md=12
    )
], className="mb-4", id="meteo")