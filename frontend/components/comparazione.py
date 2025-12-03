"""
Modulo comparazione – Permette il confronto di un dato tra due regioni
su una categoria scelta dall’utente.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html, dcc
from ..api import get_regioni

regioni = sorted(get_regioni()["nome"].unique())

layout = html.Div(
    id="comparazione",  # <-- ora il CSS lo prende sicuro
    children=[
        html.H4(
            "Ora scegli tu: compara un dato di tua preferenza",
            className="text-center mb-2"
        ),
        html.H6(
            "Scegli le due regioni e la categoria",
            className="text-center mb-4"
        ),

        # blocco dropdown uno sotto l'altro
        html.Div(
            className="comparazione-dropdowns",
            children=[
                dcc.Dropdown(
                    id="dropdown-regione-1",
                    options=[{"label": r, "value": r} for r in regioni],
                    value="Abruzzo",
                    clearable=False
                ),
                dcc.Dropdown(
                    id="dropdown-regione-2",
                    options=[{"label": r, "value": r} for r in regioni if r != "Abruzzo"],
                    value="Basilicata",
                    clearable=False
                ),
                dcc.Dropdown(
                    id="dropdown-categoria",
                    options=[],
                    placeholder="Seleziona una categoria",
                    clearable=False
                ),
            ],
        ),

        dcc.Graph(id="grafico-comparazione", style={"height": "400px"})
    ]
)