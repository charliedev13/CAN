"""
Crea la connessione a MySQL e il motore SQLAlchemy.
Espone la sessione da usare in routes e services.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# importa file env
from dotenv import load_dotenv
import os
load_dotenv()
URL_PASSWORD_DB = os.getenv("URL_PASSWORD_DB")
SQLALCHEMY_DATABASE_URL = URL_PASSWORD_DB

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency per le rotte
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()