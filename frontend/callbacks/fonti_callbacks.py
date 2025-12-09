"""
Modulo fonti_callbacks – Gestisce la sezione 'Fonti' (mix energetico regionale).

Visualizza la distribuzione percentuale delle fonti energetiche
(carbone, petrolio, gas e rinnovabili) per la regione selezionata.
"""
import plotly.express as px
from dash import Input, Output
from ..app import app
from ..api import get_mix
from ..data_utils import df_regioni


@app.callback(
    Output("grafico-mix", "figure"),
    Input("regione-dropdown", "value")
)
def update_mix(selected_region):
    """
    Aggiorna il grafico a barre orizzontali del mix energetico
    per la regione selezionata.

    Args:
        selected_region (str): Nome della regione selezionata.

    Returns:
        plotly.graph_objs.Figure: Grafico a barre orizzontali.
    """
    df_mix = get_mix().merge(df_regioni, on="id_regione")
    df_mix.rename(columns={"nome": "Regione"}, inplace=True)

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

    # 🔹 Grafico a barre orizzontali
    fig = px.bar(
        x=list(valori.values()),
        y=list(valori.keys()),
        orientation="h",
        text=[f"{v:.1f}%" for v in valori.values()],
        color=list(valori.keys()),
        color_discrete_map=colori
    )

    fig.update_traces(
        textposition="outside",
        hoverinfo="none",
        hovertemplate=None
    )

    fig.update_layout(
    margin={"l": 40, "r": 20, "t": 10, "b": 40},

    xaxis={
        "range": [0, 100],
        "title": None,
        "showgrid": False,
        "zeroline": False,
        "linecolor": "black",
        "linewidth": 1
    },

    yaxis={
        "title": None,
        "showgrid": False,
        "zeroline": False,
        "linecolor": "black",
        "linewidth": 1
    },

    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,

    font={"size": 13}
)

    return fig