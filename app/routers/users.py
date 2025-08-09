from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.db.supabase import get_supabase_client
from app.dependencies import get_current_user
from app.schemas.user import User, UserUpdate

router = APIRouter()

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Update current user's profile.
    """
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    # Here you would add the SMS verification logic for numero_telephone
    # For example, using a service like Twilio.
    # This is a placeholder for that logic.
    if "numero_telephone" in update_data:
        print(f"SMS verification needed for {update_data['numero_telephone']}")

    try:
        # Supabase stores this in the 'user_metadata' field of the auth.users table
        response = supabase.auth.update_user({"data": update_data})
        
        updated_user = response.user
        if updated_user is None:
            raise HTTPException(status_code=400, detail="Failed to update user")

        user_data = {
            "id": updated_user.id,
            "email": updated_user.email,
            "nom": updated_user.user_metadata.get("nom"),
            "prenom": updated_user.user_metadata.get("prenom"),
            "type_utilisateur": updated_user.user_metadata.get("type_utilisateur"),
            "adresse_postale": updated_user.user_metadata.get("adresse_postale"),
            "numero_telephone": updated_user.user_metadata.get("numero_telephone"),
        }
        return User(**user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile.
    """
    return current_user
