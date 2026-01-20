-- ============================================
-- SCRIPT D'INITIALISATION DES DONNÉES DE TEST
-- ============================================
-- 
-- Ce script insère des données de test dans la base de données
-- pour faciliter les tests manuels de l'API.
--
-- UTILISATION:
-- psql -U sae_samy_hugo -d sae_ddaw -f database/init_data.sql
--
-- Ou via docker-compose:
-- docker-compose exec db psql -U sae_samy_hugo -d sae_ddaw -f /docker-entrypoint-initdb.d/init_data.sql
--
-- ============================================

-- Nettoyage des données existantes (optionnel, à décommenter si besoin)
-- TRUNCATE TABLE user_project, tasks, user_profiles, projects, users RESTART IDENTITY CASCADE;

-- ============================================
-- 1. INSERTION DES UTILISATEURS (5 utilisateurs)
-- ============================================

INSERT INTO users (name, email) VALUES
('Jean Dupont', 'jean.dupont@example.com'),
('Marie Martin', 'marie.martin@example.com'),
('Pierre Durand', 'pierre.durand@example.com'),
('Sophie Bernard', 'sophie.bernard@example.com'),
('Lucas Petit', 'lucas.petit@example.com');

-- ============================================
-- 2. INSERTION DES PROFILS UTILISATEURS (5 profils)
-- Relation One-to-One avec Users
-- ============================================

INSERT INTO user_profiles (user_id, bio, phone_number) VALUES
(1, 'Développeur Full Stack passionné par Python et FastAPI. 5 ans d''expérience en développement web.', '+33 6 12 34 56 78'),
(2, 'Chef de projet avec 10 ans d''expérience dans la gestion de projets agiles.', '+33 6 23 45 67 89'),
(3, 'Développeur Frontend spécialisé en React et Vue.js. Amateur de design UX/UI.', '+33 6 34 56 78 90'),
(4, 'Data Scientist experte en Machine Learning et analyse de données.', '+33 6 45 67 89 01'),
(5, 'DevOps Engineer passionné par Docker, Kubernetes et l''automatisation.', '+33 6 56 78 90 12');

-- ============================================
-- 3. INSERTION DES PROJETS (3 projets)
-- ============================================

INSERT INTO projects (name, description) VALUES
('API de gestion de projets', 'Développement d''une API REST avec FastAPI pour gérer des projets collaboratifs. Inclut authentification, gestion des tâches et documentation Swagger.'),
('Application mobile e-commerce', 'Application mobile cross-platform pour une boutique en ligne. Intégration avec Stripe pour les paiements.'),
('Plateforme d''apprentissage en ligne', 'Plateforme web pour créer et suivre des cours en ligne. Fonctionnalités de quiz, vidéos et tracking de progression.');

-- ============================================
-- 4. INSERTION DES TÂCHES (10 tâches)
-- Relation One-to-Many avec Projects
-- ============================================

-- Tâches pour le Projet 1 (API de gestion de projets)
INSERT INTO tasks (project_id, title, status, due_date) VALUES
(1, 'Créer les modèles ORM SQLAlchemy', 'DONE', '2026-01-15'),
(1, 'Implémenter les routes CRUD pour les utilisateurs', 'DONE', '2026-01-20'),
(1, 'Ajouter l''authentification JWT', 'IN_PROGRESS', '2026-01-25'),
(1, 'Documenter l''API avec Swagger', 'TODO', '2026-02-01'),

-- Tâches pour le Projet 2 (Application mobile e-commerce)
(2, 'Créer les maquettes UI/UX', 'DONE', '2026-01-10'),
(2, 'Développer le système de panier', 'IN_PROGRESS', '2026-01-22'),
(2, 'Intégrer l''API de paiement Stripe', 'TODO', '2026-01-30'),

-- Tâches pour le Projet 3 (Plateforme d''apprentissage)
(3, 'Mettre en place le système de gestion des cours', 'IN_PROGRESS', '2026-01-18'),
(3, 'Développer le lecteur vidéo intégré', 'TODO', '2026-02-05'),
(3, 'Créer le système de quiz interactifs', 'TODO', '2026-02-15');

-- ============================================
-- 5. ASSOCIATIONS UTILISATEUR-PROJET (Many-to-Many)
-- Table d'association user_project
-- ============================================

INSERT INTO user_project (user_id, project_id) VALUES
-- Jean Dupont travaille sur les projets 1 et 2
(1, 1),
(1, 2),

-- Marie Martin travaille sur les 3 projets (chef de projet)
(2, 1),
(2, 2),
(2, 3),

-- Pierre Durand travaille sur le projet 2
(3, 2),

-- Sophie Bernard travaille sur le projet 3
(4, 3),

-- Lucas Petit travaille sur les projets 1 et 3
(5, 1),
(5, 3);

-- ============================================
-- VÉRIFICATION DES DONNÉES INSÉRÉES
-- ============================================

-- Afficher le nombre d'enregistrements par table
SELECT 'Users' AS table_name, COUNT(*) AS count FROM users
UNION ALL
SELECT 'User Profiles', COUNT(*) FROM user_profiles
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'User-Project Associations', COUNT(*) FROM user_project;

-- ============================================
-- DONNÉES DE TEST - RÉSUMÉ
-- ============================================
/*

UTILISATEURS:
1. Jean Dupont (jean.dupont@example.com) - Développeur Full Stack
2. Marie Martin (marie.martin@example.com) - Chef de projet
3. Pierre Durand (pierre.durand@example.com) - Développeur Frontend
4. Sophie Bernard (sophie.bernard@example.com) - Data Scientist
5. Lucas Petit (lucas.petit@example.com) - DevOps Engineer

PROJETS:
1. API de gestion de projets (4 tâches)
   - Membres: Jean, Marie, Lucas
   
2. Application mobile e-commerce (3 tâches)
   - Membres: Jean, Marie, Pierre
   
3. Plateforme d'apprentissage en ligne (3 tâches)
   - Membres: Marie, Sophie, Lucas

STATUTS DES TÂCHES:
- DONE: 3 tâches
- IN_PROGRESS: 3 tâches
- TODO: 4 tâches

TESTS POSTMAN SUGGÉRÉS:
1. GET /users - Liste tous les utilisateurs
2. GET /users/1 - Récupérer Jean Dupont
3. GET /users/1/profile - Récupérer le profil de Jean
4. GET /projects - Liste tous les projets
5. GET /projects/1 - Récupérer le projet "API de gestion"
6. GET /tasks/1 - Récupérer une tâche spécifique
7. PUT /users/1 - Modifier un utilisateur
8. PUT /tasks/3 - Changer le statut d'une tâche
9. DELETE /users/5/profile - Supprimer un profil
10. POST /users - Créer un nouvel utilisateur

*/
