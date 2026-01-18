from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schéma de base pour User contenant les champs communs"""
    name: str = Field(..., min_length=1, max_length=100, description="Nom de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com"
            }
        }
    )


class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com"
            }
        }
    )


class UserUpdate(BaseModel):
    """Schéma pour la mise à jour d'un utilisateur (tous les champs optionnels)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nom de l'utilisateur")
    email: Optional[EmailStr] = Field(None, description="Adresse email de l'utilisateur")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont.new@example.com"
            }
        }
    )


class UserResponse(UserBase):
    """Schéma pour la réponse API contenant un utilisateur"""
    id: int = Field(..., description="ID unique de l'utilisateur")
    
    model_config = ConfigDict(
        from_attributes=True,  # Permet la conversion depuis les modèles ORM
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com"
            }
        }
    )
