from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas

# ==============================
# REGIONI
# ==============================
class RegioneService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.Regioni).all()

    @staticmethod
    def get_by_id(regione_id: int, db: Session):
        regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
        if not regione:
            raise HTTPException(status_code=404, detail="Regione non trovata")
        return regione

    @staticmethod
    def create(regione: schemas.RegioneCreate, db: Session):
        db_regione = models.Regioni(**regione.dict())
        db.add(db_regione)
        db.commit()
        db.refresh(db_regione)
        return db_regione

    @staticmethod
    def update(regione_id: int, regione: schemas.RegioneCreate, db: Session):
        db_regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
        if not db_regione:
            raise HTTPException(status_code=404, detail="Regione non trovata")
        for key, value in regione.dict().items():
            setattr(db_regione, key, value)
        db.commit()
        db.refresh(db_regione)
        return db_regione

    @staticmethod
    def delete(regione_id: int, db: Session):
        regione = db.query(models.Regioni).filter(models.Regioni.id_regione == regione_id).first()
        if not regione:
            raise HTTPException(status_code=404, detail="Regione non trovata")
        db.delete(regione)
        db.commit()
        return {"message": "Regione eliminata con successo"}


# ==============================
# MORFOLOGIA SUOLO
# ==============================
class MorfologiaService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.MorfologiaSuolo).all()

    @staticmethod
    def create(morf: schemas.MorfologiaSuoloCreate, db: Session):
        db_morf = models.MorfologiaSuolo(**morf.dict())
        db.add(db_morf)
        db.commit()
        db.refresh(db_morf)
        return db_morf


# ==============================
# EMISSIONI TOTALI
# ==============================
class EmissioniService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.EmissioniTotali).all()

    @staticmethod
    def create(emiss: schemas.EmissioniTotaliCreate, db: Session):
        db_emiss = models.EmissioniTotali(**emiss.dict())
        db.add(db_emiss)
        db.commit()
        db.refresh(db_emiss)
        return db_emiss


# ==============================
# EDIFICI
# ==============================
class EdificiService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.Edifici).all()

    @staticmethod
    def create(ed: schemas.EdificiCreate, db: Session):
        db_ed = models.Edifici(**ed.dict())
        db.add(db_ed)
        db.commit()
        db.refresh(db_ed)
        return db_ed


# ==============================
# INDUSTRIA
# ==============================
class IndustriaService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.Industria).all()

    @staticmethod
    def create(ind: schemas.IndustriaCreate, db: Session):
        db_ind = models.Industria(**ind.dict())
        db.add(db_ind)
        db.commit()
        db.refresh(db_ind)
        return db_ind


# ==============================
# MIX ENERGETICO
# ==============================
class MixService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.MixEnergetico).all()

    @staticmethod
    def create(mix: schemas.MixEnergeticoCreate, db: Session):
        db_mix = models.MixEnergetico(**mix.dict())
        db.add(db_mix)
        db.commit()
        db.refresh(db_mix)
        return db_mix


# ==============================
# ASSORBIMENTI
# ==============================
class AssorbimentiService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.Assorbimenti).all()

    @staticmethod
    def create(ass: schemas.AssorbimentiCreate, db: Session):
        db_ass = models.Assorbimenti(**ass.dict())
        db.add(db_ass)
        db.commit()
        db.refresh(db_ass)
        return db_ass


# ==============================
# AZIONI
# ==============================
class AzioniService:
    @staticmethod
    def get_all(db: Session):
        return db.query(models.Azioni).all()

    @staticmethod
    def create(az: schemas.AzioniCreate, db: Session):
        db_az = models.Azioni(**az.dict())
        db.add(db_az)
        db.commit()
        db.refresh(db_az)
        return db_az
