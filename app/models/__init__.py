from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.project import Project
from app.models.task import Task
from app.models.user_project import user_project

# Exporter tous les modèles pour faciliter les imports
__all__ = ["User", "UserProfile", "Project", "Task", "user_project"]