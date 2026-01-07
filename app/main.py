from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import de la configuration DB
from app.database import get_db

# TODO: Importer les routes quand elles seront créées
# from app.routes import users, projects, tasks

app = FastAPI(
    title="SAE Project API",
    description="""
    API REST de gestion de projets collaboratifs développée avec FastAPI.
    
    ## Fonctionnalités
    
    * **Users** - Gestion des utilisateurs
    * **UserProfiles** - Profils utilisateurs (One-to-One)
    * **Projects** - Gestion des projets
    * **Tasks** - Gestion des tâches (One-to-Many avec Projects)
    * **Associations** - Utilisateurs ↔ Projets (Many-to-Many)
    
    ## Relations ORM implémentées
    
    * **One-to-One**: User ↔ UserProfile
    * **One-to-Many**: Project → Task
    * **Many-to-Many**: User ↔ Project
    """,
    version="1.0.0",
    contact={
        "name": "SAE DDAW - Sup Galilée",
    },
    license_info={
        "name": "MIT",
    },
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route de test pour vérifier que l'API fonctionne
@app.get("/", tags=["Root"])
def read_root():
    """
    Route de bienvenue pour vérifier que l'API est opérationnelle.
    """
    return {
        "message": "Bienvenue sur l'API de gestion de projets collaboratifs",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "running"
    }


# Route healthcheck (utile pour Docker)
@app.get("/health", tags=["Health"])
def health_check():
    """
    Route de healthcheck pour vérifier que l'API répond.
    Utilisé par Docker et les orchestrateurs.
    """
    return {"status": "healthy"}


# Route pour tester la connexion DB (mise à jour avec text())
@app.get("/db-test", tags=["Database"])
def test_database(db: Session = Depends(get_db)):
    """
    Route de test pour vérifier que la connexion à la base de données fonctionne.
    """
    try:
        # Exécuter une requête simple avec text() pour SQLAlchemy 2.0+
        result = db.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        return {
            "status": "success",
            "message": "Connexion à la base de données réussie!",
            "test_query_result": row[0]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur de connexion: {str(e)}"
        }


# Route de démo pour les schemas pédantic

# Import des schémas
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectWithTasks
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus


@app.post("/demo/projects", response_model=ProjectResponse, tags=["Demo - Schemas"])
def create_project_demo(project: ProjectCreate):
    """
    **Démonstration**: Créer un projet avec le schéma ProjectCreate.
    
    Teste la validation Pydantic sur: `name` et  `description` 
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "name": "Mon Projet",
        "description": "Description de mon projet"
    }
    ```
    """
    # Simulation d'une création (sans vraie DB)
    return ProjectResponse(
        id=1,
        name=project.name,
        description=project.description
    )


@app.get("/demo/projects/{project_id}", response_model=ProjectWithTasks, tags=["Demo - Schemas"])
def get_project_with_tasks_demo(project_id: int):
    """
    **Démonstration**: Récupérer un projet avec ses tâches.
    
    Teste le schéma ProjectWithTasks qui inclut:
    - Tous les champs de ProjectResponse
    - Une liste de TaskResponse (les tâches du projet)
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "name": "Mon Projet",
        "description": "Description",
        "tasks": [
            {
                "id": 1,
                "title": "Tâche 1",
                "status": "TODO",
                "due_date": "2026-02-15",
                "project_id": 1
            }
        ]
    }
    ```
    """
    # Simulation d'une récupération avec tâches
    return ProjectWithTasks(
        id=project_id,
        name="Mon Projet",
        description="Description de mon projet",
        tasks=[
            TaskResponse(
                id=1,
                title="Implémenter l'authentification",
                status=TaskStatus.IN_PROGRESS,
                due_date=None,
                project_id=project_id
            ),
            TaskResponse(
                id=2,
                title="Créer les routes API",
                status=TaskStatus.TODO,
                due_date=None,
                project_id=project_id
            )
        ]
    )


@app.post("/demo/tasks", response_model=TaskResponse, tags=["Demo - Schemas"])
def create_task_demo(task: TaskCreate):
    """
    **Démonstration**: Créer une tâche avec le schéma TaskCreate.
    
    Teste la validation Pydantic sur:
    - `title` (requis, 1-200 caractères)
    - `status` (enum: TODO, IN_PROGRESS, DONE) - défaut TODO
    - `due_date` (optionnel, format date YYYY-MM-DD)
    - `project_id` (requis, > 0)
    
    ### Énumérations supportées pour status:
    - `TODO` - Tâche à faire
    - `IN_PROGRESS` - Tâche en cours
    - `DONE` - Tâche terminée
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "title": "Créer les routes API",
        "status": "TODO",
        "due_date": "2026-02-20",
        "project_id": 1
    }
    ```
    """
    # Simulation d'une création
    return TaskResponse(
        id=1,
        title=task.title,
        status=task.status,
        due_date=task.due_date,
        project_id=task.project_id
    )


@app.get("/demo/task-status-enum", tags=["Demo - Schemas"])
def get_task_status_enum():
    """
    **Démonstration**: Récupérer tous les statuts possibles pour une tâche (Enum).
    
    L'énumération TaskStatus est disponible dans Swagger et validée automatiquement.
    
    ### Réponse:
    ```json
    {
        "available_statuses": ["TODO", "IN_PROGRESS", "DONE"],
        "description": "Ces valeurs sont les seules acceptées pour le champ 'status' des tâches"
    }
    ```
    """
    return {
        "available_statuses": [status.value for status in TaskStatus],
        "description": "Ces valeurs sont les seules acceptées pour le champ 'status' des tâches"
    }


# TODO: Inclure les routers quand ils seront créés (Issues #5, #6, #10, #11)
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(projects.router, prefix="/projects", tags=["Projects"])
# app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
