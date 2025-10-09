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
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
import os
import time
import threading

# --------------------------
# CONFIG
# --------------------------
BASE_URL = "http://localhost:8000"
with open("limits_IT_regions.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)
prop_name_key = "reg_name"

# Caricamento chiave API meteo
load_dotenv("meteo.env")  # carica variabili dal file meteo.env
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

meteo_lock = threading.Lock()

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
dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("CAN", className="text-white fw-bold me-5"),

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
    color="#005f73", dark=True, className="mb-3"
    ),

    # Sezione Mappa + Dropdown
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Cambiamento Ambientale Nazionale", className="text-center mb-2", style={"marginTop": "30px"}),
                html.H6("Scegli una regione di cui vedere i dati", className="text-center subhead mb-4", style={"fontSize": "1.2rem", "fontWeight": "500"}),
                dcc.Dropdown(
                    id="regione-dropdown",
                    options=[{"label": r, "value": r} for r in regioni],
                    value=regioni[0],
                    clearable=False,
                    style={"width": "60%", "margin": "0 auto"}
                ),
                html.Div(id="meteo-regionale", className="text-center mt-3"),
                dcc.Graph(id="italia-map", style={"height": "500px"}, config={"scrollZoom":False}) #blocca zoom allo scroll
            ])
        , md=12)
    ], className="mb-4", id="mappa"),

    # Sezione meteo regionale
    dbc.Row([
    dbc.Col(
        html.Div(id="meteo-container"),
        md=12
    )
], className="mb-4"),

    # Sezione Grafici a torta morfologia
    dbc.Row([
    # Colonna Altimetria
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H4(id="titolo-altimetria", className="text-center mb-3 fw-bold", style={"color": "#005F73"}),
            dcc.Graph(id="grafico-altimetria", style={"height": "400px"})
        ])),
        md=6
    ),

    # Colonna Uso del suolo
    dbc.Col(
        dbc.Card(dbc.CardBody([
            html.H4(id="titolo-uso", className="text-center mb-3 fw-bold", style={"color": "#005F73"}),
            dcc.Graph(id="grafico-uso", style={"height": "400px"})
        ])),
        md=6
    )
], className="mb-4 justify-content-center align-items-stretch", id="suolo"),

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
                html.H5("Fonti energetiche utilizzate dalla regione"),
                dcc.Graph(id="grafico-mix", style={"height": "300px"})
            ])), md=12
        )
    ], className="mb-4", id="fonti"),

    # Sezione Edifici
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("Consumi e sostenibilità degli edifici"),
                dcc.Graph(id="grafico-edifici", style={"height": "400px"})
            ])), md=12
        )
    ], className="mb-4", id="edifici"),

        # Sezione Azioni
    html.Div([
        html.H4("Cosa sta facendo la regione per l’ambiente", className="text-center mb-4 fw-bold"),
        
        dbc.Row([
            # Fotovoltaico
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.Div(
                        html.Img(src="/assets/pannello.png", style={"width": "60%"}),
                        className="azioni-img"
                    ),
                    html.H5("Impianti solari attivi", className="text-center subhead"),
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
                    html.H5("Energia rinnovabile prodotta", className="text-center subhead"),
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
                    html.H5("Auto elettriche in circolazione", className="text-center subhead"),
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
                    html.H5("Energia risparmiata", className="text-center subhead"),
                    html.Div(id="azioni-risparmio-val", className="azioni-val text-center")
                ])), md=3
            )
        ], className="mb-4 justify-content-center")
    ], className="mb-4", id="azioni"),

    # Sezione Industria
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5(id="titolo-industria", className="mb-3"),
                dcc.Graph(id="grafico-industria", style={"height": "350px"})
            ])), md=12
        )
    ], className="mb-4", id="industria"),

    # Sezione Comparazione
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H4("Ora scegli tu: compara un dato di tua preferenza", className="text-center mb-2"),
                html.H6("Scegli le due regioni e la categoria", className="text-center mb-4"),

                # 3 Dropdowns
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id="dropdown-regione-1",
                            options=[{"label": r, "value": r} for r in sorted(regioni)],
                            value="Abruzzo",
                            clearable=False
                        ), md=4
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="dropdown-regione-2",
                            options=[{"label": r, "value": r} for r in sorted(regioni) if r != "Abruzzo"],
                            value="Basilicata",
                            clearable=False
                        ), md=4
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="dropdown-categoria",
                            options=[],
                            placeholder="Seleziona una categoria",
                            clearable=False
                        ), md=4
                    )
                ], className="mb-4"),

                # Grafico comparazione
                dcc.Graph(id="grafico-comparazione", style={"height": "400px"})
            ])
        , md=12)
    ], className="mb-4", id="confronta tu"),

    # Sezione frase d'effetto
    dbc.Row([
        dbc.Col(
            html.Blockquote([
                html.P("“La Terra non appartiene all’uomo, è l’uomo che appartiene alla Terra.”", style={"color": "#005F73"}),
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
    Output("titolo-altimetria", "children"),
    Output("titolo-uso", "children"),
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

    fig_map = px.choropleth_map(
        df_map,
        geojson=geojson,
        locations="geojson_name",                 # <- usa il nome compatibile col GeoJSON
        featureidkey=f"properties.{prop_name_key}",
        color="sel",
        color_continuous_scale=["#F2AE2E", "#F27329"],
        range_color=(0, 1),
        map_style="carto-positron",
        center={"lat": 41.9, "lon": 12.5},
        zoom=4.5,
        opacity=0.7
    )

    # Tooltip
    fig_map.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                    "Superficie: %{customdata[1]} km²<br>" +
                    "Densità: %{customdata[2]} ab/km²<br>" +
                    "PIL: %{customdata[3]} mln €<extra></extra>",
        hoverlabel=dict(
            bgcolor="#faf9f7", 
            font_size=14,
            font_family="Inter, Arial, sans-serif",
            font_color="#005F73",
            bordercolor="#ffffff", 
        ),
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
    morf_altimetrica = morf_altimetrica[morf_altimetrica["Percentuale"] > 0]

    morf_altimetrica["Morfologia"] = morf_altimetrica["Morfologia"].map({
        "pianura_pct": "Pianura",
        "collina_pct": "Collina",
        "montagna_pct": "Montagna"
    })

    fig_altimetrica = px.pie(
        morf_altimetrica,
        names="Morfologia",
        values="Percentuale",
        title=None,
        color="Morfologia",
        color_discrete_map={
        "Pianura": "#F27329",   # arancio caldo
        "Collina": "#F29727",   # giallo oro
        "Montagna": "#7B4A20"   # rosso autunno
        },
        hole=0
    )

    fig_altimetrica.update_traces(
        textposition="outside",
        textinfo="percent",  # 🔹 solo percentuali
        textfont_size=12,
        pull=0,
        marker=dict(line=dict(color="#ffffff", width=1)),
        hoverinfo="none",
        hovertemplate=None
    )

    fig_altimetrica.update_layout(
        margin=dict(t=40, b=50, l=10, r=10),
        legend=dict(
            orientation="h",   # 🔹 legenda orizzontale
            y=-0.2,
            x=0.5,
            xanchor="center",
            yanchor="top",
            title_text=None
        ),
        legend_traceorder="normal",
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        autosize=False,
        height=400,
        width=400
    )

    fig_altimetrica.update_layout(title_font=dict(size=22, color="#005F73", family="Inter, sans-serif"))
    fig_altimetrica.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

    # --- Grafico 2: Agricolo, Urbano, Forestale ---
    morf_uso = dati_regione[dati_regione["Morfologia"].isin(
        ["agricolo_pct", "urbano_pct", "forestale_pct"]
    )].copy()
    morf_uso = morf_uso[morf_uso["Percentuale"] > 0]

    morf_uso["Morfologia"] = morf_uso["Morfologia"].map({
        "agricolo_pct": "Agricolo",
        "urbano_pct": "Urbano",
        "forestale_pct": "Forestale"
    })

    fig_uso = px.pie(
        morf_uso,
        names="Morfologia",
        values="Percentuale",
        title=None,
        color="Morfologia",
        color_discrete_map={
        "Agricolo": "#F2AE2E",   # giallo oro
        "Forestale": "#587823",  # verde oliva
        "Urbano": "#855771"      # malva
        },
        hole=0
    )

    fig_uso.update_traces(
        textposition="outside",
        textinfo="percent",  # 🔹 solo percentuali
        textfont_size=12,
        pull=0,
        marker=dict(line=dict(color="#ffffff", width=1)),
        hoverinfo="none",
        hovertemplate=None
    )

    fig_uso.update_layout(
        margin=dict(t=40, b=50, l=10, r=10),
        legend=dict(
            orientation="h",   # 🔹 legenda orizzontale
            y=-0.2,
            x=0.5,
            xanchor="center",
            yanchor="top",
            title_text=None
        ),
        legend_traceorder="normal",
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        autosize=False,
        height=400,
        width=400
    )

    fig_uso.update_layout(title_font=dict(size=22, color="#005F73", family="Inter, sans-serif"))
    fig_uso.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)
    titolo_alt = f"Altimetria del suolo in {selected_region}"
    titolo_uso = f"Uso del suolo in {selected_region}"
    return fig_map, fig_altimetrica, fig_uso, selected_region, titolo_alt, titolo_uso


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
        "Carbone": "#1C1C1C",
        "Petrolio": "#61A1BC",   # ottanio
        "Gas": "#855771",
        "Rinnovabili": "#587823"
    }

    # 🔹 Grafico a barre orizzontali (senza titolo interno)
    fig = px.bar(
        x=list(valori.values()),
        y=list(valori.keys()),
        orientation="h",
        text=[f"{v:.1f}%" for v in valori.values()],
        color=list(valori.keys()),
        color_discrete_map=colori
    )

    # 🔹 Impostazioni estetiche
    fig.update_traces(
        textposition="outside",
        hoverinfo="none",
        hovertemplate=None
    )

    fig.update_layout(
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(
            range=[0, 100],
            title="Percentuale (%)",
            showgrid=False,
            zeroline=False,
            linecolor="black",   # 🔹 bordo asse nero
            linewidth=1
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            linecolor="black",   # 🔹 bordo asse nero
            linewidth=1
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        font=dict(size=13)
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
        "Consumo medio di energia (kWh/m²·anno)": record["consumo_medio_kwh_m2y"].iloc[0],
        "Emissioni di gas serra per abitante (tCO₂/ab)": record["emissioni_procapite_tco2_ab"].iloc[0],
        "Uso di energia elettrica sugli edifici (%)": record["quota_elettrico_pct"].iloc[0],
        "Edifici ad alta efficienza (Classe A) (%)": record["quota_ape_classe_a_pct"].iloc[0]
    }

    colori = ["#D93223", "#855771", "#F2AE2E", "#587823"]
    
    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v}" for v in valori.values()],
        color=list(valori.keys()),
        color_discrete_sequence=colori
    )

    fig.update_traces(
        textposition="outside",
        hoverinfo="none",
        hovertemplate=None
    )

    y_max = max(valori.values()) if valori.values() else 0
    y_range = [0, y_max * 1.25]  # piccolo zoom-out

    fig.update_layout(
        margin=dict(l=40, r=20, t=10, b=120),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=True,                 # 🔹 attiva la legenda
        legend=dict(
            orientation="v",             # verticale
            y=-0.25,                      # posizione sotto il grafico
            x=0.5,
            xanchor="center",
            yanchor="top",
            title_text=None,
            itemwidth=30,                # spazio per il quadratino
            itemsizing="constant"        # quadratini uniformi
        ),
        xaxis=dict(
            title="", showticklabels=False,  # 🔹 nasconde le etichette asse X
            linecolor="black", linewidth=1, showgrid=False, zeroline=False
        ),
        yaxis=dict(
            title="",
            linecolor="black", linewidth=1, showgrid=False, zeroline=False,
            range=y_range
        ),
        font=dict(size=13)
    )
    fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)
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
        f"{record['risparmi_energetici_mtep_mln'].iloc[0]} Mtep"
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
    resp = requests.get(f"{BASE_URL}/industria").json()
    df_ind = pd.DataFrame(resp).merge(df_regioni, on="id_regione")
    df_ind.rename(columns={"nome": "Regione"}, inplace=True)

    record = df_ind[df_ind["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile"), f"Emissioni e consumo energetico dell’industria"

    emissioni_rescaled = record["emissioni_per_valore_aggiunto_tco2_per_mln_eur"].iloc[0] * 1000
    quota_elettrico = record["quota_elettrico_pct"].iloc[0]

    valori = {
        "Emissioni per valore aggiunto (kg CO₂ per €)": emissioni_rescaled,
        "Quota elettrico (%)": quota_elettrico
    }

    colori = ["#7B4A20", "#F2AE2E"]

    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v:.2f}" for v in valori.values()],
        color=list(valori.keys()),
        color_discrete_sequence=colori
    )

    fig.update_traces(
        textposition="outside",
        hoverinfo="none",
        hovertemplate=None
    )

    y_max = max(valori.values()) if valori.values() else 0
    y_range = [0, y_max * 1.2]

    fig.update_layout(
        margin=dict(l=40, r=20, t=10, b=120),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(
            orientation="v",
            y=-0.25,
            x=0.5,
            xanchor="center",
            yanchor="top",
            title_text=None,
            itemwidth=30,
            itemsizing="constant"
        ),
        xaxis=dict(
            title="", showticklabels=False,
            linecolor="black", linewidth=1, showgrid=False, zeroline=False
        ),
        yaxis=dict(
            title="",
            linecolor="black", linewidth=1, showgrid=False, zeroline=False,
            range=y_range
        ),
        font=dict(size=13)
    )
    fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)
    return fig, f"Emissioni e consumo energetico dell’industria"

