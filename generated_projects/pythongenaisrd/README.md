Here is the production-grade README.md for the FastAPI project:

**pythongenaisrd**
=====================

**Project Summary**
-------------------

pythongenaisrd is a FastAPI project that provides a robust and scalable backend API for managing leave requests, pods, and user authentication. The project is designed to follow best practices for modular code organization, using Pydantic for data modeling and Alembic for database migrations.

**Setup and Installation**
-------------------------

### Prerequisites

* Python 3.9+
* PostgreSQL 13+
* pip

### Install dependencies

```
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

* `DATABASE_URL`: PostgreSQL connection URL (e.g., `postgresql://user:password@localhost/dbname`)
* `SECRET_KEY`: Secret key for JSON Web Tokens (JWT)

### Database Setup

Run the following command to create the database schema:
```
alembic upgrade head
```

**How to Run the Server**
-------------------------

### Development Mode

```
uvicorn app.api:app --reload
```

### Production Mode

```
gunicorn -w 4 app.api:app
```

**API Documentation**
-------------------

### Swagger

http://localhost:8000/docs

### Redoc

http://localhost:8000/redoc

**Modular Code Organization**
-----------------------------

The project is organized into the following modules:

* `app`: Main application module
* `app/models`: Data models using Pydantic
* `app/services`: Business logic services
* `app/routers`: API routers
* `app/schemas`: API schema definitions
* `app/crud`: CRUD operations for models
* `app/routes`: API route definitions
* `app/api`: API endpoint implementations
* `app/api/endpoints`: API endpoint definitions

**Generated Services and Schemas**
-----------------------------------

The project uses Pydantic to generate services and schemas automatically. This ensures consistency and reduces boilerplate code.

**Testing**
----------

The project uses Pytest for unit testing. Run the following command to execute tests:
```
pytest
```

**Tech Stack**
-------------

* FastAPI
* PostgreSQL (SQLAlchemy)
* Alembic
* Pydantic
* Pytest

**License**
---------

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.