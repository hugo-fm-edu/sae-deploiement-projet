# SAE DDAW – API de Gestion de Projets Collaboratifs

**Développement & Déploiement d'une Application Web RESTful Conteneurisée**  
*Sup Galilée - École d'Ingénieurs de l'Université Sorbonne Paris Nord*

---

## Table des matières

1. [Contexte et objectifs](#contexte-et-objectifs)
2. [Fonctionnalités implémentées](#fonctionnalités-implémentées)
3. [Technologies utilisées](#technologies-utilisées)
4. [Modèle de données](#modèle-de-données)
5. [Architecture du projet](#architecture-du-projet)
6. [Installation et lancement](#installation-et-lancement)
7. [Exemples de routes API](#exemples-de-routes-api)
8. [Tests avec Postman](#tests-avec-postman)
9. [Docker Hub](#docker-hub)
10. [Jeu de données de test](#jeu-de-données-de-test)
11. [Documentation Swagger](#documentation-swagger)

---

## Contexte et objectifs

### Le problème résolu

Les organisations modernes ont besoin de **gérer efficacement des projets collaboratifs** avec plusieurs utilisateurs, des tâches assignées et une vue d'ensemble des progressions. Cette API REST répond à ce besoin en offrant un backend robuste, documenté et conteneurisé.

### Objectifs pédagogiques

- Concevoir une **architecture logicielle modulaire** et scalable
- Implémenter une **API REST conforme aux standards HTTP**
- Maîtriser la **persistance de données** avec un ORM (SQLAlchemy)
- Implémenter les **trois types de relations** de base de données
- **Conteneuriser** l'application avec Docker
- Orchestrer les services avec Docker Compose
- Documenter et tester l'API

### Stack technique

- **Backend** : Python 3.11 + FastAPI
- **Base de données** : PostgreSQL 15
- **ORM** : SQLAlchemy 2.0
- **Conteneurisation** : Docker + Docker Compose
- **Documentation** : Swagger/OpenAPI + Postman

---

## Fonctionnalités implémentées

### Gestion des utilisateurs
- Créer un nouvel utilisateur
- Lister tous les utilisateurs
- Récupérer un utilisateur par son ID
- Mettre à jour un utilisateur
- Supprimer un utilisateur

### Gestion des profils utilisateurs
- Créer un profil pour un utilisateur (One-to-One)
- Consulter le profil d'un utilisateur
- Mettre à jour le profil

### Gestion des projets
- Créer un projet
- Lister tous les projets avec pagination
- Récupérer les détails d'un projet avec ses tâches
- Mettre à jour un projet
- Supprimer un projet

### Gestion des tâches
- Créer une tâche pour un projet
- Lister les tâches d'un projet
- Récupérer une tâche par son ID
- Mettre à jour une tâche (titre, statut, date limite)
- Supprimer une tâche

### Gestion des associations utilisateur-projet
- Assigner un utilisateur à un projet
- Retirer un utilisateur d'un projet
- Lister les utilisateurs d'un projet
- Lister les projets d'un utilisateur

### Documentation et accessibilité
- **Swagger/OpenAPI** automatiquement généré : `GET /docs`
- Docstrings détaillées pour chaque endpoint
- Codes HTTP appropriés (201, 204, 400, 404, 500)
- Messages d'erreur explicites

---

## Technologies utilisées

| Composant | Technologie | Version | Justification |
|-----------|-----------|---------|---------------|
| **Framework Web** | FastAPI | 0.115.6 | API REST moderne, documentation auto, validation intégrée |
| **Serveur ASGI** | Uvicorn | 0.34.0 | Serveur ASGI performant pour FastAPI |
| **Langage** | Python | 3.11 | Syntaxe claire, écosystème riche, facile à déployer |
| **ORM** | SQLAlchemy | 2.0.36 | Abstraction DB robuste, relations complexes, migrations |
| **Base de données** | PostgreSQL | 15-alpine | SGBDR puissant, fiable, image Docker légère |
| **Connecteur DB** | psycopg2-binary | 2.9.10 | Driver PostgreSQL pour SQLAlchemy |
| **Migrations DB** | Alembic | 1.14.0 | Versioning des schémas DB, rollback facile |
| **Validation** | Pydantic | 2.10.6 | Validation des données, sérialisation JSON |
| **Variables d'env** | python-dotenv | 1.0.1 | Configuration flexible, secrets en local |
| **Conteneurisation** | Docker | Latest | Isolation, reproductibilité, déploiement simplifié |
| **Orchestration** | Docker Compose | 3.9 | Gestion multi-conteneurs, réseau, volumes |
| **Tests API** | Postman | - | GUI pour tests manuels, collections partageables |

---

## Modèle de données

### Diagramme des relations

```
┌──────────────────────────────────────────────────────────┐
│                    MODÈLE DE DONNÉES                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  User ──────[1..1]────── UserProfile                   │
│  (One-to-One avec cascade delete)                       │
│                                                          │
│  Project ──────[1..∞]────── Task                        │
│  (One-to-Many avec cascade delete)                      │
│                                                          │
│  User ──────[∞..∞]────── Project                        │
│  (Many-to-Many via table user_project)                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Entités et attributs

#### 🔹 User (Utilisateur)
```sql
id              INTEGER         PRIMARY KEY
name            VARCHAR(100)    NOT NULL
email           VARCHAR(255)    UNIQUE, NOT NULL
profile         OneToOne        → UserProfile
projects        ManyToMany      → Project
```

#### 🔹 UserProfile (Profil Utilisateur)
```sql
id              INTEGER         PRIMARY KEY
user_id         INTEGER         FOREIGN KEY → User (CASCADE)
bio             TEXT            
phone_number    VARCHAR(20)
```

**Relation One-to-One** : Chaque utilisateur possède exactement un profil unique.

#### 🔹 Project (Projet)
```sql
id              INTEGER         PRIMARY KEY
name            VARCHAR(200)    NOT NULL
description     TEXT
users           ManyToMany      → User
tasks           OneToMany       → Task
```

#### 🔹 Task (Tâche)
```sql
id              INTEGER         PRIMARY KEY
project_id      INTEGER         FOREIGN KEY → Project (CASCADE)
title           VARCHAR(255)    NOT NULL
status          VARCHAR(20)     [TODO, IN_PROGRESS, DONE]
due_date        DATE
```

**Relation One-to-Many** : Un projet peut avoir plusieurs tâches. Une tâche appartient à un seul projet.

#### 🔹 user_project (Table d'association)
```sql
user_id         INTEGER         FOREIGN KEY → User
project_id      INTEGER         FOREIGN KEY → Project
```

**Relation Many-to-Many** : Un utilisateur peut participer à plusieurs projets. Un projet peut avoir plusieurs utilisateurs.

---

## Architecture du projet

### Arborescence des dossiers

```
sae-deploiement-projet/
│
├── app/                          # Code source de l'application
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée FastAPI, configuration CORS
│   │
│   ├── database/                 # Configuration base de données
│   │   ├── __init__.py
│   │   ├── db.py                 # Engine SQLAlchemy, SessionLocal, dependency
│   │   └── init_data.sql         # Script d'initialisation avec données de test
│   │
│   ├── models/                   # Modèles ORM SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py               # Entité User avec relations
│   │   ├── user_profile.py       # Entité UserProfile (One-to-One)
│   │   ├── project.py            # Entité Project
│   │   ├── task.py               # Entité Task (One-to-Many)
│   │   └── user_project.py       # Table d'association Many-to-Many
│   │
│   ├── schemas/                  # Schémas Pydantic (validation + sérialisation)
│   │   ├── __init__.py
│   │   ├── user.py               # UserCreate, UserUpdate, UserResponse
│   │   ├── user_profile.py       # ProfileCreate, ProfileUpdate, ProfileResponse
│   │   ├── project.py            # ProjectCreate, ProjectUpdate, ProjectResponse
│   │   └── task.py               # TaskCreate, TaskUpdate, TaskResponse
│   │
│   └── routes/                   # Routeurs FastAPI (contrôleurs)
│       ├── __init__.py
│       ├── users.py              # Endpoints /users
│       ├── projects.py           # Endpoints /projects
│       └── task.py               # Endpoints /tasks
│
├── alembic/                      # Migrations de base de données (Alembic)
│   ├── env.py
│   ├── versions/
│   │   └── 2b6d6603d08a_*.py    # Migrations versionnées
│   └── script.py.mako
│
├── postman/                      # Collections de tests Postman
│   └── sae-api.json
│   └── environment.json
│
├── Dockerfile                    # Image Docker de l'API
├── docker-compose.yml            # Orchestration multi-conteneurs
├── alembic.ini                   # Configuration Alembic
├── requirements.txt              # Dépendances Python                     
└── README.md
```

### Flux de requête

```
1. Client HTTP (Postman, curl, navigateur)
   ↓
2. FastAPI (app/main.py) 
   ├─ Routing (app/routes/*.py)
   │  ├─ Validation Pydantic (app/schemas/*.py)
   │  ├─ Logique métier
   │  └─ Appels DB via SQLAlchemy
   │     ↓
   ├─ SQLAlchemy ORM (app/models/*.py)
   │  └─ Session DB
   │     ↓
   └─ PostgreSQL (via connexion psycopg2)
      ↓
3. Response JSON avec Swagger docs auto
```

---

## Installation et lancement

### Prérequis

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- (Optionnel) **Python** 3.11+ si vous voulez lancer sans Docker

### Option 1 : Lancement avec Docker Compose (recommandé)

#### Étape 1 : Cloner le projet

```bash
git clone https://github.com/hugo-fm-edu/sae-deploiement-projet.git
cd sae-deploiement-projet
```

#### Étape 2 : Démarrer les conteneurs

```bash
docker compose up -d #ou avec docker-compose
```

**Ce qu'il se passe :**
- 🐘 **PostgreSQL 15** démarre et attend les connexions
- 🔧 Health check : l'API attendra que la DB soit prête
- 🚀 **FastAPI** démarre sur `http://localhost:8000`

#### Étape 3 : Charger les données de test

```bash
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -f /app/database/init_data.sql  #ou avec docker-compose
```

Ou avec le chemin local :

```bash
psql -U sae_samy_hugo -d sae_ddaw -h localhost \
  -f app/database/init_data.sql
```

#### Étape 4 : Vérifier que tout fonctionne

```bash
# Lister les utilisateurs
curl http://localhost:8000/users

# Accédez à la documentation Swagger
# Ouvrez dans votre navigateur : http://localhost:8000/docs
```

#### Arrêter et nettoyer

```bash
# Arrêter les conteneurs
docker compose down #ou avec docker-compose

# Arrêter et supprimer les volumes (réinitialiser la DB)
docker compose down -v #ou avec docker-compose
```

---

### Option 2 : Lancement en local (Python natif)

#### Prérequis

- Python 3.11+
- PostgreSQL en local (ou Docker uniquement pour la DB)

#### Étapes

1. **Créer un environnement virtuel**

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Configurer la base de données**

Si PostgreSQL tourne en Docker :
```bash
docker run --name postgres_dev \
  -e POSTGRES_USER=sae_samy_hugo \
  -e POSTGRES_PASSWORD=sae_samy_hugo \
  -e POSTGRES_DB=sae_ddaw \
  -p 5432:5432 \
  -d postgres:15-alpine
```

4. **Créer un fichier `.env`**

```env
DATABASE_URL=postgresql://sae_samy_hugo:sae_samy_hugo@localhost:5432/sae_ddaw
```

5. **Lancer l'API**

```bash
uvicorn app.main:app --reload
```

L'API est disponible à `http://localhost:8000`

---

## Exemples de routes API

### Tableau récapitulatif

| Méthode | Endpoint | Description | Status |
|---------|----------|-------------|--------|
| **POST** | `/users` | Créer un nouvel utilisateur | 201 |
| **GET** | `/users` | Lister tous les utilisateurs | 200 |
| **GET** | `/users/{id}` | Récupérer un utilisateur | 200 |
| **PUT** | `/users/{id}` | Mettre à jour un utilisateur | 200 |
| **DELETE** | `/users/{id}` | Supprimer un utilisateur | 204 |
| **POST** | `/users/{id}/profile` | Créer le profil d'un utilisateur | 201 |
| **GET** | `/users/{id}/profile` | Récupérer le profil d'un utilisateur | 200 |
| **PUT** | `/users/{id}/profile` | Mettre à jour le profil | 200 |
| **POST** | `/projects` | Créer un projet | 201 |
| **GET** | `/projects/` | Lister tous les projets | 200 |
| **GET** | `/projects/{id}` | Récupérer un projet avec ses tâches | 200 |
| **PUT** | `/projects/{id}` | Mettre à jour un projet | 200 |
| **DELETE** | `/projects/{id}` | Supprimer un projet | 204 |
| **POST** | `/projects/{id}/users` | Assigner un utilisateur au projet | 201 |
| **DELETE** | `/projects/{id}/users/{uid}` | Retirer un utilisateur du projet | 204 |
| **POST** | `/tasks` | Créer une tâche | 201 |
| **GET** | `/tasks/{id}` | Récupérer une tâche | 200 |
| **PUT** | `/tasks/{id}` | Mettre à jour une tâche | 200 |
| **DELETE** | `/tasks/{id}` | Supprimer une tâche | 204 |

### Exemples de requêtes

#### 1. Créer un utilisateur

**Request :**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Dupont",
    "email": "alice.dupont@example.com"
  }'
```

**Response (201 Created) :**
```json
{
  "id": 1,
  "name": "Alice Dupont",
  "email": "alice.dupont@example.com"
}
```

---

#### 2. Créer un profil utilisateur (One-to-One)

**Request :**
```bash
curl -X POST http://localhost:8000/users/1/profile \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Développeur Python passionné",
    "phone_number": "+33 6 12 34 56 78"
  }'
```

**Response (201 Created) :**
```json
{
  "id": 1,
  "user_id": 1,
  "bio": "Développeur Python passionné",
  "phone_number": "+33 6 12 34 56 78"
}
```

---

#### 3. Créer un projet

**Request :**
```bash
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API REST FastAPI",
    "description": "Développement d'\''une API avec FastAPI et PostgreSQL"
  }'
```

**Response (201 Created) :**
```json
{
  "id": 1,
  "name": "API REST FastAPI",
  "description": "Développement d'une API avec FastAPI et PostgreSQL"
}
```

---

#### 4. Créer une tâche (One-to-Many)

**Request :**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "title": "Implémenter les routes CRUD",
    "status": "IN_PROGRESS",
    "due_date": "2026-02-15"
  }'
```

**Response (201 Created) :**
```json
{
  "id": 1,
  "project_id": 1,
  "title": "Implémenter les routes CRUD",
  "status": "IN_PROGRESS",
  "due_date": "2026-02-15"
}
```

---

#### 5. Assigner un utilisateur à un projet (Many-to-Many)

**Request :**
```bash
curl -X POST http://localhost:8000/projects/1/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

**Response (201 Created) :**
```json
{
  "message": "Utilisateur assigné au projet"
}
```

---

#### 6. Récupérer un projet avec ses tâches et utilisateurs

**Request :**
```bash
curl http://localhost:8000/projects/1
```

**Response (200 OK) :**
```json
{
  "id": 1,
  "name": "API REST FastAPI",
  "description": "Développement d'une API avec FastAPI et PostgreSQL",
  "tasks": [
    {
      "id": 1,
      "title": "Implémenter les routes CRUD",
      "status": "IN_PROGRESS",
      "due_date": "2026-02-15",
      "project_id": 1
    }
  ],
  "users": [
    {
      "id": 1,
      "name": "Alice Dupont",
      "email": "alice.dupont@example.com"
    }
  ]
}
```

---

#### 7. Lister tous les utilisateurs

**Request :**
```bash
curl http://localhost:8000/users
```

**Response (200 OK) :**
```json
[
  {
    "id": 1,
    "name": "Alice Dupont",
    "email": "alice.dupont@example.com"
  },
  {
    "id": 2,
    "name": "Bob Martin",
    "email": "bob.martin@example.com"
  }
]
```

---

#### 8. Supprimer un utilisateur

**Request :**
```bash
curl -X DELETE http://localhost:8000/users/1
```

**Response (204 No Content) :**
```
(pas de body, juste le code 204)
```

---

## Tests avec Postman

### Importer la collection

1. **Télécharger Postman** : https://www.postman.com/downloads/
2. **Importer la collection** :
   - Ouvrir Postman
   - Cliquer sur **"Import"**
   - Sélectionner le fichier `postman/sae-api.json`
   - La collection s'affiche complètement organisée en dossiers
3. **Importer l'environnement** :
   - Aller dans la section **Environnement**
   - - Cliquer sur **"Import"**
   - Sélectionner le fichier `postman/environment.json`

### Structure de la collection

La collection contient 3 dossiers principales:

- **Users** : Gestion des utilisateurs et leurs profils (CRUD + One-to-One)
- **Projects** : Gestion des projets et assignation des utilisateurs (CRUD + Many-to-Many)
- **Tasks** : Gestion des tâches des projets (CRUD + One-to-Many)

### Variables d'environnement Postman

La collection utilise les variables d'environnement suivantes :

```json
{
  "base_url": "http://localhost:8000",
  "user_id": "1",
  "project_id": "1",
  "task_id": "1"
}
```

Ces variables sont déjà intégrées dans les requêtes de la collection (syntaxe `{{base_url}}`, `{{user_id}}`, etc). Vous pouvez les modifier après chaque création de ressource pour tester les opérations dépendantes.

### Ordre de test recommandé

1. **Users** : Créer un utilisateur (POST /users) et copier son ID
2. **User Profiles** : Créer un profil pour cet utilisateur (POST /users/{id}/profile)
3. **Projects** : Créer un projet (POST /projects) et copier son ID
4. **Project-Users** : Assigner l'utilisateur au projet (POST /projects/{id}/users)
5. **Tasks** : Créer une tâche pour le projet (POST /tasks)
6. **Consultations** : Vérifier les relations dans les réponses (GET endpoints)

---

## Docker Hub

### Image disponible

**Docker Hub Repository** : [samykb147/sae-api-project](https://hub.docker.com/r/samykb147/sae-api-project)

### Récupérer l'image Docker

L'image est disponible avec deux tags :

```bash
# images versionnées (la dérnière est v4.0.O)
docker pull samykb147/sae-api-project:v4.0.0

# Version latest (dernière version)
docker pull samykb147/sae-api-project:latest
```

---

## Jeu de données de test

### Contenu du script `init_data.sql`

Le script prépopule la base avec :

- **5 utilisateurs** : Jean Dupont, Marie Martin, Pierre Durand, Sophie Bernard, Lucas Petit
- **5 profils utilisateurs** : bio + numéro de téléphone pour chaque utilisateur
- **3 projets** : API REST, Application Mobile e-commerce, Plateforme e-learning
- **10 tâches** : réparties entre les projets avec différents statuts (TODO, IN_PROGRESS, DONE)
- **8 associations user-project** : chaque utilisateur participe à au moins un projet

### Charger les données

**Avec Docker Compose** :

```bash
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -f /app/database/init_data.sql
```

**Avec PostgreSQL local** :

```bash
psql -U sae_samy_hugo -d sae_ddaw \
  -h localhost \
  -f app/database/init_data.sql
```

**Ou via l'interface psql** :

```bash
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw

# Dans psql :
\i /app/database/init_data.sql
```

### Identifiants de test

```sql
-- Utilisateurs de test
Email: jean.dupont@example.com
Email: marie.martin@example.com
Email: pierre.durand@example.com

-- Projets
ID 1: API de gestion de projets
ID 2: Application mobile e-commerce
ID 3: Plateforme d'apprentissage en ligne

-- Statuts de tâches
TODO           → À faire
IN_PROGRESS    → En cours
DONE           → Terminée
```

### Vérifier les données chargées

```bash
# Lister les utilisateurs
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -c "SELECT * FROM users;"

# Lister les projets
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -c "SELECT * FROM projects;"

# Lister les tâches
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -c "SELECT * FROM tasks;"

# Vérifier les associations user-project
docker compose exec db psql -U sae_samy_hugo -d sae_ddaw \
  -c "SELECT * FROM user_project;"
```

---

## Documentation Swagger

### Accéder à Swagger

Une fois l'API lancée, ouvrez dans votre navigateur :

```
http://localhost:8000/docs
```

**Vous verrez :**
- Tous les endpoints organisés par tags (Users, Projects, Tasks)
- Descriptions détaillées et docstrings
- Exemples de requêtes et réponses
- Codes HTTP et erreurs possibles
- Interface interactive pour tester directement


### Schéma OpenAPI JSON

Pour intégrer avec d'autres outils :

```
http://localhost:8000/openapi.json
```


---

## Variables d'environnement

### Fichier `.env.example`

```env
# Configuration de la base de données
DATABASE_URL=postgresql://sae_samy_hugo:sae_samy_hugo@localhost:5432/sae_ddaw

# Configuration de l'application
APP_ENV=development
DEBUG=True

# PostgreSQL (pour Docker Compose)
POSTGRES_USER=sae_samy_hugo
POSTGRES_PASSWORD=sae_samy_hugo
POSTGRES_DB=sae_ddaw
```

### Utilisation

1. Copier `.env.example` → `.env`
2. Adapter les valeurs pour votre environnement
3. `.env` est dans `.gitignore` (secrets ne sont pas committés)

---


## Notes sur l'implémentation

### Relations ORM

- **One-to-One (User ↔ UserProfile)** : Cascade delete activée. Supprimer un User supprime aussi son UserProfile.
- **One-to-Many (Project → Task)** : Cascade delete activée. Supprimer un Project supprime toutes ses Tasks.
- **Many-to-Many (User ↔ Project)** : Table d'association `user_project`. Relation bidirectionnelle avec `back_populates`.

### Gestion d'erreurs

Tous les endpoints retournent :
- **201 Created** pour les créations
- **200 OK** pour les lectures/mises à jour
- **204 No Content** pour les suppressions
- **400 Bad Request** pour les erreurs de validation
- **404 Not Found** pour les ressources inexistantes
- **500 Internal Server Error** pour les erreurs serveur

### Validation

Pydantic valide automatiquement les données entrantes via les schemas.


---

## Licence

MIT License - Libre d'utilisation à titre pédagogique et professionnel.

---

## Auteurs

**Auteurs** : MEHAMLI Samy, FERREIRA MIGUEL Hugo



**Dépôt GitHub** : [hugo-fm-edu/sae-deploiement-projet](https://github.com/hugo-fm-edu/sae-deploiement-projet)

**Image Docker Hub** : [samykb147/sae-api-project](https://hub.docker.com/r/samykb147/sae-api-project)
| Contrainte | Statut | Détail |
|-----------|--------|--------|
| API REST conforme HTTP | ✅ | GET, POST, PUT, DELETE, codes HTTP |
| Backend Python/FastAPI | ✅ | FastAPI 0.115.6 |
| BD relationnelle PostgreSQL | ✅ | PostgreSQL 15-alpine |
| ORM SQLAlchemy | ✅ | SQLAlchemy 2.0 |
| One-to-One | ✅ | User ↔ UserProfile |
| One-to-Many | ✅ | Project → Task |
| Many-to-Many | ✅ | User ↔ Project (via user_project) |
| Docker + Docker Compose | ✅ | Dockerfile + docker-compose.yml |
| Documentation Swagger | ✅ | Automatique via FastAPI |
| Tests API | ✅ | Collection Postman fournie |
| Script données test | ✅ | init_data.sql avec 5 users, 3 projects, 10 tasks |
| Docker Hub | ✅ | Image à publier (lien TBD) |
| README complet | ✅ | Ce fichier |
| GitHub repo public | ✅ | (https://github.com/hugo-fm-edu/sae-deploiement-projet) |
