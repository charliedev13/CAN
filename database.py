#creazione tabelle
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#collegare le API
'''primo metodo: 
pip3 install eurostat 
+ libreria pandas

secondo metodo: 
tramite postman e la creazione composta degli URL'''

#Connessione e setup dell'ORM
engine = create_engine('mysql://root:Hfdfzbhvd.665root@localhost/CAN_DB') #localhost da collegare al docker
Base = declarative_base()  # Classe base per i modelli ORM
Session = sessionmaker(bind=engine)  # Factory per creare sessioni

#Classe Paesi
class Regioni(Base):
    __tablename__ = 'paesi'
    id = Column(Integer, autoincrement=1, primary_key=True) 
    nome = Column(String(50))
    abitanti = Column(Integer)
    superficie_kmq = Column(Integer)
    pil = Column(Integer)
    settore_primario = Column(String(50))

#Creazione tabelle e inserimento dati
Base.metadata.create_all(engine)
session = Session()  = Paesi(nome="Spagna", abitanti=500000, pil=1700, superficie_kmq=505990, settore_primario="agricoltura")
session.add(Paesi)
session.commit()







