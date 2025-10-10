"""
Modulo navbar_callbacks – Gestisce il comportamento della barra di navigazione.

In particolare, controlla l'apertura e la chiusura del menu "hamburger"
nelle visualizzazioni mobile.

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import Input, Output, State
from ..app import app


@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open")
)
def toggle_navbar(n, is_open):
    """
    Apre o chiude la navbar in base al numero di click sul pulsante hamburger.

    Args:
        n (int): Numero di click sul toggler.
        is_open (bool): Stato attuale del menu.

    Returns:
        bool: True se il menu deve aprirsi, False se deve chiudersi.
    """
    if n:
        return not is_open
    return is_open