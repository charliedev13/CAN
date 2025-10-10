"""
Modulo suolo – Sezione dedicata alla morfologia e all’uso del suolo.
Contiene due grafici a torta: altimetria e uso del territorio.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H4(id="titolo-altimetria", className="text-center mb-3 fw-bold", style={"color": "#005F73"}),
            dcc.Graph(id="grafico-altimetria", style={"height": "400px"})
        ])),
        md=6
    ),
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H4(id="titolo-uso", className="text-center mb-3 fw-bold", style={"color": "#005F73"}),
            dcc.Graph(id="grafico-uso", style={"height": "400px"})
        ])),
        md=6
    )
], className="mb-4 justify-content-center align-items-stretch", id="suolo")