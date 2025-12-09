"""
Modulo azioni_callbacks – Gestisce la sezione AZIONI.

Mostra i valori relativi alle azioni ambientali regionali:
fotovoltaico, FER, auto elettriche e risparmi energetici.
"""
from dash import Input, Output
from ..app import app
from ..api import get_azioni
from ..data_utils import df_regioni


@app.callback(
    Output("azioni-fotovoltaico-val", "children"),
    Output("azioni-fer-val", "children"),
    Output("azioni-auto-val", "children"),
    Output("azioni-risparmio-val", "children"),
    Input("regione-dropdown", "value")
)
def update_azioni(selected_region):
    """
    Aggiorna i valori della sezione AZIONI per la regione selezionata.

    Args:
        selected_region (str): Regione selezionata.

    Returns:
        tuple: 4 stringhe (fotovoltaico, FER, auto elettriche, risparmi energetici)
    """
    df_azioni = get_azioni().merge(df_regioni, on="id_regione")
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