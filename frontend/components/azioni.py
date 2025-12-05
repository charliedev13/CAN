"""
Modulo azioni – Mostra le iniziative regionali per l’ambiente:
fotovoltaico, FER, auto elettriche e risparmio energetico.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html
import dash_bootstrap_components as dbc

TCS = "text-center subhead"
AVTC = "azioni-val text-center"

layout = html.Div([
    html.H4("Cosa sta facendo la regione per l’ambiente", className="text-center mb-4 fw-bold"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div(html.Img(src="/assets/pannello.png", style={"width": "60%"}), className="azioni-img"),
            html.H5("Impianti solari attivi", className="TCS"),
            html.Div(id="azioni-fotovoltaico-val", className=AVTC)
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div(html.Img(src="/assets/palaeolica.png", style={"width": "60%"}), className="azioni-img"),
            html.H5("Energia rinnovabile prodotta", className="TCS"),
            html.Div(id="azioni-fer-val", className=AVTC)
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div(html.Img(src="/assets/autoelettrica.png", style={"width": "60%"}), className="azioni-img"),
            html.H5("Auto elettriche in circolazione", className="TCS"),
            html.Div(id="azioni-auto-val", className=AVTC)
        ])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div(html.Img(src="/assets/casa.png", style={"width": "60%"}), className="azioni-img"),
            html.H5("Energia risparmiata", className="TCS"),
            html.Div(id="azioni-risparmio-val", className=AVTC)
        ])), md=3)
    ], className="mb-4 justify-content-center")
], className="mb-4", id="azioni")