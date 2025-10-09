fig_map.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>" +
                  "<span style='opacity:0.8;'>Superficie:</span> %{customdata[1]:,.2f} km²<br>" +
                  "<span style='opacity:0.8;'>Densità:</span> %{customdata[2]} ab/km²<br>" +
                  "<span style='opacity:0.8;'>PIL:</span> %{customdata[3]} mln €<extra></extra>",

    hoverlabel=dict(
        bgcolor="rgba(255, 255, 255, 0.9)",   # bianco semitrasparente
        bordercolor="rgba(240,240,240,0.8)", # bordo chiarissimo, effetto vetro
        font=dict(
            color="#005f73",                  
            family="SF Pro Display, -apple-system, BlinkMacSystemFont, Arial, sans-serif",
            size=14
        ),
        namelength=0
    )
)

# effetto “floating” da iOS/macOS (aggiungendo ombra tramite layout)
fig_map.update_layout(
    hovermode="closest",
    paper_bgcolor="rgba(255,255,255,0)", 
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="SF Pro Display, -apple-system, sans-serif"),
    hoverlabel=dict(
        font_size=15,
        align="left",
    )
)
