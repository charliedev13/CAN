"""
Modulo mappa_callbacks – Gestisce la mappa interattiva e i grafici di morfologia.

Include:
- la selezione della regione tramite click o dropdown
- la visualizzazione della mappa coropletica
- i grafici a torta per altimetria e uso del suolo

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.1.0
"""

import plotly.express as px
from dash import Input, Output, ctx
from ..app import app
from ..api import *
from ..data_utils import geojson, prop_name_key, df_regioni, df_long, geojson_to_df_map


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
def update_all(drop_val, click_data):
    """
    Aggiorna la mappa e i grafici a torta quando cambia la regione selezionata.
    """
    selected_region = drop_val
    trigger = ctx.triggered_id

    # --- Click su mappa: aggiorna la selezione ---
    if trigger == "italia-map" and click_data:
        pts = click_data.get("points")
        if pts and len(pts) > 0:
            clicked_loc = pts[0].get("location") or pts[0].get("hovertext")
            if clicked_loc in geojson_to_df_map:
                clicked_loc = geojson_to_df_map[clicked_loc]
            if clicked_loc in df_regioni["nome"].values:
                selected_region = clicked_loc

    # --- Mappa coropletica ---
    df_map = df_regioni.copy()
    df_map["geojson_name"] = df_map["nome"].replace({
        "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste",
        "Trentino-Alto Adige": "Trentino-Alto Adige/Südtirol"
    })
    df_map["sel"] = (df_map["nome"] == selected_region).astype(int)

    fig_map = px.choropleth_map(
        df_map,
        geojson=geojson,
        locations="geojson_name",
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
        hoverlabel={
            "bgcolor" : "#faf9f7", 
            "font_size" : 14,
            "font_family" : "Inter, Arial, sans-serif",
            "font_color" : "#005F73",
            "bordercolor" : "#ffffff", 
        },
        customdata=df_map[["nome", "superficie_kmq", "densita_demografica", "pil"]].values
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
    textinfo="percent",
    textfont_size=12,
    pull=0,
    marker={"line": {"color": "#ffffff", "width": 1}},   # ✔ literal
    hoverinfo="none",
    hovertemplate=None
    )

    fig_altimetrica.update_layout(
        margin={"t": 40, "b": 50, "l": 10, "r": 10},

        legend={
            "orientation": "h",    # 🔹 legenda orizzontale
            "y": -0.2,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "title_text": None
        },

        legend_traceorder="normal",
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        autosize=False,
        height=400,
        width=400
    )


    fig_altimetrica.update_layout(title_font={"size" : 22, "color" : "#005F73", "family" : "Inter, sans-serif"})
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
        marker={"line" : {"color" : "#ffffff", "width" : 1}},
        hoverinfo="none",
        hovertemplate=None
    )

    fig_uso.update_layout(
        margin={"t" : 40, "b" : 50, "l" : 10, "r" : 10},
        legend={
            "orientation" : "h",   # 🔹 legenda orizzontale
            "y" : -0.2,
            "x" : 0.5,
            "xanchor" : "center",
            "yanchor" : "top",
            "title_text" : None
        },
        legend_traceorder="normal",
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        autosize=False,
        height=400,
        width=400
    )

    fig_uso.update_layout(title_font={"size" : 22, "color" : "#005F73", "family" : "Inter, sans-serif"})
    fig_uso.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

    titolo_alt = f"Altimetria del suolo in {selected_region}"
    titolo_uso = f"Uso del suolo in {selected_region}"

    return fig_map, fig_altimetrica, fig_uso, selected_region, titolo_alt, titolo_uso