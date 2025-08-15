from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from app.db.supabase import get_supabase_client
from app.dependencies import get_current_user
from app.schemas.user import User
from app.schemas.project import ProjetCreate, ProjetUpdate, ProjetInDB
from app.security import RoleChecker, get_api_key
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ProjetInDB, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjetCreate,
    current_user: User = Depends(RoleChecker(["porteur de projet"])),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Create a new project. Only users with the 'porteur de projet' role can create projects.
    """
    project_dict = project.model_dump()
    project_dict["owner_id"] = str(current_user.id)
    project_dict["date_lancement"] = project.date_lancement.isoformat()
    project_dict["date_fin"] = project.date_fin.isoformat()
    try:
        response = supabase.table("projects").insert(project_dict).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create project")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ProjetInDB])
def get_projects(
    supabase: Client = Depends(get_supabase_client),
    api_key: str = Depends(get_api_key)
):
    """
    Get all projects.
    """
    try:
        response = supabase.table("projects").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.security import RoleChecker, get_api_key, allow_user_or_app

@router.get("/{project_id}", response_model=ProjetInDB)
def get_project(
    project_id: UUID,
    supabase: Client = Depends(get_supabase_client),
    auth: str = Depends(allow_user_or_app)
):
    """
    Get a single project by ID.
    Accessible by authenticated users or applications with an API key.
    """
    try:
        response = supabase.table("projects").select("*").eq("id", str(project_id)).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Project not found")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}", response_model=ProjetInDB)
def update_project(
    project_id: UUID,
    project_update: ProjetUpdate,
    current_user: User = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Update a project. Only the owner can update their project.
    """
    project = get_project(project_id, supabase)
    if str(project["owner_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

    update_data = project_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    try:
        response = supabase.table("projects").update(update_data).eq("id", str(project_id)).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to update project")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    current_user: User = Depends(RoleChecker(["administrateur", "porteur de projet"])),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Delete a project. Only the owner or an admin can delete a project.
    """
    project = get_project(project_id, supabase)
    
    # Allow deletion if the user is an admin OR the owner of the project
    if current_user.type_utilisateur != 'administrateur' and str(project["owner_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    try:
        supabase.table("projects").delete().eq("id", str(project_id)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))