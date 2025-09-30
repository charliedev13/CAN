from model_db import *
import pandas as pd

session = Session()  

# Dizionario per la normalizzazione dei nomi delle regioni
REGIONI_STANDARD = {
    "piemonte": "Piemonte",
    "valle d'aosta": "Valle d'Aosta",
    "val d'aosta": "Valle d'Aosta",
    "lombardia": "Lombardia",
    "trentino alto adige": "Trentino-Alto Adige",
    "trentino-alto adige": "Trentino-Alto Adige",
    "alto adige": "Trentino-Alto Adige",
    "trentino": "Trentino-Alto Adige",
    "veneto": "Veneto",
    "friuli venezia giulia": "Friuli-Venezia Giulia",
    "friuli-venezia giulia": "Friuli-Venezia Giulia",
    "liguria": "Liguria",
    "emilia romagna": "Emilia-Romagna",
    "emilia-romagna": "Emilia-Romagna",
    "toscana": "Toscana",
    "umbria": "Umbria",
    "marche": "Marche",
    "lazio": "Lazio",
    "abruzzo": "Abruzzo",
    "molise": "Molise",
    "campania": "Campania",
    "puglia": "Puglia",
    "basilicata": "Basilicata",
    "calabria": "Calabria",
    "sicilia": "Sicilia",
    "sardegna": "Sardegna"
}

# Funzione per normalizzare i nomi delle regioni
def normalizza_regione(nome):
    if not isinstance(nome, str):
        return None
    nome = nome.strip().lower()
    nome = nome.replace("’", "'")        # apostrofo tipografico → normale
    nome = " ".join(nome.split())        # compatta spazi multipli
    return REGIONI_STANDARD.get(nome, None)

# Lettura della lista dei nomi delle regioni e inserimento dove mancano
for nome in set(REGIONI_STANDARD.values()):
    if not session.query(Regioni).filter_by(nome=nome).first():
        session.add(Regioni(nome=nome))