# --------------------------
# dropdown e grafico comparazione
# --------------------------

# 1️⃣ Dropdown sinistro e destro si escludono a vicenda
@app.callback(
    Output("dropdown-regione-2", "options"),
    Input("dropdown-regione-1", "value")
)
def aggiorna_opzioni_regione2(selected_left):
    return [{"label": r, "value": r} for r in sorted(regioni) if r != selected_left]


@app.callback(
    Output("dropdown-regione-1", "options"),
    Input("dropdown-regione-2", "value")
)
def aggiorna_opzioni_regione1(selected_right):
    return [{"label": r, "value": r} for r in sorted(regioni) if r != selected_right]

# 2️⃣ Dropdown categorie (estrae tutti i campi numerici da tutte le tabelle tranne "assorbimenti")
# Popola le categorie numeriche per la comparazione
@app.callback(
    Output("dropdown-categoria", "options"),
    Input("dropdown-categoria", "id")
)
def popola_categorie(_):
    # Campi numerici dalle tabelle utili (escluso "assorbimenti")
    categorie = {
        # Tabella REGIONI
        "superficie_kmq": "Superficie (km²)",
        "densita_demografica": "Densità demografica (ab/km²)",
        "pil": "PIL pro capite (mln €)",

        # Tabella MIX
        "carbone_pct": "Carbone (%)",
        "petrolio_pct": "Petrolio (%)",
        "gas_pct": "Gas (%)",
        "rinnovabili_pct": "Rinnovabili (%)",

        # Tabella EDIFICI
        "consumo_medio_kwh_m2y": "Consumo medio edifici (kWh/m²·anno)",
        "emissioni_procapite_tco2_ab": "Emissioni pro capite (tCO₂/ab)",
        "quota_elettrico_pct": "Quota elettrico edifici (%)",
        "quota_ape_classe_a_pct": "Edifici in Classe A (%)",

        # Tabella INDUSTRIA
        "emissioni_per_valore_aggiunto_tco2_per_mln_eur": "Emissioni industriali (tCO₂ per mln €)",
        "quota_elettrico_pct_industria": "Quota elettrico industria (%)",

        # Tabella MORFOLOGIA
        "pianura_pct": "Aree pianeggianti (%)",
        "collina_pct": "Aree collinari (%)",
        "montagna_pct": "Aree montuose (%)",
        "agricolo_pct": "Aree agricole (%)",
        "urbano_pct": "Aree urbane (%)",
        "forestale_pct": "Aree forestali (%)"
    }

    return [{"label": v, "value": k} for k, v in categorie.items()]

