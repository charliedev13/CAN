from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
from services import (
    RegioneService,
    MorfologiaService,
    EmissioniService,
    EdificiService,
    IndustriaService,
    MixService,
    AssorbimentiService,
    AzioniService
)

router = APIRouter()

# =====================================================
# REGIONI
# =====================================================
@router.get("/regioni", response_model=List[schemas.Regione])
def get_all_regioni(db: Session = Depends(get_db)):
    return RegioneService.get_all(db)

@router.get("/regioni/{regione_id}", response_model=schemas.Regione)
def get_regione(regione_id: int, db: Session = Depends(get_db)):
    return RegioneService.get_by_id(regione_id, db)

@router.post("/regioni", response_model=schemas.Regione)
def create_regione(regione: schemas.RegioneCreate, db: Session = Depends(get_db)):
    return RegioneService.create(regione, db)

@router.put("/regioni/{regione_id}", response_model=schemas.Regione)
def update_regione(regione_id: int, regione: schemas.RegioneCreate, db: Session = Depends(get_db)):
    return RegioneService.update(regione_id, regione, db)

@router.delete("/regioni/{regione_id}")
def delete_regione(regione_id: int, db: Session = Depends(get_db)):
    return RegioneService.delete(regione_id, db)


# =====================================================
# MORFOLOGIA SUOLO
# =====================================================
@router.get("/morfologia", response_model=List[schemas.MorfologiaSuolo])
def get_all_morfologia(db: Session = Depends(get_db)):
    return MorfologiaService.get_all(db)

@router.post("/morfologia", response_model=schemas.MorfologiaSuolo)
def create_morfologia(morf: schemas.MorfologiaSuoloCreate, db: Session = Depends(get_db)):
    return MorfologiaService.create(morf, db)


# =====================================================
# EMISSIONI TOTALI
# =====================================================
@router.get("/emissioni", response_model=List[schemas.EmissioniTotali])
def get_all_emissioni(db: Session = Depends(get_db)):
    return EmissioniService.get_all(db)

@router.post("/emissioni", response_model=schemas.EmissioniTotali)
def create_emissioni(emiss: schemas.EmissioniTotaliCreate, db: Session = Depends(get_db)):
    return EmissioniService.create(emiss, db)


# =====================================================
# EDIFICI
# =====================================================
@router.get("/edifici", response_model=List[schemas.Edifici])
def get_all_edifici(db: Session = Depends(get_db)):
    return EdificiService.get_all(db)

@router.post("/edifici", response_model=schemas.Edifici)
def create_edifici(ed: schemas.EdificiCreate, db: Session = Depends(get_db)):
    return EdificiService.create(ed, db)


# =====================================================
# INDUSTRIA
# =====================================================
@router.get("/industria", response_model=List[schemas.Industria])
def get_all_industria(db: Session = Depends(get_db)):
    return IndustriaService.get_all(db)

@router.post("/industria", response_model=schemas.Industria)
def create_industria(ind: schemas.IndustriaCreate, db: Session = Depends(get_db)):
    return IndustriaService.create(ind, db)


# =====================================================
# MIX ENERGETICO
# =====================================================
@router.get("/mix", response_model=List[schemas.MixEnergetico])
def get_all_mix(db: Session = Depends(get_db)):
    return MixService.get_all(db)

@router.post("/mix", response_model=schemas.MixEnergetico)
def create_mix(mix: schemas.MixEnergeticoCreate, db: Session = Depends(get_db)):
    return MixService.create(mix, db)


# =====================================================
# ASSORBIMENTI
# =====================================================
@router.get("/assorbimenti", response_model=List[schemas.Assorbimenti])
def get_all_assorbimenti(db: Session = Depends(get_db)):
    return AssorbimentiService.get_all(db)

@router.post("/assorbimenti", response_model=schemas.Assorbimenti)
def create_assorbimenti(ass: schemas.AssorbimentiCreate, db: Session = Depends(get_db)):
    return AssorbimentiService.create(ass, db)


# =====================================================
# AZIONI
# =====================================================
@router.get("/azioni", response_model=List[schemas.Azioni])
def get_all_azioni(db: Session = Depends(get_db)):
    return AzioniService.get_all(db)

@router.post("/azioni", response_model=schemas.Azioni)
def create_azioni(az: schemas.AzioniCreate, db: Session = Depends(get_db)):
    return AzioniService.create(az, db)