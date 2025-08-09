from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client
from app.db.supabase import get_supabase_client
from app.schemas.user import UserCreate, UserInDB
from jose import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register(user: UserCreate, supabase: Client = Depends(get_supabase_client)):
    """
    Register a new user.
    """
    hashed_password = user.get_password_hash()
    user_data = user.model_dump()
    user_data.pop("password")
    
    # Supabase handles user creation and returns a user object.
    # The password is sent to Supabase, which then hashes it.
    # We are pre-hashing here as an example if you were to store users in a public table.
    # For Supabase auth, you would typically do:
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "nom": user.nom,
                    "prenom": user.prenom
                }
            }
        })
        if res.user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not register user")

        # Assuming you have a public.users table to mirror auth.users
        # You would insert the user details there.
        # This is a common pattern to have a public profile for users.
        # For this example, we'll just return the user from Supabase auth.
        
        # The user object from Supabase doesn't directly map to UserInDB,
        # so we'll manually construct it.
        # In a real app, you'd likely have a separate table for user profiles.
        
        # For now, we can't get the ID easily without another query, so we'll mock it.
        # A better approach is to use a trigger in Supabase to copy the user to a public table.
        
        return UserInDB(id=res.user.id, email=res.user.email, nom=user.nom, prenom=user.prenom)
        # return {"id":res.user.id, "email":res.user.email, "nom":user.nom, "prenom":user.prenom}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), supabase: Client = Depends(get_supabase_client)):
    """
    Login a user and return a JWT token.
    """
    try:
        res = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password
        })

        if res.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"access_token": res.session.access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
