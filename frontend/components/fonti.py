"""
Modulo fonti – Mostra il mix energetico regionale.

Contiene il grafico a barre orizzontali con la ripartizione percentuale
tra carbone, petrolio, gas e fonti rinnovabili.

Autori: Carlotta Forlino, Andrea Calabrò, Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H4("Fonti energetiche utilizzate dalla regione",
                        className="text-center mb-3 fw-bold",
                        style={"color": "#005F73"}),
                dcc.Graph(id="grafico-mix", style={"height": "300px"})
            ])
        ), md=12
    )
], className="mb-4", id="fonti")