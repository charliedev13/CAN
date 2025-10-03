"""Dashboard CAN con mappa interattiva, KPI e semafori dinamici.
Per avviare:
    python app.py
"""

import json
import requests
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc

# --------------------------
# CONFIG
# --------------------------
BASE_URL = "http://localhost:8000"  # API FastAPI
with open("limits_IT_regions.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)
prop_name_key = "reg_name"

# --------------------------
# CARICAMENTO DATI DAL BACKEND
# --------------------------
# Regioni e morfologia
regioni_resp = requests.get(f"{BASE_URL}/regioni").json()
morf_resp = requests.get(f"{BASE_URL}/morfologia").json()

df_regioni = pd.DataFrame(regioni_resp)   # colonne: id_regione, nome, ...
df_morf = pd.DataFrame(morf_resp)         # colonne: id_regione, pianura_pct, ...

# Merge su id_regione
df = df_morf.merge(df_regioni, on="id_regione")
df.rename(columns={"nome": "Regione"}, inplace=True)

# Conversione numeri
for col in df.columns:
    if col not in ["id_regione", "Regione"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Per grafici (long format)
df["geo_region"] = df["Regione"]
df_long = df.melt(
    id_vars=["id_regione", "Regione", "geo_region"],
    var_name="Morfologia",
    value_name="Percentuale"
)

# Assorbimenti
assorb_resp = requests.get(f"{BASE_URL}/assorbimenti").json()
df_assorb = pd.DataFrame(assorb_resp).merge(df_regioni, on="id_regione")
df_assorb.rename(columns={"nome": "Regione"}, inplace=True)

# Emissioni totali
emiss_resp = requests.get(f"{BASE_URL}/emissioni").json()
df_emiss = pd.DataFrame(emiss_resp).merge(df_regioni, on="id_regione")
df_emiss.rename(columns={"nome": "Regione"}, inplace=True)

regioni = df["Regione"].unique()

# --------------------------
# DASH APP
# --------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title="CAN Dashboard")

# --------------------------
# FUNZIONI DI SUPPORTO
# --------------------------
def dot(active: bool, color="#27ae60"):
    return html.Span(style={
        "width": "12px", "height": "12px", "borderRadius": "50%",
        "display": "inline-block", "marginRight": "6px",
        "backgroundColor": color if active else "#e9ecef",
        "border": "1px solid #ced4da"
    })

def dot_row(active_count=2, color="#27ae60"):
    return html.Div([dot(i < active_count, color) for i in range(3)], style={"display":"flex"})

def semaforo_from_text(txt: str):
    """Ritorna ('assorbimenti'/'emissioni'/None, score) in base al testo"""
    if not txt:
        return None, 2
    t = txt.lower()
    if "assorbimenti" in t and ("inferiore" in t or "migliorare" in t):
        return "assorbimenti", 1
    if "emissioni" in t and ("elevate" in t or "superiori" in t):
        return "emissioni", 3
    return None, 2

# --------------------------
# LAYOUT
# --------------------------
app.layout = dbc.Container(fluid=True, children=[

    dbc.NavbarSimple(brand="Progetto CAN – Dashboard", color="primary", dark=True, className="mb-3"),

    # Dropdown + Mappa
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="regione-dropdown",
                options=[{"label": r, "value": r} for r in regioni],
                value="Abruzzo",
                clearable=False
            ), md=4
        ),
        dbc.Col(dcc.Graph(id="italia-map", style={"height": "500px"}), md=8)
    ], className="mb-4"),

    # KPI + grafico morfologia
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Consumo medio"), html.H3("—")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Emissioni pro capite"), html.H3("—")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Quota elettrico"), html.H3("—")])), md=3),
        dbc.Col(dcc.Graph(id="grafico-regionale", style={"height": "250px"}), md=3),
    ], className="mb-4"),

    # Aree di miglioramento (dinamico)
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Aree di miglioramento"),
                html.Div(id="contenitore-semaforo")  # callback lo popola
            ])), md=12
        )
    ], className="mb-4"),

    html.Footer(
        dbc.Container([html.Hr(), html.Small("Progetto CAN – Dashboard", className="text-muted")])
    )
])

# --------------------------
# CALLBACK MAPPA E TORTA
# --------------------------
@app.callback(
    Output("italia-map", "figure"),
    Output("grafico-regionale", "figure"),
    Output("regione-dropdown", "value"),
    Input("regione-dropdown", "value"),
    Input("italia-map", "clickData")
)
def update_all(drop_val, clickData):
    selected_region = drop_val
    trigger = ctx.triggered_id

    if trigger == "italia-map" and clickData:
        pts = clickData.get("points")
        if pts and len(pts) > 0:
            clicked_loc = pts[0].get("location") or pts[0].get("hovertext")
            if clicked_loc in df["geo_region"].values:
                selected_region = clicked_loc

    df_map = pd.DataFrame({"geo_region": df["geo_region"].unique()})
    df_map["sel"] = df_map["geo_region"].apply(lambda g: 1 if g == selected_region else 0)

    fig_map = px.choropleth_mapbox(
        df_map, geojson=geojson, locations="geo_region",
        featureidkey=f"properties.{prop_name_key}",
        color="sel", color_continuous_scale=["#cccccc", "#ff7f0e"], range_color=(0,1),
        mapbox_style="carto-positron", center={"lat":41.9, "lon":12.5}, zoom=5.5, opacity=0.7,
        hover_name="geo_region"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)

    dati_regione = df_long[df_long["Regione"] == selected_region]
    fig_chart = px.pie(dati_regione, names="Morfologia", values="Percentuale", title="Morfologia")

    return fig_map, fig_chart, selected_region

# --------------------------
# CALLBACK SEMAFORO
# --------------------------
@app.callback(
    Output("contenitore-semaforo", "children"),
    Input("regione-dropdown", "value")
)
def update_semaforo(selected_region):
    # Recupero testo da assorbimenti
    record = df_assorb[df_assorb["Regione"] == selected_region]
    testo = record["aree_miglioramento"].iloc[0] if not record.empty else None

    tipo, score = semaforo_from_text(testo)

    # Recupero emissioni totali
    record_emiss = df_emiss[df_emiss["Regione"] == selected_region]
    valore_emiss = record_emiss["co2eq_mln_t"].iloc[0] if not record_emiss.empty else None
    sottotitolo = f"Milioni di tonnellate CO₂ eq: {valore_emiss}" if valore_emiss else ""

    if tipo == "assorbimenti":
        return html.Div([
            html.H6("🌿 Assorbimenti", className="mt-2"),
            dot_row(score, "#27ae60"),
            html.Small(sottotitolo, className="text-muted")
        ])
    elif tipo == "emissioni":
        return html.Div([
            html.H6("🏭 Emissioni", className="mt-2"),
            dot_row(score, "#e74c3c"),
            html.Small(sottotitolo, className="text-muted")
        ])
    else:
        return html.Small("Nessuna area di miglioramento definita", className="text-muted")

# --------------------------
if __name__ == "__main__":
    app.run(debug=True)