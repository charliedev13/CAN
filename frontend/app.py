"""
CAN Dashboard – Applicazione di visualizzazione ambientale e energetica nazionale

Questa è la versione completamente componentizzata della dashboard CAN.
Integra frontend interattivo (Dash) e backend (FastAPI) tramite richieste REST.

Struttura:
    components/   → layout delle singole sezioni
    callbacks/    → funzioni interattive e logica dei grafici
    api.py        → chiamate al backend FastAPI
    data_utils.py → dati condivisi e funzioni di supporto

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""

from dash import Dash
import dash_bootstrap_components as dbc

# ===========================
# IMPORT COMPONENTI (layout)
# ===========================
from .components.navbar import layout as navbar_layout
from .components.mappa import layout as mappa_layout
from .components.meteo import layout as meteo_layout
from .components.suolo import layout as suolo_layout
from .components.swot import layout as swot_layout
from .components.fonti import layout as fonti_layout
from .components.edifici import layout as edifici_layout
from .components.azioni import layout as azioni_layout
from .components.industria import layout as industria_layout
from .components.comparazione import layout as comparazione_layout
from .components.footer import layout as footer_layout

# ===========================
# INIZIALIZZAZIONE APP DASH
# ===========================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="CAN Dashboard"
)
app.title = "CAN Dashboard"
server = app.server  # per compatibilità con eventuale deploy

# ===========================
# LAYOUT COMPLETO DELL'APP
# ===========================
app.layout = dbc.Container(fluid=True, children=[
    navbar_layout,
    mappa_layout,
    meteo_layout,
    suolo_layout,
    swot_layout,
    fonti_layout,
    edifici_layout,
    azioni_layout,
    industria_layout,
    comparazione_layout,
    footer_layout
])

# ===========================
# IMPORT CALLBACKS
# ===========================
from .callbacks.navbar_callbacks import *
from .callbacks.mappa_callbacks import *
from .callbacks.meteo_callbacks import *
from .callbacks.swot_callbacks import *
from .callbacks.fonti_callbacks import *
from .callbacks.edifici_callbacks import *
from .callbacks.azioni_callbacks import *
from .callbacks.industria_callbacks import *
from .callbacks.comparazione_callbacks import *

# ===========================
# AVVIO SERVER
# ===========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)

