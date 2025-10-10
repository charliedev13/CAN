"""
Modulo footer – Sezione finale della dashboard con citazione e credits.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Blockquote([
                html.P("“La Terra non appartiene all’uomo, è l’uomo che appartiene alla Terra.”",
                       style={"color": "#005F73"})
            ], className="blockquote text-center"),
            md=12
        )
    ], className="mb-4"),
    html.Footer(
        dbc.Container([
            html.Small("Dati ISTAT e ISPRA - Eurix Srl © 2025", className="text-white")
        ], className="text-center"),
        style={"backgroundColor": "#005f73", "padding": "10px"})
])