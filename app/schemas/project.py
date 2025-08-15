from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from uuid import UUID

class ProjetBase(BaseModel):
    titre: str
    description: str
    type_financement: str
    montant_objectif: float
    montant_minimum: Optional[float] = None
    montant_collecte: float = 0.0
    montant_maximum: Optional[float] = None
    date_lancement: date
    date_fin: date
    duree_collecte: int
    statut: str = "reçu"
    secteur: str
    region: Optional[str] = None
    localisation: str
    tags_impact: Optional[List[str]] = []
    medias: Optional[List[str]] = []

class ProjetCreate(ProjetBase):
    pass

class ProjetUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    medias: Optional[List[str]] = None

class ProjetInDB(ProjetBase):
    id: UUID
    owner_id: UUID
    coach_id: Optional[UUID] = None
    comite_statut: Optional[str] = "en attente"

    class Config:
        orm_mode = True
