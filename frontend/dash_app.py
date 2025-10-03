import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, ctx

# --------------------------
# CARICAMENTO DATI
# --------------------------

# Carico CSV Morfologia del suolo
df = pd.read_csv("Morfologia_del_suolo.csv")

# Pulizia valori numerici
for col in df.columns[1:]:
    df[col] = df[col].replace({',': '.', '~': ''}, regex=True).astype(float)

# Colonna per collegamento con GeoJSON
df["geo_region"] = df["Regione"]

# Trasformo in formato long per grafici
df_long = df.melt(id_vars=["Regione","geo_region"], var_name="Morfologia", value_name="Percentuale")

# Carico GeoJSON delle regioni italiane
with open("limits_IT_regions.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

prop_name_key = "reg_name"  # nome della proprietà nel GeoJSON

# --------------------------
# DASH APP
# --------------------------
app = Dash(__name__)

regioni = df["Regione"].unique()

app.layout = html.Div([
    html.H2("Mappa interattiva Italia - Seleziona Regione"),

    # Dropdown per selezione regione
    dcc.Dropdown(
        id="regione-dropdown",
        options=[{"label": r, "value": r} for r in regioni],
        value="Abruzzo",
        clearable=False,
        style={"width": "50%", "margin": "auto"}
    ),

    # Mappa Italia
    dcc.Graph(id="italia-map", style={"height": "700px"}),

    # Grafico a torta
    dcc.Graph(id="grafico-regionale", style={"height": "500px"})
])

# --------------------------
# CALLBACK
# --------------------------
@app.callback(
    Output("italia-map", "figure"),
    Output("grafico-regionale", "figure"),
    Output("regione-dropdown", "value"),
    Input("regione-dropdown", "value"),
    Input("italia-map", "clickData")
)
def update_all(drop_val, clickData):
    selected_region = drop_val  # default: dropdown

    # Controllo se l'utente ha cliccato sulla mappa
    trigger = ctx.triggered_id
    if trigger == "italia-map" and clickData:
        pts = clickData.get("points")
        if pts and len(pts) > 0:
            clicked_loc = pts[0].get("location") or pts[0].get("hovertext")
            if clicked_loc:
                match = df[df["geo_region"] == clicked_loc]
                if not match.empty:
                    selected_region = match["Regione"].iloc[0]

    # Evidenzio la regione selezionata
    df_map = pd.DataFrame({"geo_region": df["geo_region"].unique()})
    df_map["sel"] = df_map["geo_region"].apply(lambda g: 1 if g == df.loc[df["Regione"]==selected_region, "geo_region"].iloc[0] else 0)

    # Creo mappa con hover dinamico
    fig_map = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        locations="geo_region",
        featureidkey=f"properties.{prop_name_key}",
        color="sel",
        color_continuous_scale=["#cccccc", "#ff7f0e"],
        range_color=(0,1),
        mapbox_style="carto-positron",
        center={"lat":41.8719, "lon":12.5674},
        zoom=5.5,
        opacity=0.7,
        hover_name="geo_region"
    )

    fig_map.update_traces(
        marker_line_width=1,
        marker_line_color="black",
        hovertemplate="<b>%{hovertext}</b><extra></extra>"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)

    # Grafico a torta per la regione selezionata
    dati_regione = df_long[df_long["Regione"] == selected_region]
    fig_chart = px.pie(dati_regione, names="Morfologia", values="Percentuale",
                       title=f"Morfologia del suolo - {selected_region}")

    return fig_map, fig_chart, selected_region

# --------------------------
# RUN
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