# 3️⃣ Grafico comparativo
@app.callback(
    Output("grafico-comparazione", "figure"),
    Input("dropdown-regione-1", "value"),
    Input("dropdown-regione-2", "value"),
    Input("dropdown-categoria", "value")
)
def update_confronto(regione1, regione2, categoria):
    if not (regione1 and regione2 and categoria):
        return px.bar()

    # Mappa endpoint per ogni categoria
    endpoint_map = {
        "superficie_kmq": "regioni",
        "densita_demografica": "regioni",
        "pil": "regioni",
        "carbone_pct": "mix",
        "petrolio_pct": "mix",
        "gas_pct": "mix",
        "rinnovabili_pct": "mix",
        "consumo_medio_kwh_m2y": "edifici",
        "emissioni_procapite_tco2_ab": "edifici",
        "quota_elettrico_pct": "edifici",
        "quota_ape_classe_a_pct": "edifici",
        "emissioni_per_valore_aggiunto_tco2_per_mln_eur": "industria",
        "quota_elettrico_pct_industria": "industria",
        "pianura_pct": "morfologia",
        "collina_pct": "morfologia",
        "montagna_pct": "morfologia",
        "agricolo_pct": "morfologia",
        "urbano_pct": "morfologia",
        "forestale_pct": "morfologia",
    }

    endpoint = endpoint_map.get(categoria)
    if not endpoint:
        return px.bar(title="Categoria non supportata")

    # Carico i dati
    try:
        dati = requests.get(f"{BASE_URL}/{endpoint}").json()
        df = pd.DataFrame(dati)
    except Exception as e:
        return px.bar(title=f"Errore nel recupero dati: {e}")

    if df.empty:
        return px.bar(title=f"Nessun dato disponibile in {endpoint}")

    # Gestione campo industria
    if categoria == "quota_elettrico_pct_industria" and "quota_elettrico_pct" in df.columns:
        df["quota_elettrico_pct_industria"] = df["quota_elettrico_pct"]

    # Conversione sicura
    df[categoria] = pd.to_numeric(df[categoria], errors="coerce").fillna(0)

    # Merge con i nomi regione se serve
    if "nome" not in df.columns:
        if "id_regione" not in df.columns:
            return px.bar(title=f"Manca 'id_regione' in {endpoint}")
        df = df.merge(df_regioni[["id_regione", "nome"]], on="id_regione", how="left")

    # Filtro le regioni selezionate
    df_sel = df[df["nome"].isin([regione1, regione2])]
    if df_sel.empty:
        return px.bar(title="Dati non trovati per le regioni selezionate")

    # Calcolo range X per “zoom-out”
    x_max = df_sel[categoria].max()
    x_range = [0, x_max * 1.2]

    # Grafico orizzontale
    fig = px.bar(
        df_sel,
        x=categoria,
        y="nome",
        orientation="h",
        text=df_sel[categoria],
        color="nome",
        color_discrete_sequence=["#00798c", "#61A1BC"]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hoverinfo="none",      # 🔸 disattiva fumetti
        hovertemplate=None
    )

    fig.update_layout(
        margin=dict(l=60, r=30, t=10, b=40),
        plot_bgcolor="white",   # 🔸 sfondo bianco
        paper_bgcolor="white",
        showlegend=False,
        xaxis=dict(
            title="",           # 🔸 nessun titolo asse X
            linecolor="black",
            linewidth=1,
            showgrid=False,
            zeroline=False,
            range=x_range
        ),
        yaxis=dict(
            title="",           # 🔸 nessun titolo asse Y
            linecolor="black",
            linewidth=1,
            showgrid=False,
            zeroline=False
        ),
        font=dict(size=13)
    )

    return fig

