#Connessione e setup dell'ORM - localhost da collegare al docker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Hfdfzbhvd.665root@127.0.0.1:3306/CAN_DB"

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
