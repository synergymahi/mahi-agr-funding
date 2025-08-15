from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.dependencies import get_current_user, get_optional_current_user
from app.schemas.user import User
from typing import List, Optional
import os

API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
optional_api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def RoleChecker(allowed_roles: List[str]):
    """
    Dependency that checks if the current user has one of the allowed roles.
    """
    def _check_roles(current_user: User = Depends(get_current_user)):
        if current_user.type_utilisateur not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted: User does not have the right role"
            )
        return current_user
    return _check_roles

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency that checks for a valid API key.
    """
    if API_KEY and api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API KEY"
        )

async def get_optional_api_key(api_key: str = Security(optional_api_key_header)):
    if api_key and API_KEY and api_key == API_KEY:
        return api_key
    return None

async def allow_user_or_app(
    user: Optional[User] = Depends(get_optional_current_user),
    api_key: Optional[str] = Depends(get_optional_api_key)
):
    if user is None and api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide a user token or an API key.",
        )
    return user or api_key