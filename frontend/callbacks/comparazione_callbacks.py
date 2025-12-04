"""
Modulo comparazione_callbacks – Gestisce la sezione di confronto tra regioni.

Permette di:
- aggiornare i dropdown in modo che le due regioni non coincidano
- popolare la lista di categorie confrontabili
- generare il grafico di comparazione orizzontale

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
import plotly.express as px
import pandas as pd
import requests
from dash import Input, Output
from ..app import app
from ..data_utils import df_regioni
from ..api import BASE_URL


# 1️⃣ Dropdown sinistro → aggiorna opzioni del destro
@app.callback(
    Output("dropdown-regione-2", "options"),
    Input("dropdown-regione-1", "value")
)
def aggiorna_opzioni_regione2(selected_left):
    """Esclude la regione sinistra dal menu destro."""
    return [{"label": r, "value": r} for r in sorted(df_regioni["nome"].unique()) if r != selected_left]


# 2️⃣ Dropdown destro → aggiorna opzioni del sinistro
@app.callback(
    Output("dropdown-regione-1", "options"),
    Input("dropdown-regione-2", "value")
)
def aggiorna_opzioni_regione1(selected_right):
    """Esclude la regione destra dal menu sinistro."""
    return [{"label": r, "value": r} for r in sorted(df_regioni["nome"].unique()) if r != selected_right]


# 3️⃣ Popola le categorie confrontabili
@app.callback(
    Output("dropdown-categoria", "options"),
    Input("dropdown-categoria", "id")
)
def popola_categorie(_):
    """Restituisce la lista delle categorie confrontabili."""
    categorie = {
        "superficie_kmq": "Superficie (km²)",
        "densita_demografica": "Densità demografica (ab/km²)",
        "pil": "PIL pro capite (mln €)",
        "carbone_pct": "Carbone (%)",
        "petrolio_pct": "Petrolio (%)",
        "gas_pct": "Gas (%)",
        "rinnovabili_pct": "Rinnovabili (%)",
        "consumo_medio_kwh_m2y": "Consumo medio edifici (kWh/m²·anno)",
        "emissioni_procapite_tco2_ab": "Emissioni pro capite (tCO₂/ab)",
        "quota_elettrico_pct": "Quota elettrico edifici (%)",
        "quota_ape_classe_a_pct": "Edifici in Classe A (%)",
        "emissioni_per_valore_aggiunto_tco2_per_mln_eur": "Emissioni industriali (tCO₂ per mln €)",
        "quota_elettrico_pct_industria": "Quota elettrico industria (%)",
        "pianura_pct": "Aree pianeggianti (%)",
        "collina_pct": "Aree collinari (%)",
        "montagna_pct": "Aree montuose (%)",
        "agricolo_pct": "Aree agricole (%)",
        "urbano_pct": "Aree urbane (%)",
        "forestale_pct": "Aree forestali (%)"
    }
    return [{"label": v, "value": k} for k, v in categorie.items()]


# 4️⃣ Grafico comparativo
@app.callback(
    Output("grafico-comparazione", "figure"),
    Input("dropdown-regione-1", "value"),
    Input("dropdown-regione-2", "value"),
    Input("dropdown-categoria", "value")
)
def update_confronto(regione1, regione2, categoria):
    """
    Aggiorna il grafico di comparazione per le due regioni e la categoria scelta.
    """
    if not (regione1 and regione2 and categoria):
        return px.bar()

    endpoint_map = {
        "superficie_kmq": "regioni", "densita_demografica": "regioni", "pil": "regioni",
        "carbone_pct": "mix", "petrolio_pct": "mix", "gas_pct": "mix", "rinnovabili_pct": "mix",
        "consumo_medio_kwh_m2y": "edifici", "emissioni_procapite_tco2_ab": "edifici",
        "quota_elettrico_pct": "edifici", "quota_ape_classe_a_pct": "edifici",
        "emissioni_per_valore_aggiunto_tco2_per_mln_eur": "industria",
        "quota_elettrico_pct_industria": "industria",
        "pianura_pct": "morfologia", "collina_pct": "morfologia", "montagna_pct": "morfologia",
        "agricolo_pct": "morfologia", "urbano_pct": "morfologia", "forestale_pct": "morfologia"
    }
    endpoint = endpoint_map.get(categoria)
    if not endpoint:
        return px.bar(title="Categoria non supportata")

    # Recupero dati
    try:
        dati = requests.get(f"{BASE_URL}/{endpoint}").json()
        df = pd.DataFrame(dati)
    except Exception as e:
        return px.bar(title=f"Errore nel recupero dati: {e}")

    if df.empty:
        return px.bar(title=f"Nessun dato disponibile per {endpoint}")

    if categoria == "quota_elettrico_pct_industria" and "quota_elettrico_pct" in df.columns:
        df["quota_elettrico_pct_industria"] = df["quota_elettrico_pct"]

    df[categoria] = pd.to_numeric(df[categoria], errors="coerce").fillna(0)
    if "nome" not in df.columns and "id_regione" in df.columns:
        df = df.merge(df_regioni[["id_regione", "nome"]], on="id_regione", how="left")

    df_sel = df[df["nome"].isin([regione1, regione2])]
    if df_sel.empty:
        return px.bar(title="Dati non trovati per le regioni selezionate")

    x_max = df_sel[categoria].max()
    fig = px.bar(
        df_sel,
        x=categoria,
        y="nome",
        orientation="h",
        text=df_sel[categoria],
        color="nome",
        color_discrete_sequence=["#00798c", "#61A1BC"]
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", hoverinfo="none", hovertemplate=None)
    fig.update_layout(
        margin={"l": 60, "r": 30, "t": 10, "b": 40},
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis={"range": [0, x_max * 1.2], "linecolor": "black", "linewidth": 1},
        yaxis={"linecolor": "black", "linewidth": 1},
        xaxis_title=None,
        yaxis_title=None,
        font={"size": 13}
    )

    return fig