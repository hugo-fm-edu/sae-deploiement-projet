from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectWithTasks
from app.schemas.task import TaskResponse

# configurer le routeur
router = APIRouter(prefix="/projects", tags=["projects"])

# POST /projects - Créer un projet 
@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau projet",
    description="Crée un nouveau projet avec un nom et une description optionnelle"
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Crée un nouveau projet
    
    - **name**: Nom du projet (obligatoire, 1-100 caractères)
    - **description**: Description du projet (optionnelle, max 500 caractères)
    """
    # Créer l'objet projet
    db_project = Project(
        name=project.name,
        description=project.description
    )
    # Ajouter a la BDD 
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# GET /projects - Lister tous les projets
@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Lister tous les projets",
    description="Récupère la liste de tous les projets"
)
def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les projets

    - **skip**: Nombre de projets à ignorer (pour la pagination)
    - **limit**: Nombre maximum de projets à retourner
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


# GET /projects/{id} - Récupérer un projet avec ses tâches
@router.get(
    "/{project_id}",
    response_model=ProjectWithTasks,
    summary="Récupérer un projet avec ses tâches",
    description="Récupère les détails d'un projet et toutes ses tâches"
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer un projet spécifique avec toutes ses tâches.
    
    - **project_id**: ID du projet
    
    Retourne une erreur 404 si le projet n'existe pas.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    
    return project


# PUT /projects/{id} - Mettre à jour un projet
@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Mettre à jour un projet",
    description="Met à jour les détails d'un projet"
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un projet existant.
    
    - **project_id**: ID du projet à modifier
    - **name**: Nouveau nom (optionnel)
    - **description**: Nouvelle description (optionnel)
    
    Retourne une erreur 404 si le projet n'existe pas.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    
    # Mettre à jour les champs si fournis car optionnel
    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description
    
    db.commit()
    db.refresh(project)
    return project

# DELETE /projects/{id} - Supprimer un projet
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un projet",
    description="Supprime un projet et toutes ses tâches associées"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer un projet.
    
    - **project_id**: ID du projet à supprimer
    
    - **Attention**: Cette action supprime également toutes les tâches associées.
    
    Retourne une erreur 404 si le projet n'existe pas.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    
    db.delete(project)
    db.commit()
    return None


# POST /projects/{id}/users/{user_id} - Ajouter un utilisateur au projet
@router.post(
    "/{project_id}/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Ajouter un utilisateur au projet",
    description="Associe un utilisateur à un projet (relation Many-to-Many)"
)
def add_user_to_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Associer un utilisateur à un projet (relation Many-to-Many).
    
    - **project_id**: ID du projet
    - **user_id**: ID de l'utilisateur à ajouter
    
    Retourne une erreur 404 si le projet ou l'utilisateur n'existe pas.
    Retourne une erreur 400 si l'utilisateur est déjà assigné au projet.
    """
    # Vérifier que le projet existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'ID {user_id} non trouvé"
        )
    
    # Vérifier que l'utilisateur n'est pas déjà associé
    if user in project.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utilisateur est déjà associé à ce projet"
        )
    
    # Ajouter l'utilisateur
    project.users.append(user)
    db.commit()
    
    return {"message": f"Utilisateur {user_id} ajouté au projet {project_id}"}


# DELETE /projects/{id}/users/{user_id} - Retirer un utilisateur du projet
@router.delete(
    "/{project_id}/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Retirer un utilisateur du projet",
    description="Désassocie un utilisateur d'un projet (relation Many-to-Many)"
)
def remove_user_from_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retirer un utilisateur d'un projet.
    
    - **project_id**: ID du projet
    - **user_id**: ID de l'utilisateur à retirer
    
    Retourne une erreur 404 si le projet, l'utilisateur ou l'association n'existe pas.
    """
    # Vérifier que le projet existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    
    # Vérifier que l'user existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'ID {user_id} non trouvé"
        )
    
    # Vérifier que le user est associé a ce projet
    if user not in project.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utilisateur n'est pas associé à ce projet"
        )
    
    # Retirer le user de ce projet
    project.users.remove(user)
    db.commit()
    
    return {"message": f"Utilisateur {user_id} retiré du projet {project_id}"}


# GET /projects/{id}/users - Lister les utilisateurs du projet
@router.get(
    "/{project_id}/users",
    response_model=dict,
    summary="Lister les utilisateurs d'un projet",
    description="Récupère la liste de tous les utilisateurs associés à un projet"
)
def get_project_users(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des utilisateurs assignés à un projet.
    
    - **project_id**: ID du projet
    
    Retourne une erreur 404 si le projet n'existe pas.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    # Verifier que le projet existe
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )
    #retourner la liste des users associés a ce projet
    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in project.users
    ]
    
    return {
        "project_id": project_id,
        "project_name": project.name,
        "users_count": len(project.users),
        "users": users_data
    }