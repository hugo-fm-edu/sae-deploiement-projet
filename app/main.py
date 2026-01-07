from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Configuration CORS (pour permettre les requêtes depuis le frontend si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
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


# TODO: Inclure les routers quand ils seront créés (Issues #5, #6, #10, #11)
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(projects.router, prefix="/projects", tags=["Projects"])
# app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
