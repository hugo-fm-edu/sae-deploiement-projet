from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProfileBase(BaseModel):
    """Schéma de base pour UserProfile contenant les champs communs"""
    bio: Optional[str] = Field(None, max_length=500, description="Biographie de l'utilisateur")
    phone_number: Optional[str] = Field(None, max_length=20, description="Numéro de téléphone")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bio": "Développeur passionné par Python et FastAPI",
                "phone_number": "+33 6 12 34 56 78"
            }
        }
    )


class ProfileCreate(ProfileBase):
    """Schéma pour la création d'un profil utilisateur"""
    user_id: int = Field(..., description="ID de l'utilisateur associé")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "bio": "Développeur passionné par Python et FastAPI",
                "phone_number": "+33 6 12 34 56 78"
            }
        }
    )


class ProfileUpdate(ProfileBase):
    """Schéma pour la mise à jour d'un profil (tous les champs optionnels)"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bio": "Développeur senior spécialisé en FastAPI et PostgreSQL",
                "phone_number": "+33 6 98 76 54 32"
            }
        }
    )


class ProfileResponse(ProfileBase):
    """Schéma pour la réponse API contenant un profil utilisateur"""
    id: int = Field(..., description="ID unique du profil")
    user_id: int = Field(..., description="ID de l'utilisateur associé")
    
    model_config = ConfigDict(
        from_attributes=True,  # Permet la conversion depuis les modèles ORM
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "bio": "Développeur passionné par Python et FastAPI",
                "phone_number": "+33 6 12 34 56 78"
            }
        }
    )
