#modellazione del DB e creazione tabelle
from sqlalchemy import Engine, create_engine, Column, Integer, String, Numeric, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from database import Base, engine

# Regioni

class Regioni(Base):
    __tablename__ = 'regioni'
    id_regione = Column(Integer, autoincrement=True, primary_key=True) 
    nome = Column(String(80), unique=True, nullable=False)
    superficie_kmq = Column(Numeric(12,2))
    densita_demografica = Column(Numeric(12,2))
    pil = Column(Numeric(14,2))

    # relazioni 1:1
    morfologia = relationship("MorfologiaSuolo", back_populates="regione", uselist=False)
    emissioni_totali = relationship("EmissioniTotali", back_populates="regione", uselist=False)
    edifici = relationship("Edifici", back_populates="regione", uselist=False)
    industria = relationship("Industria", back_populates="regione", uselist=False)
    mix = relationship("MixEnergetico", back_populates="regione", uselist=False)
    assorbimenti = relationship("Assorbimenti", back_populates="regione", uselist=False)
    azioni = relationship("Azioni", back_populates="regione", uselist=False)


# Morfologia suolo

class MorfologiaSuolo(Base):
    __tablename__ = "morfologia_suolo"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    pianura_pct = Column(Numeric(5,2))
    collina_pct = Column(Numeric(5,2))
    montagna_pct = Column(Numeric(5,2))
    urbano_pct = Column(Numeric(5,2))
    agricolo_pct = Column(Numeric(5,2))
    forestale_pct = Column(Numeric(5,2))

    regione = relationship("Regioni", back_populates="morfologia")


# Emissioni totali
class EmissioniTotali(Base):
    __tablename__ = "emissioni_totali"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    co2eq_mln_t = Column(Numeric(12,3))  # milioni di tonnellate CO2eq

    regione = relationship("Regioni", back_populates="emissioni_totali")

# Edifici
class Edifici(Base):
    __tablename__ = "edifici"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    consumo_medio_kwh_m2y = Column(Numeric(12,2))
    emissioni_procapite_tco2_ab = Column(Numeric(12,3))
    quota_elettrico_pct = Column(Numeric(5,2))
    quota_ape_classe_a_pct = Column(Numeric(5,2))

    regione = relationship("Regioni", back_populates="edifici")

# Industria
class Industria(Base):
    __tablename__ = "industria"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    emissioni_per_valore_aggiunto_tco2_per_mln_eur = Column(Numeric(12,4))
    quota_elettrico_pct = Column(Numeric(5,2))

    regione = relationship("Regioni", back_populates="industria")

# Mix energetico
class MixEnergetico(Base):
    __tablename__ = "mix_energetico"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    carbone_pct = Column(Numeric(5,2))
    petrolio_pct = Column(Numeric(5,2))
    gas_pct = Column(Numeric(5,2))
    rinnovabili_pct = Column(Numeric(5,2))

    regione = relationship("Regioni", back_populates="mix")

    __table_args__ = (
        # opzionale: controlla che la somma sia ~100 (tolleranza ±1)
        CheckConstraint(
            "(carbone_pct + petrolio_pct + gas_pct + rinnovabili_pct) BETWEEN 99.0 AND 101.0",
            name="chk_mix_somma_~100"
        ),
    )

# Assorbimenti
class Assorbimenti(Base):
    __tablename__ = "assorbimenti"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    punti_forza = Column(Text)
    aree_miglioramento = Column(Text)

    regione = relationship("Regioni", back_populates="assorbimenti")

# Azioni
class Azioni(Base):
    __tablename__ = "azioni"

    id_regione = Column(Integer, ForeignKey("regioni.id_regione"), primary_key=True)
    fotovoltaico_capacita_gw = Column(Numeric(10,3))
    quota_produzione_fer_pct = Column(Numeric(5,2))
    quota_auto_elettriche_pct = Column(Numeric(5,2))
    risparmi_energetici_mtep_mln = Column(Numeric(10,3))

    regione = relationship("Regioni", back_populates="azioni")

#Creazione tabelle 
Base.metadata.create_all(engine)