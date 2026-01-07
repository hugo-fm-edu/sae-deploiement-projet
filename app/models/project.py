from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database.db import Base


class Project(Base):
    """
    Modèle Project représentant un projet collaboratif.
    
    Relations:
    - Many-to-Many avec User (un projet peut avoir plusieurs utilisateurs)
    - One-to-Many avec Task (un projet peut avoir plusieurs tâches)
    """
    __tablename__ = "projects"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relations
    # Many-to-Many avec User via la table d'association user_project
    users = relationship(
        "User",
        secondary="user_project",  # Table d'association
        back_populates="projects"
    )
    
    # One-to-Many avec Task
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"  # Supprime les tâches si le projet est supprimé
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
