from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class UserProfile(Base):
    """
    Modèle UserProfile représentant le profil d'un utilisateur.
    
    Relations:
    - One-to-One avec User (un profil appartient à un utilisateur unique)
    """
    __tablename__ = "user_profiles"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # Supprime le profil si l'utilisateur est supprimé
        unique=True,  # Assure la relation one-to-one
        nullable=False
    )
    bio = Column(String(500), nullable=True)  # Biographie de l'utilisateur
    phone_number = Column(String(20), nullable=True)  # Numéro de téléphone
    
    # Relations
    # One-to-One avec User
    user = relationship(
        "User",
        back_populates="profile"
    )
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"