# Correzione dati all'italiana, circa e pct (10.000,00 -> 10000.00, ~40 -> 40, 50% --> 50)
def to_float(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    val = str(val).strip()
    if val.startswith("~"):
        val = val[1:]  # rimuove il simbolo ~
    if val.endswith("%"):
        val = val[:-1]  # rimuove il simbolo %
    val = val.replace(".", "").replace(",", ".")
    try:
        return float(val)
    except ValueError:
        return None


# Popola tabella regioni con i dati dal CSV
df = pd.read_csv("Regioni.csv")

# Inserisci i record della tab regioni
for i, row in df.iterrows():
    regione_std = normalizza_regione(row["Regione"])
    if not regione_std:
        continue

    record = session.query(Regioni).filter_by(nome=regione_std).first()
    if record:
        record.superficie_kmq = to_float(row["Superficie Kmq"])
        record.densita_demografica = to_float(row["densita_demografica_kmq\nabitanti/km²"])
        record.pil = to_float(row["PIL per abitante (migliaia di €)"])
    else:
        nuova_regione = Regioni(
            nome=regione_std,
            superficie_kmq=to_float(row["Superficie Kmq"]),
            densita_demografica=to_float(row["densita_demografica_kmq\nabitanti/km²"]),
            pil=to_float(row["PIL per abitante (migliaia di €)"])
        )
        session.add(nuova_regione)

# Popola tabella morfologia_suolo con i dati dal CSV
df_morf = pd.read_csv("Morfologia_del_suolo.csv")

for i, row in df_morf.iterrows():
    regione_std = normalizza_regione(row["Regione"])
    if not regione_std:
        continue

    record_regione = session.query(Regioni).filter_by(nome=regione_std).first()
    if not record_regione:
        continue  # se la regione non è stata inserita prima, salta

    record_morf = session.query(MorfologiaSuolo).filter_by(id_regione=record_regione.id_regione).first()
    if not record_morf:
        record_morf = MorfologiaSuolo(id_regione=record_regione.id_regione)
        session.add(record_morf)

    record_morf.pianura_pct = to_float(row["Pianura (%)"])
    record_morf.collina_pct = to_float(row["Collina (%)"])
    record_morf.montagna_pct = to_float(row["Montagna (%)"])
    record_morf.urbano_pct = to_float(row["Urbano (%)"])
    record_morf.agricolo_pct = to_float(row["Agricolo (%)"])
    record_morf.forestale_pct = to_float(row["Forestale (%)"])

# Popola tabella emissioni_totali con i dati dal CSV
df_emiss = pd.read_csv("Emissioni regionali MILIONI di t co2.csv")

for i, row in df_emiss.iterrows():
    regione_std = normalizza_regione(row["Regione"])
    if not regione_std:
        continue

    record_regione = session.query(Regioni).filter_by(nome=regione_std).first()
    if not record_regione:
        continue

    record_emiss = session.query(EmissioniTotali).filter_by(id_regione=record_regione.id_regione).first()
    if not record_emiss:
        record_emiss = EmissioniTotali(id_regione=record_regione.id_regione)
        session.add(record_emiss)

    record_emiss.co2eq_mln_t = to_float(row["Emissioni (milioni di t CO₂ eq)"])

# Popola tabella edifici con i dati dai 4 CSV
df_consumi = pd.read_csv("Consumi di energia degli edifici.csv")
df_emissioni = pd.read_csv("Emissioni pro capite di gas serra degli edifici.csv")
df_quota_elettrico = pd.read_csv("Quota di consumi elettrici negli edifici rispetto al totale.csv")
df_classe_a = pd.read_csv("Quota di edifici in classe A negli APE.csv")

for record_regione in session.query(Regioni).all():
    regione_std = record_regione.nome

    # Recupera o crea il record edifici
    record_edifici = session.query(Edifici).filter_by(id_regione=record_regione.id_regione).first()
    if not record_edifici:
        record_edifici = Edifici(id_regione=record_regione.id_regione)
        session.add(record_edifici)

    # Consumo medio
    row_cons = df_consumi[df_consumi["Regione"].str.strip().str.lower() == regione_std.lower()]
    if not row_cons.empty:
        record_edifici.consumo_medio_kwh_m2y = to_float(row_cons.iloc[0]["Consumo medio (kWh/m²/anno)"])

    # Emissioni pro capite
    row_emiss = df_emissioni[df_emissioni["Regione"].str.strip().str.lower() == regione_std.lower()]
    if not row_emiss.empty:
        record_edifici.emissioni_procapite_tco2_ab = to_float(row_emiss.iloc[0]["Emissioni pro capite (tCO₂eq/ab)"])

    # Quota elettrico
    row_qe = df_quota_elettrico[df_quota_elettrico["Regione"].str.strip().str.lower() == regione_std.lower()]
    if not row_qe.empty:
        record_edifici.quota_elettrico_pct = to_float(row_qe.iloc[0]["Quota (%)"])

    # Quota classe A
    row_ca = df_classe_a[df_classe_a["Regione"].str.strip().str.lower() == regione_std.lower()]
    if not row_ca.empty:
        record_edifici.quota_ape_classe_a_pct = to_float(row_ca.iloc[0]["Quota (%)"])


# Popola tabella industria
df_emissioni = pd.read_csv("Emissioni di gas serra per valore aggiunto dell'industria.csv")
df_quota = pd.read_csv("Quota di consumi elettrici nell'industria.csv")

# Merge dei due dataset sulla colonna Regione
df_industria = pd.merge(df_emissioni, df_quota, on="Regione", how="outer")

for i, row in df_industria.iterrows():
    regione_std = normalizza_regione(row["Regione"])
    if not regione_std:
        continue

    record = session.query(Industria).filter_by(id_regione=
        session.query(Regioni.id_regione).filter_by(nome=regione_std).scalar()
    ).first()

    if record:
        record.emissioni_per_valore_aggiunto_tco2_per_mln_eur = to_float(row["Emissioni (tCO₂eq/€ mln)"])
        record.quota_elettrico_pct = to_float(row["Quota (%)"])
    else:
        nuova_industria = Industria(
            id_regione=session.query(Regioni.id_regione).filter_by(nome=regione_std).scalar(),
            emissioni_per_valore_aggiunto_tco2_per_mln_eur=to_float(row["Emissioni (tCO₂eq/€ mln)"]),
            quota_elettrico_pct=to_float(row["Quota (%)"])
        )
        session.add(nuova_industria)

# Popola tabella mix_energetico
df_mix = pd.read_csv("Quote mixenergetico.csv")

for i, row in df_mix.iterrows():
    regione_std = normalizza_regione(row["Regione"])
    if not regione_std:
        continue

    id_regione = session.query(Regioni.id_regione).filter_by(nome=regione_std).scalar()
    if not id_regione:
        continue

    record = session.query(MixEnergetico).filter_by(id_regione=id_regione).first()
    if not record:
        record = MixEnergetico(id_regione=id_regione)
        session.add(record)

    record.carbone_pct = to_float(row["Carbone"])
    record.petrolio_pct = to_float(row["Petrolio"])
    record.gas_pct = to_float(row["Gas"])

    record.rinnovabili_pct = to_float(row["Rinnovabili"])

# Popola tabella assorbimenti (guidato da Regioni)
df_ass = pd.read_csv("Assorbimenti regionali.csv")

for record_regione in session.query(Regioni).all():
    regione_std = record_regione.nome

    # cerca record già esistente
    record = session.query(Assorbimenti).filter_by(id_regione=record_regione.id_regione).first()
    if not record:
        record = Assorbimenti(id_regione=record_regione.id_regione)
        session.add(record)

    # cerca la riga corrispondente nel CSV
    row = df_ass[df_ass["Regione"].str.strip().str.lower() == regione_std.lower()]

    if not row.empty:
        record.punti_forza = row.iloc[0]["Punti di forza principali"] if pd.notna(row.iloc[0]["Punti di forza principali"]) else None
        record.aree_miglioramento = row.iloc[0]["Aree di miglioramento principali"] if pd.notna(row.iloc[0]["Aree di miglioramento principali"]) else None
    else:
        record.punti_forza = None
        record.aree_miglioramento = None

# --- Popola tabella Azioni ---
df_fotovoltaico = pd.read_csv("Capacità installata di energia fotovoltaica.csv")
df_rinnovabili = pd.read_csv("Produzione di energia elettrica da fonti rinnovabili.csv")
df_auto = pd.read_csv("Quota di auto elettriche.csv")
df_risparmi = pd.read_csv("Risparmi energetici.csv")

# Normalizza numeri italiani e % 
def parse_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip().replace("~", "")  # rimuove circa
    if val.endswith("%"):
        val = val[:-1]  # rimuove il simbolo %
    val = val.replace(".", "").replace(",", ".")  # converte 10.000,50 -> 10000.50
    try:
        return float(val)
    except ValueError:
        return None

# Dizionari regione → valore
fotovoltaico_map = {
    normalizza_regione(r): parse_number(v)
    for r, v in zip(df_fotovoltaico["Regione"], df_fotovoltaico["Capacità fotovoltaica (GW)"])
}
rinnovabili_map = {
    normalizza_regione(r): parse_number(v)
    for r, v in zip(df_rinnovabili["Regione"], df_rinnovabili["Produzione da FER (%)"])
}
auto_map = {
    normalizza_regione(r): parse_number(v)
    for r, v in zip(df_auto["Regione"], df_auto["Quota di auto elettriche (%)"])
}
risparmi_map = {
    normalizza_regione(r): parse_number(v)
    for r, v in zip(df_risparmi["Regione"], df_risparmi["Risparmio energetico (Mtep)"])
}

# Inserisci/aggiorna ogni regione
for nome in REGIONI_STANDARD.values():
    record_reg = session.query(Regioni).filter_by(nome=nome).first()
    if not record_reg:
        continue

    record = session.query(Azioni).filter_by(id_regione=record_reg.id_regione).first()
    if not record:
        record = Azioni(id_regione=record_reg.id_regione)
        session.add(record)

    record.fotovoltaico_capacita_gw = fotovoltaico_map.get(nome)
    record.quota_produzione_fer_pct = rinnovabili_map.get(nome)
    record.quota_auto_elettriche_pct = auto_map.get(nome)
    record.risparmi_energetici_mtep_mln = risparmi_map.get(nome)

session.commit()



