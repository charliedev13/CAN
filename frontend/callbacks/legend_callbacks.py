"""
Callback legenda – apertura/chiusura della legenda
(riquadro fisso desktop + offcanvas mobile).
"""
from dash import Input, Output, State, ctx, no_update, clientside_callback, ClientsideFunction
from ..app import app


# 🔹 Pannello fisso desktop:
#   - inizialmente visibile
#   - X lo chiude
#   - click su "Legenda" nel footer lo apre/chiude (toggle)
@app.callback(
    Output("legend-panel", "style"),
    Input("legend-close", "n_clicks"),
    Input("legend-footer-link", "n_clicks"),
    State("legend-panel", "style"),
    prevent_initial_call=False,
)
def toggle_legend_desktop(n_close, n_footer, current_style):
    # Primo caricamento: pannello visibile
    if ctx.triggered_id is None:
        return {"display": "block"}
    
    # Hanno cliccato la X → chiudi il pannello
    if ctx.triggered_id == "legend-close":
        return {"display": "none"}
    
    # Hanno cliccato "Legenda" nel footer → toggle
    if ctx.triggered_id == "legend-footer-link":
        # Se il pannello è nascosto o non ha stile, mostralo
        if not current_style or current_style.get("display") == "none":
            return {"display": "block"}
        # Altrimenti nascondilo
        else:
            return {"display": "none"}
    
    return no_update

# 🔹 Usa clientside callback per verificare la larghezza dello schermo
# e aprire l'offcanvas SOLO su mobile (larghezza < 992px)
app.clientside_callback(
    """
    function(n_clicks, is_open) {
        if (!n_clicks) {
            return false;
        }
        
        // Apri l'offcanvas SOLO se lo schermo è minore di 992px (mobile/tablet)
        if (window.innerWidth < 992) {
            return !is_open;
        }
        
        // Su desktop non fare nulla con l'offcanvas
        return is_open;
    }
    """,
    Output("legend-offcanvas", "is_open"),
    Input("legend-footer-link", "n_clicks"),
    State("legend-offcanvas", "is_open"),
    prevent_initial_call=True,
)