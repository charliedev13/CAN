#Questa applicazione comparativa permette di confrontare le emissioni e l'impegno ambientale di ogni regione italiana

#Vengono utilizzati i csv presenti in DB: fonti ISTAT e ISPRA
#L'utente può selezionare la regione e verificarene i dati

#L'applicazione è stata sviluppata da Carlotta Forlino, Andrea Calabrò e Nicolò Giraudo
"""per far partire il main: 
1) assicurarsi di avere installato le dipendenze in requirements.txt
2) essere dentro la cartella backend
3) avere il venv attivo (se non lo è, digitare: source venv/bin/activate)
4) eseguire il comando:
python -m uvicorn main:app --reload --port 8000"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routes import router as regioni_router

# Creazione delle tabelle
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CAN API",
    description="API CRUD per gestire dati energetici delle regioni",
    version="1.0.0"
)

# Abilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi router
app.include_router(regioni_router)

#test per verificare che l'API sia attiva
@app.get("/")
def read_root():
    return {"message": "CAN API is running. Visit /docs for Swagger UI."}
