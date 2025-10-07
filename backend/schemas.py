"""Schemas è il ponte tra il database (modelli) e le operazioni CRUD (routes). 
Quindi, ci permette di definire come i dati vengono inviati e ricevuti dall'API."""

#Qui definiamo i modelli Pydantic per la validazione

from pydantic import BaseModel
from typing import Optional

# ---------------------
# Regioni
# ---------------------
class RegioneBase(BaseModel):
    nome: str
    superficie_kmq: Optional[float] = None
    densita_demografica: Optional[float] = None
    pil: Optional[float] = None

class RegioneCreate(RegioneBase):
    pass

class Regione(RegioneBase):
    id_regione: int

    class Config:
        orm_mode = True


# ---------------------
# Morfologia suolo
# ---------------------
class MorfologiaSuoloBase(BaseModel):
    pianura_pct: Optional[float] = None
    collina_pct: Optional[float] = None
    montagna_pct: Optional[float] = None
    urbano_pct: Optional[float] = None
    agricolo_pct: Optional[float] = None
    forestale_pct: Optional[float] = None

class MorfologiaSuoloCreate(MorfologiaSuoloBase):
    id_regione: int

class MorfologiaSuolo(MorfologiaSuoloBase):
    id_regione: int

    class Config:
        orm_mode = True


# ---------------------
# Emissioni totali
# ---------------------
class EmissioniTotaliBase(BaseModel):
    co2eq_mln_t: Optional[float] = None

class EmissioniTotaliCreate(EmissioniTotaliBase):
    id_regione: int

class EmissioniTotali(EmissioniTotaliBase):
    id_regione: int

    class Config:
        orm_mode = True


# ---------------------
# Edifici
# ---------------------
class EdificiBase(BaseModel):
    consumo_medio_kwh_m2y: Optional[float] = None
    emissioni_procapite_tco2_ab: Optional[float] = None
    quota_elettrico_pct: Optional[float] = None
    quota_ape_classe_a_pct: Optional[float] = None

class EdificiCreate(EdificiBase):
    id_regione: int

class Edifici(EdificiBase):
    id_regione: int

    class Config:
        orm_mode = True


# =====================================================
# INDUSTRIA
# =====================================================
class IndustriaBase(BaseModel):
    emissioni_per_valore_aggiunto_tco2_per_mln_eur: Optional[float] = None
    quota_elettrico_pct: Optional[float] = None

class IndustriaCreate(IndustriaBase):
    id_regione: int

class Industria(IndustriaBase):
    id_regione: int

    class Config:
        orm_mode = True

    # ✅ Proprietà alias per compatibilità con la dashboard
    @property
    def quota_elettrico_pct_industria(self) -> Optional[float]:
        """
        Alias per quota_elettrico_pct usato nel frontend
        (grafici e comparazioni).
        """
        return self.quota_elettrico_pct

# ---------------------
# Mix energetico
# ---------------------
class MixEnergeticoBase(BaseModel):
    carbone_pct: Optional[float] = None
    petrolio_pct: Optional[float] = None
    gas_pct: Optional[float] = None
    rinnovabili_pct: Optional[float] = None

class MixEnergeticoCreate(MixEnergeticoBase):
    id_regione: int

class MixEnergetico(MixEnergeticoBase):
    id_regione: int

    class Config:
        orm_mode = True


# ---------------------
# Assorbimenti
# ---------------------
class AssorbimentiBase(BaseModel):
    punti_forza: Optional[str] = None
    aree_miglioramento: Optional[str] = None

class AssorbimentiCreate(AssorbimentiBase):
    id_regione: int

class Assorbimenti(AssorbimentiBase):
    id_regione: int

    class Config:
        orm_mode = True


# ---------------------
# Azioni
# ---------------------
class AzioniBase(BaseModel):
    fotovoltaico_capacita_gw: Optional[float] = None
    quota_produzione_fer_pct: Optional[float] = None
    quota_auto_elettriche_pct: Optional[float] = None
    risparmi_energetici_mtep_mln: Optional[float] = None

class AzioniCreate(AzioniBase):
    id_regione: int

class Azioni(AzioniBase):
    id_regione: int

    class Config:
        orm_mode = True

