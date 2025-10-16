from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routes import router as regioni_router
#from routes_auth import router as auth_api_router
#from auth_app import router as auth_pages_router

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
#app.include_router(auth_api_router)        # API autenticazione
#app.include_router(auth_pages_router)      # Pagine HTML autenticazione

#test per verificare che l'API sia attiva
@app.get("/")
def read_root():
    return {"message": "CAN API is running. Visit /docs for Swagger UI."}
