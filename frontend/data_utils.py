"""
Modulo data_utils – Contiene i dati condivisi e funzioni di supporto
per le callback della CAN Dashboard.

Autori: Eurix Srl - Team CAN – Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
Versione: 1.0.0
"""
import json
import pandas as pd
import requests
import os

BASE_URL = "http://localhost:8000"

# Percorso sicuro per il geojson
geojson_path = os.path.join(os.path.dirname(__file__), "limits_IT_regions.geojson")
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson = json.load(f)
prop_name_key = "reg_name"

# =========================
# 1️⃣ CARICAMENTO REGIONI
# =========================
regioni_resp = requests.get(f"{BASE_URL}/regioni").json()
df_regioni = pd.DataFrame(regioni_resp)

# =========================
# 2️⃣ MORFOLOGIA E ASSORBIMENTI
# =========================
morf_resp = requests.get(f"{BASE_URL}/morfologia").json()
assorb_resp = requests.get(f"{BASE_URL}/assorbimenti").json()

df_morf = pd.DataFrame(morf_resp).merge(df_regioni, on="id_regione", how="left")
df_morf.rename(columns={"nome": "Regione"}, inplace=True)

df_assorb = pd.DataFrame(assorb_resp).merge(df_regioni, on="id_regione", how="left")
df_assorb.rename(columns={"nome": "Regione"}, inplace=True)

# Conversione morfologia in formato long
df_morf["geo_region"] = df_morf["Regione"]
exclude_cols = ["id_regione", "Regione", "geo_region", "superficie_kmq", "densita_demografica", "pil"]
df_long = df_morf.melt(
    id_vars=["id_regione", "Regione", "geo_region"],
    value_vars=[c for c in df_morf.columns if c not in exclude_cols],
    var_name="Morfologia",
    value_name="Percentuale"
)

geojson_to_df_map = {
    "Trentino-Alto Adige": "Trentino-Alto Adige",
    "Trentino-Alto Adige/Südtirol": "Trentino-Alto Adige",
    "Provincia di Trento": "Trentino-Alto Adige",
    "Provincia di Bolzano": "Trentino-Alto Adige",
    "Valle d'Aosta/Vallée d'Aoste": "Valle d'Aosta"
}

# =========================
# 3️⃣ EMISSIONI TOTALI
# =========================
try:
    emiss_resp = requests.get(f"{BASE_URL}/emissioni").json()
    df_emissioni = pd.DataFrame(emiss_resp)

    if not df_emissioni.empty:
        df_emissioni = df_emissioni.merge(
            df_regioni[["id_regione", "nome"]],
            on="id_regione",
            how="left"
        )
        df_emissioni.rename(columns={
            "nome": "Regione",
            "co2eq_mln_t": "emissioni_totali_mln_t"
        }, inplace=True)
    else:
        print("[API] Nessun dato emissioni ricevuto")
        df_emissioni = pd.DataFrame(columns=["id_regione", "Regione", "emissioni_totali_mln_t"])

except Exception as e:
    print(f"[API] Errore caricando emissioni totali: {e}")
    df_emissioni = pd.DataFrame(columns=["id_regione", "Regione", "emissioni_totali_mln_t"])