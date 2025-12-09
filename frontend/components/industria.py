"""
Modulo industria – Sezione dedicata ai dati sulle emissioni e consumo energetico industriale.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H5(id="titolo-industria", className="mb-3"),
            dcc.Graph(id="grafico-industria", style={"height": "350px"})
        ])), md=12
    )
], className="mb-4", id="industria")