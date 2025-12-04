"""
Modulo navbar – Barra di navigazione principale della CAN Dashboard.

Contiene il brand e i link di ancoraggio alle sezioni principali della dashboard:
Mappa, Suolo, Fonti, Edifici, Azioni, Industria e Confronta tu.

Autore: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("CAN", className="text-white fw-bold me-5 padding-left-15"),

        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Mappa", href="#mappa", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Suolo", href="#suolo", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Fonti", href="#fonti", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Edifici", href="#edifici", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Azioni", href="#azioni", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Industria", href="#industria", external_link=True, className="text-white")),
                dbc.NavItem(dbc.NavLink("Confronta tu", href="#confronta tu", external_link=True, className="text-white")),
            ], className="ms-auto", navbar=True),
            id="navbar-collapse",
            is_open=False,
            navbar=True,
        ),
    ]),
    color="#005f73",
    dark=True,
    className="mb-3"
)