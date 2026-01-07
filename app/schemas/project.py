from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ProjectBase(BaseModel):
    """Schema de base pour project (champs communs)"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nom du projet",
        example="Mon Projet"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Description du projet",
        example="Ceci est une description de mon projet."
    )

class ProjectCreate(ProjectBase):
    """Schema pour la creation d'un projet, 
    hérite de ProjectBase et ajoite rien de spécifique
    """
    pass

class ProjectUpdate(BaseModel):
    """
    Schema pour la mise à jour d'un projet
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
    )
    
class ProjectResponse(ProjectBase):
    """Schema pour la réponse d'un projet,
    hérite de ProjectBase et ajoute l'id
    """
    id: int = Field(..., description="Identifiant unique du projet")
    
    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Mon Projet",
                "description": "Ceci est une description de mon projet.",
            }
        }
    )


# pour eviter les imports circulaires
from .task import TaskResponse

class ProjectWithTasks(ProjectResponse):
    """Schema pour la réponse d'un projet avec toutes ses tâches"""
    tasks: List[TaskResponse] = Field(
        default_factory=list,
        description="Liste des tâches du projet"
    )

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Mon Projet",
                "description": "Ceci est une description de mon projet.",
                "tasks": [
                    {
                        "id": 1,
                        "title": "Ma Tâche",
                        "status": "DONE",
                        "due_date": "2026-01-07",
                        "project_id": 1
                    },
                    {
                        "id": 2,
                        "title": "Ma Deuxième Tâche",
                        "status": "IN_PROGRESS",
                        "due_date": "2026-01-30",
                        "project_id": 1
                    }
                ]
            }
        }
    )