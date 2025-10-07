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
    # Header
dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("CAN", className="text-white fw-bold me-5"),

        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Mappa", href="#mappa", external_link=True, className="text-white")),
            dbc.NavItem(dbc.NavLink("Suolo", href="#suolo", external_link=True, className="text-white")),
            dbc.NavItem(dbc.NavLink("Fonti", href="#fonti", external_link=True, className="text-white")),
            dbc.NavItem(dbc.NavLink("Edifici", href="#edifici", external_link=True, className="text-white")),
            dbc.NavItem(dbc.NavLink("Industria", href="#industria", external_link=True, className="text-white")),
        ], className="ms-auto", navbar=True)
    ]),
    color="#005f73", dark=True, className="mb-3"),

    # Sezione Mappa + Dropdown
    # Sezione Mappa
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H2("Cambiamento Ambientale Nazionale", className="text-center mb-2"),
                html.H5("Scegli una regione di cui vedere i dati", className="text-center mb-4"),
                dcc.Dropdown(
                    id="regione-dropdown",
                    options=[{"label": r, "value": r} for r in regioni],
                    value=regioni[0],
                    clearable=False,
                    style={"width": "60%", "margin": "0 auto"}
                ),
                dcc.Graph(id="italia-map", style={"height": "500px"})
            ])
        , md=12)
    ], className="mb-4", id="mappa"),


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

    # Sezione Punti di forza + Aree di miglioramento (altezza uguale)
    dbc.Row([
        # Colonna sinistra – Punto di forza
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Punto di forza"),
                    html.Div(id="contenitore-punto-forza", className="flex-grow-1")
                ]),
                className="carta-sezione"
            ), md=6
        ),

        # Colonna destra – Aree di miglioramento
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Aree di miglioramento"),
                    html.Div(id="contenitore-semaforo", className="flex-grow-1")
                ]),
                className="carta-sezione"
            ), md=6
        )
    ], className="mb-4", align="stretch"),

    # Sezione Mix Energetico
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Mix energetico"),
                dcc.Graph(id="grafico-mix", style={"height": "300px"})
            ])), md=12
        )
    ], className="mb-4", id="fonti"),

    # Sezione Edifici
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Indicatori sugli edifici"),
                dcc.Graph(id="grafico-edifici", style={"height": "400px"})
            ])), md=12
        )
    ], className="mb-4", id="edifici"),

    # Sezione Azioni
    dbc.Row([
        # Fotovoltaico
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(
                    html.Img(src="/assets/pannello.png", style={"width": "60%"}),
                    className="azioni-img"
                ),
                html.H5("Capacità fotovoltaico (GW)", className="text-center"),
                html.Div(id="azioni-fotovoltaico-val", className="azioni-val text-center")
            ])), md=3
        ),

        # Produzione da FER
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(
                    html.Img(src="/assets/palaeolica.png", style={"width": "60%"}),
                    className="azioni-img"
                ),
                html.H5("Produzione da FER (%)", className="text-center"),
                html.Div(id="azioni-fer-val", className="azioni-val text-center")
            ])), md=3
        ),

        # Auto elettriche
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(
                    html.Img(src="/assets/autoelettrica.png", style={"width": "60%"}),
                    className="azioni-img"
                ),
                html.H5("Auto elettriche (%)", className="text-center"),
                html.Div(id="azioni-auto-val", className="azioni-val text-center")
            ])), md=3
        ),

        # Risparmi energetici
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.Div(
                    html.Img(src="/assets/casa.png", style={"width": "60%"}),
                    className="azioni-img"
                ),
                html.H5("Risparmi energetici (Mtep mln)", className="text-center"),
                html.Div(id="azioni-risparmio-val", className="azioni-val text-center")
            ])), md=3
        )
    ], className="mb-4"),

    # Sezione Industria
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5(id="titolo-industria", className="mb-3"),
                dcc.Graph(id="grafico-industria", style={"height": "350px"})
            ])), md=12
        )
    ], className="mb-4", id="industria"),

    # Sezione frase d'effetto
    dbc.Row([
        dbc.Col(
            html.Blockquote([
                html.P("“La Terra non appartiene all’uomo, è l’uomo che appartiene alla Terra.”"),
            ], className="blockquote text-center"),
            md=12
        )
    ], className="mb-4"),

    # Footer
    html.Footer(
    dbc.Container([
        html.Small("Eurix Srl © 2025", className="text-white")
    ], className="text-center"),
    style={"backgroundColor": "#005f73", "padding": "10px"})
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
            # normalizza dai nomi GeoJSON a quelli del DB
            if clicked_loc in geojson_to_df_map:
                clicked_loc = geojson_to_df_map[clicked_loc]
            # verifica contro l’elenco del DB
            if clicked_loc in df_regioni["nome"].values:
                selected_region = clicked_loc

   # --------------------------
    # Mappa coropletica (costruita da df_regioni)
    # --------------------------
    df_map = df_regioni.copy()

    # Nome da usare nel GeoJSON (solo VdA e Trentino hanno etichette diverse)
    df_map["geojson_name"] = df_map["nome"].replace({
        "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste",
        "Trentino-Alto Adige": "Trentino-Alto Adige/Südtirol"
    })

    # Evidenzia la regione selezionata
    df_map["sel"] = (df_map["nome"] == selected_region).astype(int)

    fig_map = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        locations="geojson_name",                 # <- usa il nome compatibile col GeoJSON
        featureidkey=f"properties.{prop_name_key}",
        color="sel",
        color_continuous_scale=["#cccccc", "#ff7f0e"],
        range_color=(0, 1),
        mapbox_style="carto-positron",
        center={"lat": 41.9, "lon": 12.5},
        zoom=5.5,
        opacity=0.7
    )

    # Tooltip pulito (niente "geo_region=...")
    fig_map.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                    "Superficie: %{customdata[1]} km²<br>" +
                    "Densità: %{customdata[2]} ab/km²<br>" +
                    "PIL: %{customdata[3]} mln €<extra></extra>",
        customdata=df_map[["nome", "superficie_kmq", "densita_demografica", "pil"]].values
    )

    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)

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

