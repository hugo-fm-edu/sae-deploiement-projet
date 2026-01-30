from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    """Enum pour le statut des taches"""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskBase(BaseModel):
    """Schema de base pour une tache"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Titre de la tâche",
        example="Ma Tâche"
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Statut de la tâche"
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Date d'échéance (format: YYYY-MM-DD)",
        example="2026-02-15"
    )

class TaskCreate(TaskBase):
    """Schema pour la création d'une tache"""
    project_id: int = Field(
        ..., 
        gt=0,
        description="ID du projet auquel appartient la tâche",
        example=1
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Créer les routes API",
                "status": "TODO",
                "due_date": "2026-02-20",
                "project_id": 1
            }
        }
    )

class TaskUpdate(BaseModel):
    """Schema pour la mise à jour d'une tache"""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
    )
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "IN_PROGRESS",
                "due_date": "2026-02-25"
            }
        }
    )
class TaskResponse(TaskBase):
    """Schema pour la réponse d'une tache,
    hérite de TaskBase et ajoute l'id et project_id
    """
    id: int
    project_id: int

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Ma Tâche",
                "status": "DONE",
                "due_date": "2026-01-07",
                "project_id": 1
            }
        }
    )   