# --------------------------
# Navbar hamburger (mobile)
# --------------------------
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open")
)
def toggle_navbar(n, is_open):
    if n:
        return not is_open
    return is_open

# --------------------------
# METEO REGIONALE
# --------------------------
# Mappatura regioni -> città per meteo
REGIONE_TO_CITY = {
    "Piemonte": "Torino",
    "Valle d'Aosta": "Aosta",
    "Lombardia": "Milano",
    "Trentino-Alto Adige": "Trento",
    "Veneto": "Venezia",
    "Friuli-Venezia Giulia": "Trieste",
    "Liguria": "Genova",
    "Emilia-Romagna": "Bologna",
    "Toscana": "Firenze",
    "Umbria": "Perugia",
    "Marche": "Ancona",
    "Lazio": "Roma",
    "Abruzzo": "L'Aquila",
    "Molise": "Campobasso",
    "Campania": "Napoli",
    "Puglia": "Bari",
    "Basilicata": "Potenza",
    "Calabria": "Catanzaro",
    "Sicilia": "Palermo",
    "Sardegna": "Cagliari"
}

# Funzione emoji in base al meteo
def meteo_emoji(description: str):
    d = description.lower()
    
    if "sereno" in d or "clear" in d:
        return "☀️"
    elif "poche nuvole" in d or "nubi sparse" in d or "nuvoloso" in d or "cielo coperto" in d or "cloud" in d:
        return "☁️"
    elif "pioggia" in d or "rain" in d or "rovesci" in d:
        return "🌧️"
    elif "temporale" in d or "storm" in d:
        return "⛈️"
    elif "neve" in d or "snow" in d:
        return "❄️"
    elif "nebbia" in d or "foschia" in d or "fog" in d or "mist" in d:
        return "🌫️"
    elif "vento" in d or "wind" in d:
        return "💨"
    elif "sole" in d and ("nuvole" in d or "cloud" in d):
        return "🌤️"
    else:
        return "🌡️"

