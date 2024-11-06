Projet Hair - Site E-commerce
Bienvenue sur le projet Hair ! Ce site e-commerce est dédié à la marque d'une artiste hairstylist, intégrant un portfolio captivant de ses réalisations. Le projet utilise une architecture microservices avec FastAPI pour le backend et React pour le frontend. Le projet inclut également des fonctionnalités de CRUD, de gestion des utilisateurs (utilisateur et administrateur), ainsi qu'une base de données MongoDB pour stocker les utilisateurs et les informations nécessaires à l'administration.

Description
Le projet implémente une plateforme e-commerce permettant de visualiser les services de coiffure proposés, de consulter un portfolio des réalisations, de gérer les commandes et les utilisateurs. Le backend est construit avec FastAPI, tandis que le frontend est développé avec React. Le système de gestion des utilisateurs et de l'administration est implémenté via des rôles (utilisateur et administrateur). Les actions CRUD sont accessibles à l'administrateur pour gérer les services de coiffure et les commandes. Les utilisateurs peuvent se connecter via JWT pour accéder à leurs informations et effectuer des achats. Le paiement est géré via Stripe.

Fonctionnalités
Backend (FastAPI) :

Gestion des utilisateurs (connexion, inscription, et gestion des rôles).
API RESTful pour créer, lire, mettre à jour et supprimer des services.
Gestion des commandes et des paiements via Stripe.
JWT pour sécuriser les routes et l'accès aux fonctionnalités des utilisateurs.
Gestion des rôles utilisateurs : utilisateurs standard et administrateurs.
Intégration de MongoDB pour stocker les informations des utilisateurs et des services.
Frontend (React) :

Interface utilisateur réactive et conviviale.
Pages pour la visualisation des services, du portfolio et des commandes.
Interface d'administration accessible uniquement aux administrateurs pour gérer les services et les commandes (CRUD).
Gestion du panier et intégration du paiement via Stripe.
CRUD (Create, Read, Update, Delete) :

CRUD pour gérer les services de coiffure et les commandes depuis l'interface d'administration.
Base de données MongoDB :

MongoDB est utilisé pour stocker les utilisateurs et gérer les rôles (admin et utilisateur).
MySQL est utilisé pour les données des commandes.
Environnement virtuel :

Utilisation d'un environnement virtuel Python pour gérer les dépendances.
Tests unitaires avec pytest :

Tests pour valider les fonctionnalités principales du backend.
CI/CD avec GitHub Actions :

Automatisation du déploiement du projet avec chaque mise à jour du code source.
Docker :

Utilisation de Docker pour containeriser les services backend et frontend, afin d'assurer une exécution cohérente dans différents environnements.
Schéma de l'architecture
scss
Copier le code
+---------------------+        +-----------------------+
| Frontend (React)    | <----> | Backend (FastAPI)     |
|                     |        |                       |
| - Interface UI      |        | - API Restful         |
| - Panier d'achat    |        | - Gestion des services|
| - Authentification  |        | - Gestion des commandes|
|                     |        | - Stripe Payment      |
+---------------------+        | - JWT Authentication  |
                               +-----------------------+
                                         |
                                         v
                             +---------------------+
                             | MongoDB             |
                             | (Users, Roles)      |
                             +---------------------+
                                         |
                                         v
                             +------------------------------+
                             | MySQL Database               |
                             | (Orders,Category,Products)   |
                             +------------------------------+
Technologies utilisées
Backend :

FastAPI : Framework pour la création rapide d'API RESTful en Python.
SQLAlchemy : ORM pour interagir avec la base de données MySQL.
MongoDB : Base de données NoSQL pour stocker les informations des utilisateurs et gérer les rôles.
JWT : Pour l'authentification sécurisée des utilisateurs.
Stripe : Pour gérer les paiements en ligne.
Frontend :

React : Pour construire l'interface utilisateur dynamique et réactive.
Axios : Pour effectuer des requêtes HTTP vers l'API FastAPI.
Tests :

pytest : Pour effectuer des tests unitaires et d'intégration.
CI/CD :

GitHub Actions : Pour automatiser les tests, le déploiement et la gestion du projet.
Docker :

Conteneurisation des services pour assurer une exécution cohérente dans tous les environnements.
Gestion des Utilisateurs et Rôles
Le projet gère deux types d'utilisateurs : les utilisateurs standard et les administrateurs. Voici les fonctionnalités liées à la gestion des utilisateurs et des rôles :

Authentification :
Les utilisateurs peuvent se connecter via JWT.
Un utilisateur standard peut consulter les services et passer une commande.
Un administrateur peut gérer les services et les commandes via une interface d'administration dédiée.
CRUD pour les services (Admin seulement) :
Create : Ajouter un nouveau service de coiffure.
Read : Afficher la liste des services existants.
Update : Modifier un service existant.
Delete : Supprimer un service de la base de données.

CI/CD avec GitHub Actions
Le projet est configuré pour déployer automatiquement les modifications via GitHub Actions. Chaque push dans la branche main déclenche un workflow pour :

Exécuter les tests unitaires.
Construire les containers Docker.
Déployer l'application.
