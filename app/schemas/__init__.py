"""
Schémas Pydantic pour validation et sérialisation des données.
"""

from .task import (
    TaskStatus,
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from .project import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectWithTasks
)

__all__ = [
    # Task schemas
    "TaskStatus",
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectWithTasks",
]
