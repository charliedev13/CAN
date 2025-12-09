"""
Modulo edifici_callbacks – Gestisce il grafico sui consumi e le emissioni
degli edifici per la regione selezionata.
"""
import plotly.express as px
from dash import Input, Output
from ..app import app
from ..api import get_edifici


@app.callback(
    Output("grafico-edifici", "figure"),
    Input("regione-dropdown", "value")
)
def update_edifici(selected_region):
    """
    Aggiorna il grafico a barre della sezione 'Edifici' in base alla regione selezionata.

    Args:
        selected_region (str): Nome della regione scelta.

    Returns:
        plotly.graph_objs.Figure: Grafico a barre aggiornato.
    """
    df_edifici = get_edifici()
    record = df_edifici[df_edifici["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile")

    valori = {
        "Consumo medio di energia (kWh/m²·anno)": record["consumo_medio_kwh_m2y"].iloc[0],
        "Emissioni di gas serra per abitante (tCO₂/ab)": record["emissioni_procapite_tco2_ab"].iloc[0],
        "Quanta parte dell’energia consumata proviene da elettricità (%)": record["quota_elettrico_pct"].iloc[0],
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
    fig.update_traces(textposition="outside", hoverinfo="none", hovertemplate=None)

    y_max = max(valori.values()) if valori.values() else 0
    fig.update_layout(
        margin={"l": 40, "r": 20, "t": 10, "b": 120},
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=True,
        legend_title_text=None,
        legend={
            "orientation": "v",
            "y": -0.25,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        xaxis={
            "title": "",
            "showticklabels": False,
            "linecolor": "black",
            "linewidth": 1
        },
        yaxis={
            "title": "",
            "linecolor": "black",
            "linewidth": 1,
            "range": [0, y_max * 1.25]
        },
        font={"size": 13}
    )

    fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)
    return fig