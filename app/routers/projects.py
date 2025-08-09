from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from app.db.supabase import get_supabase_client
from app.dependencies import get_current_user
from app.schemas.user import User
from app.schemas.project import ProjetCreate, ProjetUpdate, ProjetInDB
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ProjetInDB, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjetCreate,
    current_user: User = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Create a new project.
    """
    project_dict = project.dict()
    project_dict["owner_id"] = str(current_user.id)
    
    try:
        response = supabase.table("projects").insert(project_dict).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create project")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ProjetInDB])
def get_projects(supabase: Client = Depends(get_supabase_client)):
    """
    Get all projects.
    """
    try:
        response = supabase.table("projects").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=ProjetInDB)
def get_project(project_id: UUID, supabase: Client = Depends(get_supabase_client)):
    """
    Get a single project by ID.
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
    # First, verify the project exists and the current user is the owner
    project = get_project(project_id, supabase)
    if str(project["owner_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

    update_data = project_update.dict(exclude_unset=True)
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
    current_user: User = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Delete a project. Only the owner can delete their project.
    """
    project = get_project(project_id, supabase)
    if str(project["owner_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    try:
        supabase.table("projects").delete().eq("id", str(project_id)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
