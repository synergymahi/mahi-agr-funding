from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from typing import Optional, Literal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str

class UserCreate(UserBase):
    password: str

    def get_password_hash(self):
        return pwd_context.hash(self.password)

class UserUpdate(BaseModel):
    type_utilisateur: Optional[Literal['donateur/prêteur', 'porteur de projet', 'administrateur']] = Field(None, description="Type of user")
    adresse_postale: Optional[str] = Field(None, description="Postal address")
    numero_telephone: Optional[str] = Field(None, description="Phone number")

class User(UserBase):
    id: str
    type_utilisateur: Optional[Literal['donateur/prêteur', 'porteur de projet', 'administrateur']] = None
    adresse_postale: Optional[str] = None
    numero_telephone: Optional[str] = None
    
    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True