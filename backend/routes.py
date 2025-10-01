from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter()

# =====================================================
# ROUTES REGIONI
# =====================================================
@router.get("/regioni", response_model=List[schemas.Regione])
def get_all_regioni(db: Session = Depends(get_db)):
    return db.query(models.Regioni).all()

@router.get("/regioni/{regione_id}", response_model=schemas.Regione)
def get_regione(regione_id: int, db: Session = Depends(get_db)):
    regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
    if not regione:
        raise HTTPException(status_code=404, detail="Regione non trovata")
    return regione

@router.post("/regioni", response_model=schemas.Regione)
def create_regione(regione: schemas.RegioneCreate, db: Session = Depends(get_db)):
    db_regione = models.Regioni(**regione.dict())
    db.add(db_regione)
    db.commit()
    db.refresh(db_regione)
    return db_regione

@router.put("/regioni/{regione_id}", response_model=schemas.Regione)
def update_regione(regione_id: int, regione: schemas.RegioneCreate, db: Session = Depends(get_db)):
    db_regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
    if not db_regione:
        raise HTTPException(status_code=404, detail="Regione non trovata")
    for key, value in regione.dict().items():
        setattr(db_regione, key, value)
    db.commit()
    db.refresh(db_regione)
    return db_regione

@router.delete("/regioni/{regione_id}")
def delete_regione(regione_id: int, db: Session = Depends(get_db)):
    regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
    if not regione:
        raise HTTPException(status_code=404, detail="Regione non trovata")
    db.delete(regione)
    db.commit()
    return {"message": "Regione eliminata con successo"}


# =====================================================
# MORFOLOGIA SUOLO
# =====================================================
@router.get("/morfologia", response_model=List[schemas.MorfologiaSuolo])
def get_all_morfologia(db: Session = Depends(get_db)):
    return db.query(models.MorfologiaSuolo).all()

@router.post("/morfologia", response_model=schemas.MorfologiaSuolo)
def create_morfologia(morf: schemas.MorfologiaSuoloCreate, db: Session = Depends(get_db)):
    db_morf = models.MorfologiaSuolo(**morf.dict())
    db.add(db_morf)
    db.commit()
    db.refresh(db_morf)
    return db_morf


# =====================================================
# EMISSIONI TOTALI
# =====================================================
@router.get("/emissioni", response_model=List[schemas.EmissioniTotali])
def get_all_emissioni(db: Session = Depends(get_db)):
    return db.query(models.EmissioniTotali).all()

@router.post("/emissioni", response_model=schemas.EmissioniTotali)
def create_emissioni(emiss: schemas.EmissioniTotaliCreate, db: Session = Depends(get_db)):
    db_emiss = models.EmissioniTotali(**emiss.dict())
    db.add(db_emiss)
    db.commit()
    db.refresh(db_emiss)
    return db_emiss


# =====================================================
# EDIFICI
# =====================================================
@router.get("/edifici", response_model=List[schemas.Edifici])
def get_all_edifici(db: Session = Depends(get_db)):
    return db.query(models.Edifici).all()

@router.post("/edifici", response_model=schemas.Edifici)
def create_edifici(ed: schemas.EdificiCreate, db: Session = Depends(get_db)):
    db_ed = models.Edifici(**ed.dict())
    db.add(db_ed)
    db.commit()
    db.refresh(db_ed)
    return db_ed


# =====================================================
# INDUSTRIA
# =====================================================
@router.get("/industria", response_model=List[schemas.Industria])
def get_all_industria(db: Session = Depends(get_db)):
    return db.query(models.Industria).all()

@router.post("/industria", response_model=schemas.Industria)
def create_industria(ind: schemas.IndustriaCreate, db: Session = Depends(get_db)):
    db_ind = models.Industria(**ind.dict())
    db.add(db_ind)
    db.commit()
    db.refresh(db_ind)
    return db_ind

# =====================================================
# MIX ENERGETICO
# =====================================================
@router.get("/mix", response_model=List[schemas.MixEnergetico])
def get_all_mix(db: Session = Depends(get_db)):
    return db.query(models.MixEnergetico).all()

@router.post("/mix", response_model=schemas.MixEnergetico)
def create_mix(mix: schemas.MixEnergeticoCreate, db: Session = Depends(get_db)):
    db_mix = models.MixEnergetico(**mix.dict())
    db.add(db_mix)
    db.commit()
    db.refresh(db_mix)
    return db_mix


# =====================================================
# ASSORBIMENTI
# =====================================================
@router.get("/assorbimenti", response_model=List[schemas.Assorbimenti])
def get_all_assorbimenti(db: Session = Depends(get_db)):
    return db.query(models.Assorbimenti).all()

@router.post("/assorbimenti", response_model=schemas.Assorbimenti)
def create_assorbimenti(ass: schemas.AssorbimentiCreate, db: Session = Depends(get_db)):
    db_ass = models.Assorbimenti(**ass.dict())
    db.add(db_ass)
    db.commit()
    db.refresh(db_ass)
    return db_ass


# =====================================================
# AZIONI
# =====================================================
@router.get("/azioni", response_model=List[schemas.Azioni])
def get_all_azioni(db: Session = Depends(get_db)):
    return db.query(models.Azioni).all()

@router.post("/azioni", response_model=schemas.Azioni)
def create_azioni(az: schemas.AzioniCreate, db: Session = Depends(get_db)):
    db_az = models.Azioni(**az.dict())
    db.add(db_az)
    db.commit()
    db.refresh(db_az)
    return db_az