# SAE DDAW – API de gestion de projets collaboratifs (Python / FastAPI)

## Contexte et objectif

Ce projet s’inscrit dans le cadre de la SAE *Développement & Déploiement d’une Application Web RESTful Conteneurisée* (Sup Galilée).

L’objectif est de concevoir, développer et déployer une **API REST** permettant de gérer des **projets collaboratifs**, leurs **utilisateurs**, ainsi que les **tâches associées**, en respectant les bonnes pratiques de développement logiciel (architecture modulaire, persistance via ORM, conteneurisation, documentation, tests, etc.).

Le projet sera développé en **Python avec FastAPI**, persisté avec **PostgreSQL via SQLAlchemy**, et conteneurisé avec **Docker / Docker Compose**.

> ⚠️ Ce projet remplace la version Java/Spring Boot initiale, abandonnée en raison de multiples problèmes de configuration Maven/SDK.

---

## Fonctionnalités prévues (version initiale)

- Gestion des utilisateurs (création, consultation, mise à jour, suppression)
- Gestion des profils utilisateurs
- Gestion des projets
- Gestion des tâches associées à un projet
- Association des utilisateurs aux projets
- API REST documentée automatiquement via Swagger

---

## Modèle de données (prévisionnel)

### 🔹 User
- id
- name
- email

### 🔹 UserProfile
- id
- bio
- phoneNumber

### 🔹 Project
- id
- name
- description

### 🔹 Task
- id
- title
- status
- dueDate

---

## Relations ORM

Le projet implémente **les trois types de relations exigées** :

### One-to-One
- **User ↔ UserProfile**  
  Chaque utilisateur possède un unique profil.

### One-to-Many / Many-to-One
- **Project → Task**  
  Un projet peut contenir plusieurs tâches.  
  Une tâche appartient à un seul projet.

### Many-to-Many
- **User ↔ Project**  
  Un utilisateur peut participer à plusieurs projets.  
  Un projet peut avoir plusieurs utilisateurs.


---

## API REST – Routes envisagées

### Users
- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `PUT /users/{id}`
- `DELETE /users/{id}`

### Projects
- `POST /projects`
- `GET /projects`
- `GET /projects/{id}`
- `DELETE /projects/{id}`

### Tasks
- `POST /projects/{project_id}/tasks`
- `GET /tasks/{id}`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

---

## Base de données – Chargement des données de test

Un script SQL est disponible pour insérer des données de test dans la base de données.

### Données de test incluses

Le fichier `database/init_data.sql` contient :
- **5 utilisateurs** avec profils complets
- **3 projets** collaboratifs
- **10 tâches** réparties sur les projets
- **Associations** utilisateur-projet (Many-to-Many)

### Utilisation

**Méthode 1 : Avec Docker Compose (recommandé)**

```bash
# Copier le script dans le container
docker cp database/init_data.sql sae-db:/tmp/init_data.sql

# Exécuter le script
docker-compose exec db psql -U sae_samy_hugo -d sae_ddaw -f /tmp/init_data.sql
```

**Méthode 2 : en Local**

```bash
psql -U sae_samy_hugo -d sae_ddaw -f database/init_data.sql
```

**Méthode 3 : Via un autre outil**

1. Ouvrir le fichier `database/init_data.sql`
2. Copier le contenu
3. Exécuter dans l'outil de votre choix

---