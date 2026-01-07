from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sae_samy_hugo:sae_samy_hugo@localhost:5432/sae_ddaw")

# Créer le moteur SQLAlchemy
# echo=True affiche les requêtes SQL dans le terminal (utile pour debug)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mettre False en production
    pool_pre_ping=True,  # Vérifie que la connexion est vivante avant de l'utiliser
    pool_size=10,  # Nombre de connexions dans le pool
    max_overflow=20  # Connexions supplémentaires si le pool est plein
)

# Créer une SessionLocal pour les requêtes DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles ORM
Base = declarative_base()


# Dependency pour injecter la session DB dans les routes FastAPI
def get_db():
    """
    Crée une session de base de données et la ferme automatiquement après utilisation.
    À utiliser comme dépendance dans les routes FastAPI avec Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fonction pour initialiser la base de données (créer les tables)
def init_db():
    """
    Crée toutes les tables définies dans les modèles.
    À utiliser uniquement en développement ou pour les tests.
    En production, utiliser Alembic pour les migrations.
    """
    from app.models import user, user_profile, project, task  # Import ici pour éviter les imports circulaires
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès")


# Fonction pour tester la connexion
def test_connection():
    """
    Teste la connexion à la base de données.
    """
    try:
        with engine.connect() as connection:
            # Utiliser text() pour les requêtes SQL brutes (SQLAlchemy 2.0+)
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            print("✅ Connexion à la base de données réussie!")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False
