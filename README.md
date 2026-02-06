# Web Development Project IV: Recruitment Feedback Management

## Project Overview

This project demonstrates the integration of an **Odoo ERP module** with a **Django web application**. The goal is to structure and manage recruitment interview feedback: recruiters use Odoo to create and evaluate feedback, while candidates can consult their interview feedback through a Django portal. Communication between Django and Odoo is handled via **XML-RPC**.

The project showcases Odoo module development (models, views, security, demo data, and decorators such as `@api.depends`, `@api.onchange`, and `@api.constrains`) as well as Django–Odoo integration.

## Authors

* Noje Alessian
* Opre Nicoleta

---

## Startup Instructions

To test the project, please follow these steps **in order**:

### 1. Install required libraries

```bash
pip install -r requirements.txt
```

### 2. Start the Odoo server (Docker)

The **Odoo** backend and the **PostgreSQL** database are containerized.

From the root of the project (where the `docker-compose.yml` file is located), run:

```bash
docker-compose up
```

Wait until the Odoo server is fully operational (available on port **8069**).

---

### 3. Start the Django application

Open a new terminal at the root of the project (same level as `manage.py`) and run:

```bash
python manage.py runserver
```

*(or `py manage.py runserver` depending on your Windows configuration)*

---

### 4. Configure the Odoo connection

Once Django is running, configure the Odoo connection so communication can work:

1. Go to: [http://127.0.0.1:8000/admin/odoo_config/odooconfig/](http://127.0.0.1:8000/admin/odoo_config/odooconfig/)
2. Log in using the Django superuser credentials.
3. Add a new configuration ("Add odoo config") and fill in the Odoo parameters (URL, database, user, password).

---

## Access and Credentials (Demo Data)

### 🔹 Odoo – Recruiter Interface

* **URL**: [http://localhost:8069](http://localhost:8069)
* **Login**: `admin`
* **Password**: `admin`
* **Database name**: `demo_db`

The **Feedback** module is already installed and demo data is loaded.

---

### 🔹 Django – Candidate Interface

* **Portal URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Admin URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

**Superuser credentials**:

* **Login**: `admin`
* **Password**: `admin`

---

## Technical Note

The **SQLite** database (`db.sqlite3`) is intentionally included in the Git repository to provide ready-to-use demo data and simplify setup and grading.
