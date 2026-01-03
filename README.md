# Projet Développement Web IV : Gestion des Feedbacks de Recrutement

## Objectif du projet

Ce projet a pour but de lier un ERP (**Odoo**) à un portail web externe (**Django**) afin de gérer les retours d'entretiens d'embauche.

## Auteurs

* Noje Alessian
* Opre Nicoleta

---

# 🚀 Instructions de Lancement

Pour tester le projet, veuillez suivre ces deux étapes **dans l'ordre** :

## 1. Lancer le serveur Odoo (Docker)

Le backend **Odoo** et la base de données **PostgreSQL** sont conteneurisés.

À la racine du projet (où se trouve le fichier `docker-compose.yml`), exécutez :

```bash
docker-compose up
```

Attendez quelques instants que le serveur Odoo soit totalement opérationnel (accessible via le port **8069**).

---

## 2. Lancer l'application Django

Ouvrez un nouveau terminal à la racine du projet (au même niveau que le fichier `manage.py`) et exécutez la commande suivante :

```bash
python manage.py runserver
```

*(ou `py manage.py runserver` selon votre configuration Windows)*

---

# 🔗 Accès et Identifiants (Demo Data)

Une fois les serveurs lancés, vous pouvez accéder aux interfaces suivantes :

## 🔹 Odoo – Interface Recruteur

* **URL** : [http://localhost:8069](http://localhost:8069)
* **Email** : `admin`
* **Mot de passe** : `admin`

Le module **"Feedback"** est déjà installé et les données de démonstration sont chargées.

---

## 🔹 Django – Interface Candidat

* **URL Portail** : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **URL Admin** : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Superuser

* **Login** : `admin`
* **Password** : `admin`

---

# 📝 Note Technique

La base de données **SQLite** (`db.sqlite3`) a été laissée intentionnellement dans le dépôt Git afin de fournir des données de démonstration prêtes à l'emploi et de faciliter la correction sans nécessiter de configuration initiale complexe.
