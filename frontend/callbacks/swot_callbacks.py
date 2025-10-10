"""
Modulo swot_callbacks – Gestisce la sezione SWOT:
- Punto di forza
- Aree di miglioramento (semaforo)

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
from dash import Input, Output, html
from ..app import app
from ..data_utils import df_assorb, df_emissioni


def dot(active: bool, color="#27ae60"):
    """Crea un piccolo cerchio colorato per il semaforo."""
    return html.Span(style={
        "width": "12px", "height": "12px", "borderRadius": "50%",
        "display": "inline-block", "marginRight": "6px",
        "backgroundColor": color if active else "#e9ecef",
        "border": "1px solid #ced4da"
    })


def dot_row(active_count=2, color="#27ae60"):
    """Crea una riga orizzontale di tre pallini (semaforo)."""
    return html.Div([dot(i < active_count, color) for i in range(3)],
                    style={"display": "flex"})


def semaforo_from_text(txt: str):
    """Interpreta il testo per determinare il tipo di area e il punteggio."""
    if not txt:
        return None, 2
    t = txt.lower()
    if "assorbimenti" in t and ("inferiore" in t or "migliorare" in t):
        return "assorbimenti", 1
    if "emissioni" in t and ("elevate" in t or "superiore" in t):
        return "emissioni", 3
    return None, 2


@app.callback(
    Output("contenitore-semaforo", "children"),
    Input("regione-dropdown", "value")
)
def update_semaforo(selected_region):
    """Aggiorna il semaforo delle aree di miglioramento."""
    record = df_assorb[df_assorb["Regione"] == selected_region]
    testo = record["aree_miglioramento"].iloc[0] if not record.empty else None
    tipo, score = semaforo_from_text(testo)

    valore_emiss = df_emissioni.loc[df_emissioni["Regione"] == selected_region, "emissioni_totali_mln_t"].iloc[0] if selected_region in df_emissioni["Regione"].values else None
    sottotitolo = f"Emissioni totali di gas serra: {valore_emiss} milioni di tonnellate di CO₂" if valore_emiss else ""

    if tipo == "assorbimenti":
        colore = "#27ae60"
        titolo = "🌿 Assorbimenti"
    elif tipo == "emissioni":
        colore = "#e74c3c"
        titolo = "🏭 Emissioni"
    else:
        return html.Small("Nessuna area di miglioramento definita", className="text-muted")

    return html.Div([
        html.H6(titolo, className="mt-2"),
        html.Div([
            dot_row(score, colore),
            html.Span(testo, style={"marginLeft": "10px"})
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Small(sottotitolo, className="text-muted")
    ])


@app.callback(
    Output("contenitore-punto-forza", "children"),
    Input("regione-dropdown", "value")
)
def update_punto_forza(selected_region):
    """Aggiorna il box del punto di forza della regione selezionata."""
    record = df_assorb[df_assorb["Regione"] == selected_region]
    testo = record["punti_forza"].iloc[0] if not record.empty else None

    if not testo:
        return html.Small("Nessun punto di forza indicato", className="text-muted")

    return html.Div([
        html.H6("💪 Questa regione si distingue per:", className="mt-2"),
        html.Div([html.Span(testo, style={"marginLeft": "10px"})],
                 style={"display": "flex", "alignItems": "center", "marginBottom": "8px"})
    ])