@app.callback(
    Output("contenitore-punto-forza", "children"),
    Input("regione-dropdown", "value")
)
def update_punto_forza(selected_region):
    record = df_assorb[df_assorb["Regione"] == selected_region]
    testo = record["punti_forza"].iloc[0] if not record.empty else None

    if not testo:
        return html.Small("Nessun punto di forza indicato", className="text-muted")

    return html.Div([
        html.H6("💪 Questa regione si distingue per:", className="mt-2"),
        html.Div([
            html.Span(testo, style={"marginLeft": "10px"})
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"})
    ])



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

    colori = {
        "Carbone": "black",
        "Petrolio": "#008080",   # ottanio bluastro
        "Gas": "gray",
        "Rinnovabili": "lightgreen"
    }

    # Grafico a barre orizzontali (una barra per ogni fonte)
    fig = px.bar(
        x=list(valori.values()),   # valori percentuali
        y=list(valori.keys()),     # nomi fonti
        orientation="h",
        text=[f"{v}%" for v in valori.values()],
        labels={"x": "Percentuale (%)", "y": "Fonte"},
        title="Mix energetico (%)"
    )

    # Colori personalizzati
    fig.update_traces(marker_color=[colori[k] for k in valori.keys()], textposition="outside")

    fig.update_layout(
        margin=dict(l=60, r=20, t=40, b=20),
        xaxis=dict(range=[0, 100])  # sempre fino a 100%
    )

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
# AZIONI
# --------------------------
@app.callback(
    Output("azioni-fotovoltaico-val", "children"),
    Output("azioni-fer-val", "children"),
    Output("azioni-auto-val", "children"),
    Output("azioni-risparmio-val", "children"),
    Input("regione-dropdown", "value")
)
def update_azioni(selected_region):
    resp = requests.get(f"{BASE_URL}/azioni").json()
    df_azioni = pd.DataFrame(resp).merge(df_regioni, on="id_regione")
    df_azioni.rename(columns={"nome": "Regione"}, inplace=True)

    record = df_azioni[df_azioni["Regione"] == selected_region]
    if record.empty:
        return "-", "-", "-", "-"

    return (
        f"{record['fotovoltaico_capacita_gw'].iloc[0]} GW",
        f"{record['quota_produzione_fer_pct'].iloc[0]} %",
        f"{record['quota_auto_elettriche_pct'].iloc[0]} %",
        f"{record['risparmi_energetici_mtep_mln'].iloc[0]}"
    )

# --------------------------
# INDUSTRIA
# --------------------------
@app.callback(
    Output("grafico-industria", "figure"),
    Output("titolo-industria", "children"),
    Input("regione-dropdown", "value")
)
def update_industria(selected_region):
    # Recupera dati dall'endpoint /industria
    resp = requests.get(f"{BASE_URL}/industria").json()
    df_ind = pd.DataFrame(resp).merge(df_regioni, on="id_regione")
    df_ind.rename(columns={"nome": "Regione"}, inplace=True)

    record = df_ind[df_ind["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile"), f"Industria della {selected_region}"

    # 🔹 Rescaling: da tCO₂ / mln € → kg CO₂ / €
    emissioni_rescaled = record["emissioni_per_valore_aggiunto_tco2_per_mln_eur"].iloc[0] * 1000
    quota_elettrico = record["quota_elettrico_pct"].iloc[0]

    valori = {
        "Emissioni per valore aggiunto\n(kg CO₂ per €)": emissioni_rescaled,
        "Quota elettrico (%)": quota_elettrico
    }

    colori = ["lightgray", "yellow"]

    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v:.2f}" for v in valori.values()],
        labels={"x": "Indicatore", "y": "Valore"},
        title=""
    )
    fig.update_traces(marker_color=colori, textposition="outside")
    fig.update_layout(
        margin=dict(l=40, r=20, t=20, b=80),
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )

    return fig, f"Industria della {selected_region}"

# --------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
