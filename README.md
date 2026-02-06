# Web Development Project IV: Recruitment Feedback Management

## Project Objective

The purpose of this project is to connect an ERP (**Odoo**) to an external web portal (**Django**) in order to manage recruitment interview feedback.

## Authors

* Noje Alessian
* Opre Nicoleta

---

# Startup Instructions

To test the project, please follow these 4 steps **in order**:

## 1. Install the required libraries

```bash
pip install -r requirements.txt
```

## 2. Start the Odoo server (Docker)

The **Odoo** backend and the **PostgreSQL** database are containerized.

From the root of the project (where the `docker-compose.yml` file is located), run:

```bash
docker-compose up
```

Wait a few moments until the Odoo server is fully operational (accessible via port **8069**).

---

## 3. Start the Django application

Open a new terminal at the root of the project (at the same level as the `manage.py` file) and run the following command:

```bash
python manage.py runserver
```

*(or `py manage.py runserver` depending on your Windows configuration)*

---

## 4. Configure the Odoo connection

Once Django is running, you need to tell it where to find Odoo so that communication works properly:

1. Go to this specific URL: [http://127.0.0.1:8000/admin/odoo_config/odooconfig/](http://127.0.0.1:8000/admin/odoo_config/odooconfig/)
2. Log in with the Django superuser (see credentials below).
3. Add a new configuration ("Add odoo config" button) by entering the Odoo parameters below (URL, DB, User, Password).

---

# Access and Credentials (Demo Data)

Once the servers are running, you can access the following interfaces:

## 🔹 Odoo – Recruiter Interface

* **URL** : [http://localhost:8069](http://localhost:8069)
* **Email** : `admin`
* **Password** : `admin`
* **DB Name** : `demo_db`
  The **"Feedback"** module is already installed and demo data is loaded.

---

## 🔹 Django – Candidate Interface

* **Portal URL** : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Admin URL** : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Superuser

* **Login** : `admin`
* **Password** : `admin`

---

# Technical Note

The **SQLite** database (`db.sqlite3`) has been intentionally left in the Git repository in order to provide ready-to-use demo data and to facilitate grading without requiring complex initial configuration.
