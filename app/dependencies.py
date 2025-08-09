from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from jose import JWTError, jwt
import os
from app.db.supabase import get_supabase_client
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in .env file")

ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), supabase: Client = Depends(get_supabase_client)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Supabase automatically verifies the JWT, so we just need to get the user
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if user is None:
            raise credentials_exception
            
        user_data = {
            "id": user.id,
            "email": user.email,
            "nom": user.user_metadata.get("nom"),
            "prenom": user.user_metadata.get("prenom"),
            "type_utilisateur": user.user_metadata.get("type_utilisateur"),
            "adresse_postale": user.user_metadata.get("adresse_postale"),
            "numero_telephone": user.user_metadata.get("numero_telephone"),
        }
        return User(**user_data)
    except Exception:
        raise credentials_exception