# --------------------------
# CACHE METEO SICURA
# --------------------------
meteo_cache = {}
CACHE_TTL = 3600  # 1 ora in secondi

meteo_lock = threading.Lock()

@app.callback(
    Output("meteo-container", "children"),
    Input("regione-dropdown", "value")
)
def update_meteo(selected_region):
    with meteo_lock:
        dati = meteo_cache.get(selected_region, {"temp": "N/A", "desc": "Dati non disponibili", "emoji": "🌡️"})
    temp = dati["temp"]
    desc = dati["desc"]
    emoji = dati["emoji"]

    return html.Div([
        html.H4("Meteo", className="text-center mb-1"),
        html.H5(selected_region, className="text-center subhead mb-2"),
        html.Div([
            html.Span(f"{emoji} ", style={"fontSize": "32px", "marginRight": "10px"}),
            html.Span(f"{temp}°C – {desc.capitalize()}", style={"fontSize": "18px"})
        ], style={"textAlign": "center"})
    ], style={"marginBottom": "20px"})

def aggiorna_cache_meteo():
    """Aggiorna il meteo di tutte le regioni ogni ora."""
    while True:
        now = time.time()
        for region, city in REGIONE_TO_CITY.items():
            try:
                city_url = city.replace(" ", "")
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city_url},IT&units=metric&appid={WEATHER_API_KEY}&lang=it"
                resp = requests.get(url).json()
                temp = resp["main"]["temp"]
                desc = resp["weather"][0]["description"]
                emoji = meteo_emoji(desc)
                with meteo_lock:
                    meteo_cache[region] = {
                        "timestamp": now,
                        "temp": temp,
                        "desc": desc,
                        "emoji": emoji
                    }
                print(f"[API] Cache aggiornata per {region}: {temp}°C, {desc}")
            except Exception as e:
                print(f"[API] Errore aggiornando meteo per {region}: {e}")
        time.sleep(CACHE_TTL)  # 1 ora

# Avvio del thread daemon
threading.Thread(target=aggiorna_cache_meteo, daemon=True).start()

# --------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
