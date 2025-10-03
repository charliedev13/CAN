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
BASE_URL = "http://localhost:8000"
with open("limits_IT_regions.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)
prop_name_key = "reg_name"

# Mapping speciale per regioni
geojson_to_df_map = {
    # Trentino-Alto Adige
    "Trentino-Alto Adige": "Trentino-Alto Adige",
    "Trentino-Alto Adige/Südtirol": "Trentino-Alto Adige",
    "Trentino": "Trentino-Alto Adige",
    "Alto Adige": "Trentino-Alto Adige",
    "Südtirol": "Trentino-Alto Adige",
    "South Tyrol": "Trentino-Alto Adige",
    "Provincia di Trento": "Trentino-Alto Adige",
    "Provincia di Bolzano": "Trentino-Alto Adige",
    "Bolzano-Bozen": "Trentino-Alto Adige",
    # Valle d'Aosta
    "Valle d'Aosta/Vallée d'Aoste": "Valle d'Aosta",
    "Vallée d'Aoste": "Valle d'Aosta",
    "Val d'Outa": "Valle d'Aosta",
    "Augschtalann": "Valle d'Aosta",
    "Ougstalland": "Valle d'Aosta",
    "Val d'Osta": "Valle d'Aosta"
}

# --------------------------
# CARICAMENTO DATI DAL BACKEND
# --------------------------
regioni_resp = requests.get(f"{BASE_URL}/regioni").json()
morf_resp = requests.get(f"{BASE_URL}/morfologia").json()
assorb_resp = requests.get(f"{BASE_URL}/assorbimenti").json()
emiss_resp = requests.get(f"{BASE_URL}/emissioni").json()
mix_resp = requests.get(f"{BASE_URL}/mix").json()
edifici_resp = requests.get(f"{BASE_URL}/edifici").json()

df_regioni = pd.DataFrame(regioni_resp)
df_morf = pd.DataFrame(morf_resp).merge(df_regioni, on="id_regione")
df_morf.rename(columns={"nome": "Regione"}, inplace=True)
df_assorb = pd.DataFrame(assorb_resp).merge(df_regioni, on="id_regione")
df_assorb.rename(columns={"nome": "Regione"}, inplace=True)
df_emiss = pd.DataFrame(emiss_resp).merge(df_regioni, on="id_regione")
df_emiss.rename(columns={"nome": "Regione"}, inplace=True)
df_mix = pd.DataFrame(mix_resp).merge(df_regioni, on="id_regione")
df_mix.rename(columns={"nome": "Regione"}, inplace=True)
df_edifici = pd.DataFrame(edifici_resp).merge(df_regioni, on="id_regione")
df_edifici.rename(columns={"nome": "Regione"}, inplace=True)

# Conversione per morfologia (long format)
df_morf["geo_region"] = df_morf["Regione"]
exclude_cols = ["id_regione", "Regione", "geo_region", "superficie_kmq", "densita_demografica", "pil"]
df_long = df_morf.melt(
    id_vars=["id_regione", "Regione", "geo_region"],
    value_vars=[c for c in df_morf.columns if c not in exclude_cols],
    var_name="Morfologia",
    value_name="Percentuale"
)

# Allineamento nomi geojson con DB
df_long["geo_region"] = df_long["geo_region"].replace({
    "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste",
    "Trentino-Alto Adige": "Trentino-Alto Adige/Südtirol"
})

regioni = sorted(df_regioni["nome"].unique())

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
    if not txt:
        return None, 2
    t = txt.lower()
    if "assorbimenti" in t and ("inferiore" in t or "migliorare" in t):
        return "assorbimenti", 1
    if "emissioni" in t and ("elevate" in t or "superiore" in t):
        return "emissioni", 3
    return None, 2

# --------------------------
# LAYOUT
# --------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title="CAN Dashboard")

app.layout = dbc.Container(fluid=True, children=[
    
    # Navbar/Header
    dbc.NavbarSimple(brand="Progetto CAN – Dashboard", color="primary", dark=True, className="mb-3"),

    # Sezione Mappa + Dropdown
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="regione-dropdown",
                options=[{"label": r, "value": r} for r in regioni],
                value=regioni[0],
                clearable=False
            ), md=4
        ),
        dbc.Col(dcc.Graph(id="italia-map", style={"height": "500px"}), md=8)
    ], className="mb-4"),

    # Sezione Grafici a torta morfologia
    dbc.Row([
    dbc.Col(
        dcc.Graph(id="grafico-altimetria", style={"height": "350px"}),
        md=6
    ),
    dbc.Col(
        dcc.Graph(id="grafico-uso", style={"height": "350px"}),
        md=6
    )
    ], className="mb-4"),

    # Sezione Aree di miglioramento (semaforo)
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Aree di miglioramento"),
                html.Div(id="contenitore-semaforo")
            ])), md=12
        )
    ], className="mb-4"),

    # Sezione Mix Energetico
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Mix energetico"),
                dcc.Graph(id="grafico-mix", style={"height": "300px"})
            ])), md=12
        )
    ], className="mb-4"),

    # Sezione Edifici
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Indicatori sugli edifici"),
                dcc.Graph(id="grafico-edifici", style={"height": "400px"})
            ])), md=12
        )
    ], className="mb-4"),

    # Sezione Azioni
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(id="azioni-fotovoltaico-img", className="azioni-img"),
                html.H5("Capacità fotovoltaico (GW)", className="text-center"),
                html.Div(id="azioni-fotovoltaico-val", className="azioni-val text-center")
            ])), md=3
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(id="azioni-fer-img", className="azioni-img"),
                html.H5("Produzione da FER (%)", className="text-center"),
                html.Div(id="azioni-fer-val", className="azioni-val text-center")
            ])), md=3
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(id="azioni-auto-img", className="azioni-img"),
                html.H5("Auto elettriche (%)", className="text-center"),
                html.Div(id="azioni-auto-val", className="azioni-val text-center")
            ])), md=3
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(id="azioni-risparmio-img", className="azioni-img"),
                html.H5("Risparmi energetici (Mtep mln)", className="text-center"),
                html.Div(id="azioni-risparmio-val", className="azioni-val text-center")
            ])), md=3
        )
    ], className="mb-4"),

    # Footer
    html.Footer(dbc.Container([html.Hr(), html.Small("Progetto CAN – Dashboard", className="text-muted")]))
])

