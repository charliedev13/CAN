"""
Modulo swot – Sezione Punti di forza e Aree di miglioramento.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H5("Punto di forza"),
                html.Div(id="contenitore-punto-forza", className="flex-grow-1")
            ]),
            className="carta-sezione"
        ), md=6
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H5("Aree di miglioramento"),
                html.Div(id="contenitore-semaforo", className="flex-grow-1")
            ]),
            className="carta-sezione"
        ), md=6
    )
], className="mb-4", align="stretch", id="swot")