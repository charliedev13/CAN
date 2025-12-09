"""
Modulo edifici – Sezione sui consumi e la sostenibilità degli edifici regionali.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Row([
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H5("Consumi e sostenibilità degli edifici"),
            dcc.Graph(id="grafico-edifici", style={"height": "400px"})
        ])), md=12
    )
], className="mb-4", id="edifici")