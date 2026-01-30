from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class Task(Base):
    """
    Modèle Task représentant une tâche associée à un projet.
    
    Relations:
    - Many-to-One avec Project (une tâche appartient à un projet)
    """
    __tablename__ = "tasks"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),  # Supprime la tâche si le projet est supprimé
        nullable=False
    )
    title = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False, default="TODO")  # TODO, IN_PROGRESS, DONE
    due_date = Column(Date, nullable=True)  # Date d'échéance
    
    # Relations
    # Many-to-One avec Project
    project = relationship(
        "Project",
        back_populates="tasks"
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
