from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.project import Project
from app.models.task import Task
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

# configurer le routeur
router = APIRouter(prefix="/tasks", tags=["tasks"])

# POST /projects/{project_id}/tasks - créer tâche dans un projet
@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une nouvelle tâche dans un projet",
    description="Crée une nouvelle tâche associée à un projet spécifique (relation One-to-Many)"
)
def create_task_in_project(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Créer une nouvelle tâche dans un projet.
    
    - **project_id**: ID du projet auquel appartient la tâche
    - **title**: Titre de la tâche (obligatoire, 1-200 caractères)
    - **status**: Statut de la tâche (TODO, IN_PROGRESS, DONE) - défaut: TODO
    - **due_date**: Date d'échéance (optionnelle, format: YYYY-MM-DD)
    
    Le project_id dans l'URL et dans le body doivent correspondre.
    
    Retourne une erreur 404 si le projet n'existe pas.
    Retourne une erreur 400 si les project_id ne correspondent pas.
    """
    # verifier que le projet existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec id {project_id} non trouvé."
        )
    #verifier que les project_id correspondent
    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le project_id dans l'URL et dans le body doivent correspondre."
        )
    # creer la tache
    new_task = Task(
        title=task.title,
        status=task.status,
        due_date=task.due_date,
        project_id=project_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# GET /tasks/{task_id} - Récupérer une tâche
@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Récupérer une tâche par son ID",
    description="Récupère les détails d'une tâche spécifique par son ID"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupérer une tâche spécifique par son ID.
    
    - **task_id**: ID de la tâche
    
    Retourne une erreur 404 si la tâche n'existe pas.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée."
        )
    return task

# PUT /tasks/{task_id} - Mettre à jour une tâche
@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Mettre à jour une tâche par son ID",
    description="Met à jour les détails d'une tâche (titre, statut, date d'échéance)"
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour une tâche existante.
    
    - **task_id**: ID de la tâche à modifier
    - **title**: Nouveau titre (optionnel)
    - **status**: Nouveau statut (optionnel)
    - **due_date**: Nouvelle date d'échéance (optionnel)
    
    Retourne une erreur 404 si la tâche n'existe pas.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée."
        )
    # mettre à jour les champs si fournis
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.due_date is not None:
        task.due_date = task_update.due_date

    db.commit()
    db.refresh(task)

    return task

# DELETE /tasks/{task_id} - Supprimer une tâche
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une tâche par son ID",
    description="Supprime une tâche spécifique par son ID"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprimer une tâche spécifique par son ID.
    
    - **task_id**: ID de la tâche à supprimer
    
    Retourne une erreur 404 si la tâche n'existe pas.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée."
        )
    db.delete(task)
    db.commit()
    return

# GET /tasks - Lister toutes les tâches (bonus)
@router.get(
    "",
    response_model=List[TaskResponse],
    summary="Lister toutes les tâches",
    description="Récupère une liste de toutes les tâches existantes"
)
def list_all_tasks(
    project_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Récupérer une liste de toutes les tâches.
    
    - **project_id**: (optionnel) Filtrer les tâches par ID de projet
    """

    #filtrer par project_id si fourni
    if project_id is not None:
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
    else:
        tasks = db.query(Task).all()
    return tasks