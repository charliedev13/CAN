from model_db import *
import pandas as pd

session = Session()  

"""regioni = pd.read_csv('Regioni.csv')"""
regioni = Regioni()

# Record di prova
piemonte = Regioni(
    nome="Piemonte",
    superficie_kmq=25399.00,
    densita_demografica=170.50,
    pil=143000.00
)

# Inserimento e commit
session.add(piemonte)


print("✅ Inserito record di test in 'regioni'")


"""for index, row in regioni.iterrows():
    new_region = Regioni(
        nome=row['nome'],
        superficie_kmq=row['superficie_kmq'],
        densita_demografica=row['densita_demografica'],
        pil=row['pil']
    )
    session.add(new_region)"""




session.commit()
"""print("Dati inseriti correttamente.")"""