# --------------------------
# CALLBACKS
# --------------------------

# --- Mappa + Grafico Morfologia ---
@app.callback(
    Output("italia-map", "figure"),
    Output("grafico-altimetria", "figure"),
    Output("grafico-uso", "figure"),
    Output("regione-dropdown", "value"),
    Input("regione-dropdown", "value"),
    Input("italia-map", "clickData")
)
def update_all(drop_val, clickData):
    # --------------------------
    # Selezione regione da dropdown o click sulla mappa
    # --------------------------
    selected_region = drop_val
    trigger = ctx.triggered_id

    if trigger == "italia-map" and clickData:
        pts = clickData.get("points")
        if pts and len(pts) > 0:
            clicked_loc = pts[0].get("location") or pts[0].get("hovertext")
            if clicked_loc in geojson_to_df_map:
                clicked_loc = geojson_to_df_map[clicked_loc]
            if clicked_loc in df_long["geo_region"].values:
                selected_region = clicked_loc

    # --------------------------
    # Mappa coropletica
    # --------------------------
    df_map = pd.DataFrame({"geo_region": df_long["geo_region"].unique()})
    df_map["sel"] = df_map["geo_region"].apply(lambda g: 1 if g == selected_region else 0)

    fig_map = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        locations="geo_region",
        featureidkey=f"properties.{prop_name_key}",
        color="sel",
        color_continuous_scale=["#cccccc", "#ff7f0e"],
        range_color=(0, 1),
        mapbox_style="carto-positron",
        center={"lat": 41.9, "lon": 12.5},
        zoom=5.5,
        opacity=0.7,
        hover_name="geo_region"
    )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)

    # --------------------------
    # Grafici a torta morfologia (uso del suolo)
    # --------------------------
    dati_regione = df_long[df_long["Regione"] == selected_region].copy()

    # --- Grafico 1: Pianura, Collina, Montagna ---
    morf_altimetrica = dati_regione[dati_regione["Morfologia"].isin(
        ["pianura_pct", "collina_pct", "montagna_pct"]
    )].copy()

    morf_altimetrica["Morfologia"] = morf_altimetrica["Morfologia"].map({
        "pianura_pct": "Pianura",
        "collina_pct": "Collina",
        "montagna_pct": "Montagna"
    })

    fig_altimetrica = px.pie(
        morf_altimetrica,
        names="Morfologia",
        values="Percentuale",
        title=f"Altimetria del suolo in {selected_region} (%)",
        color="Morfologia",
        color_discrete_map={
            "Pianura": "lightgreen",
            "Collina": "yellow",
            "Montagna": "saddlebrown"
        }
    )
    fig_altimetrica.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=12,
        pull=[0.05]*len(morf_altimetrica),
        marker=dict(line=dict(color="#000000", width=0.5))
    )
    fig_altimetrica.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(orientation="v", y=0.5, x=1.1, valign="middle")
    )
    fig_altimetrica.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

    # --- Grafico 2: Agricolo, Urbano, Forestale ---
    morf_uso = dati_regione[dati_regione["Morfologia"].isin(
        ["agricolo_pct", "urbano_pct", "forestale_pct"]
    )].copy()

    morf_uso["Morfologia"] = morf_uso["Morfologia"].map({
        "agricolo_pct": "Aree agricole",
        "urbano_pct": "Aree urbane",
        "forestale_pct": "Aree forestali"
    })

    fig_uso = px.pie(
        morf_uso,
        names="Morfologia",
        values="Percentuale",
        title=f"Uso del suolo in {selected_region} (%)",
        color="Morfologia",
        color_discrete_map={
            "Aree agricole": "orange",
            "Aree urbane": "gray",
            "Aree forestali": "green"
        }
    )
    fig_uso.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=12,
        pull=[0.05]*len(morf_uso),
        marker=dict(line=dict(color="#000000", width=0.5))
    )
    fig_uso.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(orientation="v", y=0.5, x=1.1, valign="middle")
    )
    fig_uso.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

    # --------------------------
    # Return → mappa + i 2 grafici torta
    # --------------------------
    return fig_map, fig_altimetrica, fig_uso, selected_region

