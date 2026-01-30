from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse
from app.schemas.user_profile import ProfileBase, ProfileCreate, ProfileUpdate, ProfileResponse

# Exporter tous les schémas pour faciliter les imports
__all__ = [
    "UserBase",
    "UserCreate", 
    "UserUpdate",
    "UserResponse",
    "ProfileBase",
    "ProfileCreate",
    "ProfileUpdate",
    "ProfileResponse"
]
