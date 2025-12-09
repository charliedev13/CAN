"""
Modulo footer – Sezione finale della dashboard con citazione e credits.
"""
from dash import html
import dash_bootstrap_components as dbc


def legend_content():
    """Contenuto testuale della legenda (riutilizzato desktop + mobile)."""
    return html.Dl(
        className="legend-list",
        children=[
            html.Dt("PIL"),
            html.Dd("Prodotto Interno Lordo. È la ricchezza di un Paese, o in questo caso di una regione. Rappresenta il valore totale di tutti i beni e servizi finali prodotti al suo interno in un anno."),

            html.Dt("ab/km₂"),
            html.Dd("Numero di abitanti in un kilometro quadrato."),

            html.Dt("Pro capite"),
            html.Dd("Valore riferito a un singolo abitante."),

            html.Dt("tCO₂"),
            html.Dd("Tonnellate di anidride carbonica, cioè emissioni."),

            html.Dt("Assorbimenti"),
            html.Dd("Compensazione delle emissioni di CO₂. Rimozione dell'anidride carbonica dall'atmosfera e suo stoccaggio, sia tramite metodi naturali (es. foreste) sia artificiali (es. tecnologie di cattura)."),

            html.Dt("Mtep"),
            html.Dd("Milioni di tonnellate di petrolio risparmiate grazie all'impiego di una quantità di energia rinnovabile equivalente."),

            html.Dt("Kilowattora (kWh)"),
            html.Dd("Quantitativo d'energia erogato in un'ora dal contatore."),

            html.Dt("Classe A"),
            html.Dd("Immobile ad altissima efficienza energetica, caratterizzato da bassi consumi e minimo impatto ambientale. Le sue principali caratteristiche includono un elevato isolamento termico, impianti di riscaldamento e raffrescamento efficienti, e l'uso di fonti di energia rinnovabile."),
        
            html.Dt("Gigawatt (GW)"),
            html.Dd("Indica la potenza elettrica, pari a un miliardo di Watt."),

            html.Dt("CO₂ per €"),
            html.Dd("Emissioni di CO₂ per euro prodotto: indica quanta CO₂ viene emessa per ogni euro generato dal settore industriale, come misura dell’efficienza produttiva."),

            html.Dt("nan"),
            html.Dd("I dati non sono attualmente disponibili per questa specifica area geografica."),
        ],
    )


# 🔹 Pannello legenda fisso in basso a sinistra (desktop)
legend_panel_desktop = html.Div(
    id="legend-panel",
    className="legend-panel",
    children=[
        html.Div(
            className="legend-header",
            children=[
                html.Span("Legenda", className="legend-title"),
                html.Button(
                    "×",
                    id="legend-close",
                    n_clicks=0,
                    className="legend-close",
                ),
            ],
        ),
        legend_content(),
    ],
)

# 🔹 Legenda mobile in offcanvas (aperta da “Legenda” nel footer)
legend_offcanvas_mobile = dbc.Offcanvas(
    id="legend-offcanvas",
    title="Legenda",
    placement="bottom",
    is_open=False,
    children=legend_content(),
)


# 🔹 Layout del footer (citazione + barra in fondo)
layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Blockquote(
                        [
                            html.P(
                                "“La Terra non appartiene all’uomo, è l’uomo che appartiene alla Terra.”",
                                style={"color": "#005F73"},
                            )
                        ],
                        className="blockquote text-center",
                    ),
                    md=12,
                )
            ],
            className="mb-4",
        ),
        html.Footer(
            dbc.Container(
                [
                    html.Small(
                        "Dati ISTAT e ISPRA · Team CAN, 2025",
                        className="text-white",
                    ),
                    html.Span(" · ", className="text-white"),
                    html.Button(
                        "Legenda",
                        id="legend-footer-link",
                        n_clicks=0,
                        className="footer-link text-white fw-bold",
                        style={
                            "background": "none",
                            "border": "none",
                            "padding": "15px",
                            "cursor": "pointer",
                            "textDecoration": "underline",
                        },
                    ),
                ],
                className="text-center py-2",
            ),
            style={"backgroundColor": "#005f73", "padding": "10px"},
        ),
    ]
)
