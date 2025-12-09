"""
Modulo mappa – Sezione principale con la mappa interattiva e il menu a tendina
per la selezione della regione. Include anche il blocco meteo regionale.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from ..api import *  # richieste API comuni (regioni, morfologia, ecc.)

# Caricamento delle regioni tramite API
df_regioni = get_regioni()
# Evita crash se l'API non ha risposto come previsto
if df_regioni is None or df_regioni.empty or "nome" not in df_regioni.columns:
    print("[MAPPA] Nessuna regione caricata: API non disponibile o risposta non valida.")
    regioni = []
else:
    regioni = sorted(df_regioni["nome"].unique())

# Layout della sezione mappa
layout = dbc.Row([
    dbc.Col(
        html.Div([
            html.H1("Cambiamento Ambientale Nazionale", className="text-center mb-2", style={"marginTop": "30px"}),
            html.H6("Scegli una regione di cui vedere i dati", className="text-center subhead mb-4",
                    style={"fontSize": "1.2rem", "fontWeight": "500"}),

            dcc.Dropdown(
                id="regione-dropdown",
                options=[{"label": r, "value": r} for r in regioni],
                value=regioni[0] if regioni else None,
                clearable=False,
                style={"width": "60%", "margin": "0 auto"}
            ),

            html.Div(id="meteo-regionale", className="text-center mt-3"),

            dcc.Graph(id="italia-map", style={"height": "500px"}, config={"scrollZoom": False})
        ])
    , md=12)
], className="mb-4", id="mappa")