# --------------------------
# SEMAFORO (Aree di miglioramento)
# --------------------------
@app.callback(
    Output("contenitore-semaforo", "children"),
    Input("regione-dropdown", "value")
)
def update_semaforo(selected_region):
    record = df_assorb[df_assorb["Regione"] == selected_region]
    testo = record["aree_miglioramento"].iloc[0] if not record.empty else None
    tipo, score = semaforo_from_text(testo)

    record_emiss = df_emiss[df_emiss["Regione"] == selected_region]
    valore_emiss = record_emiss["co2eq_mln_t"].iloc[0] if not record_emiss.empty else None
    sottotitolo = f"Emissioni annuali di gas serra: {valore_emiss} milioni di tonnellate" if valore_emiss else ""

    if tipo == "assorbimenti":
        return html.Div([
            html.H6("🌿 Assorbimenti", className="mt-2"),
            html.Div([
                dot_row(score, "#27ae60"),
                html.Span(testo, style={"marginLeft": "10px"})
            ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
            html.Small(sottotitolo, className="text-muted")
        ])
    elif tipo == "emissioni":
        return html.Div([
            html.H6("🏭 Emissioni", className="mt-2"),
            html.Div([
                dot_row(score, "#e74c3c"),
                html.Span(testo, style={"marginLeft": "10px"})
            ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
            html.Small(sottotitolo, className="text-muted")
        ])
    else:
        return html.Small("Nessuna area di miglioramento definita", className="text-muted")


# --------------------------
# MIX ENERGETICO
# --------------------------
@app.callback(
    Output("grafico-mix", "figure"),
    Input("regione-dropdown", "value")
)
def update_mix(selected_region):
    record = df_mix[df_mix["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile")

    valori = {
        "Carbone": record["carbone_pct"].iloc[0],
        "Petrolio": record["petrolio_pct"].iloc[0],
        "Gas": record["gas_pct"].iloc[0],
        "Rinnovabili": record["rinnovabili_pct"].iloc[0]
    }
    colori = ["black", "#008080", "gray", "lightgreen"]

    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v}%" for v in valori.values()],
        labels={"x": "Fonte", "y": "Percentuale"},
        title="Mix energetico (%)"
    )
    fig.update_traces(marker_color=colori, textposition="outside")
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=40), yaxis=dict(range=[0, 100]))
    return fig


# --------------------------
# EDIFICI
# --------------------------
@app.callback(
    Output("grafico-edifici", "figure"),
    Input("regione-dropdown", "value")
)
def update_edifici(selected_region):
    record = df_edifici[df_edifici["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile")

    valori = {
        "Consumo medio di energia degli edifici": record["consumo_medio_kwh_m2y"].iloc[0],
        "Emissioni medie di gas serra per abitante": record["emissioni_procapite_tco2_ab"].iloc[0],
        "Uso di energia elettrica sugli edifici (%)": record["quota_elettrico_pct"].iloc[0],
        "Edifici ad alta efficienza (Classe A) (%)": record["quota_ape_classe_a_pct"].iloc[0]
    }
    colori = ["#A6CEE3", "#B2DF8A", "#FDBF6F", "#CAB2D6"]

    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v}" for v in valori.values()],
        labels={"x": "Indicatore", "y": "Valore"},
        title="Indicatori sugli edifici"
    )
    fig.update_traces(marker_color=colori, textposition="outside")
    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=100),
        xaxis=dict(title="", tickangle=-20),
        yaxis=dict(title="")
    )
    return fig

# --------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
