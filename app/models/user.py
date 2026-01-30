from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base


class User(Base):
    """
    Modèle User représentant un utilisateur du système.
    
    Relations:
    - One-to-One avec UserProfile (un utilisateur a un profil unique)
    - Many-to-Many avec Project (un utilisateur peut participer à plusieurs projets)
    """
    __tablename__ = "users"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relations
    # One-to-One avec UserProfile
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,  # Indique qu'il s'agit d'une relation one-to-one
        cascade="all, delete-orphan"  # Supprime le profil si l'utilisateur est supprimé
    )
    
    # Many-to-Many avec Project via la table d'association user_project
    projects = relationship(
        "Project",
        secondary="user_project",  # Table d'association
        back_populates="users"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
