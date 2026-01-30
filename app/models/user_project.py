from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.db import Base

# Table d'association pour la relation Many-to-Many entre User et Project
user_project = Table(
    'user_project',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True)
)
