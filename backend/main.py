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
app.include_router(regioni_router)         # API dati regionali

#test per verificare che l'API sia attiva
@app.get("/")
def read_root():
    return {"message": "CAN API is running. Visit /docs for Swagger UI."}
