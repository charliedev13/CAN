"""
Modulo industria_callbacks – Gestisce la sezione INDUSTRIA.

Contiene la logica per aggiornare il grafico delle emissioni e del consumo
energetico industriale in base alla regione selezionata.

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
import plotly.express as px
from dash import Input, Output
from ..app import app
from ..api import get_industria
from ..data_utils import df_regioni


@app.callback(
    Output("grafico-industria", "figure"),
    Output("titolo-industria", "children"),
    Input("regione-dropdown", "value")
)
def update_industria(selected_region):
    """
    Aggiorna il grafico INDUSTRIA e il titolo in base alla regione selezionata.

    Args:
        selected_region (str): Nome della regione.

    Returns:
        tuple: Figure aggiornata e titolo stringa.
    """
    df_ind = get_industria().merge(df_regioni, on="id_regione")
    df_ind.rename(columns={"nome": "Regione"}, inplace=True)

    record = df_ind[df_ind["Regione"] == selected_region]
    if record.empty:
        return px.bar(title="Nessun dato disponibile"), "Emissioni e consumo energetico dell’industria"

    emissioni_rescaled = record["emissioni_per_valore_aggiunto_tco2_per_mln_eur"].iloc[0] * 1000
    quota_elettrico = record["quota_elettrico_pct"].iloc[0]

    valori = {
        "Emissioni per valore aggiunto (kg CO₂ per €)": emissioni_rescaled,
        "Quota di energia elettrica sul totale dei consumi (%)": quota_elettrico
    }
    colori = ["#7B4A20", "#F2AE2E"]

    fig = px.bar(
        x=list(valori.keys()),
        y=list(valori.values()),
        text=[f"{v:.2f}" for v in valori.values()],
        color=list(valori.keys()),
        color_discrete_sequence=colori
    )
    fig.update_traces(textposition="outside", hoverinfo="none", hovertemplate=None)

    y_max = max(valori.values()) if valori.values() else 0
    fig.update_layout(
        margin=dict(l=40, r=20, t=10, b=120),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=True,
        legend_title_text=None,
        legend=dict(orientation="v", y=-0.25, x=0.5, xanchor="center", yanchor="top"),
        xaxis=dict(title="", showticklabels=False, linecolor="black", linewidth=1),
        yaxis=dict(title="", linecolor="black", linewidth=1, range=[0, y_max * 1.2]),
        font=dict(size=13)
    )
    fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)
    return fig, "Emissioni e consumo energetico dell’industria"