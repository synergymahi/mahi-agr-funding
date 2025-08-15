from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.db.supabase import get_supabase_admin_client
from app.schemas.user import User, UserAdminUpdate
from app.security import RoleChecker
from uuid import UUID

router = APIRouter()

@router.put("/users/{user_id}", response_model=User)
def update_user_by_admin(
    user_id: UUID,
    user_update: UserAdminUpdate,
    admin_user: User = Depends(RoleChecker(["administrateur"])),
    supabase: Client = Depends(get_supabase_admin_client),
):
    """
    Update a user's information. Accessible only by an administrator.
    """
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    try:
        # For admin updates, custom data must be placed in the 'user_metadata' field.
        response = supabase.auth.admin.update_user_by_id(
            str(user_id), {"user_metadata": update_data}
        )
        print("Supabase admin update response:", response)
        
        updated_user = response.user
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found or failed to update")

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
        # The Supabase client can raise specific errors, but we'll catch a generic one for now
        raise HTTPException(status_code=500, detail=str(e))
