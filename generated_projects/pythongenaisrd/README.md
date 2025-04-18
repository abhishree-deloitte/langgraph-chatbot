Here is the production-grade README.md for the FastAPI project:

**pythongenaisrd**
=====================

**Project Summary**
---------------------

pythongenaisrd is a FastAPI project that provides a robust and scalable API for managing dashboard data, leave management, project-oriented development, and authentication and authorization. The project is built using FastAPI, PostgreSQL (with SQLAlchemy), Alembic, Pydantic, and Pytest.

**Setup & Installation**
-------------------------

### Prerequisites

* Python 3.9+
* PostgreSQL 13+
* pip

### Installation

1. Clone the repository: `git clone https://github.com/your-username/pythongenaisrd.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a PostgreSQL database and update the `DATABASE_URL` environment variable in `.env` file.
4. Run Alembic migrations: `alembic upgrade head`

**How to Run the Server**
-------------------------

1. Run the server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Open a web browser and navigate to `http://localhost:8000`

**API Documentation**
-------------------

API documentation is available at:

* Swagger: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

**Environment Variables**
-------------------------

Create a `.env` file in the project root with the following variables:

* `DATABASE_URL`: PostgreSQL database connection URL (e.g., `postgresql://user:password@localhost/dbname`)
* `SECRET_KEY`: Secret key for JWT authentication (e.g., `secret_key_here`)

**Modular Code and Generated Services/Schemas**
---------------------------------------------

The project follows a modular code structure, with separate folders for API routes, database models, services, and schemas. Pydantic is used to generate schemas for API responses and requests.

**Testing**
----------

The project uses Pytest for unit testing. Run tests using `pytest`.

**Directory Structure**
---------------------

* `.pytest_cache/`: Pytest cache directory
* `alembic/`: Alembic migration directory
* `app/`: Application code directory
	+ `api/`: API routes directory
	+ `database/`: Database models directory
	+ `models/`: Database models directory
	+ `routers/`: API routers directory
	+ `schemas/`: Pydantic schemas directory
	+ `services/`: Business logic services directory
* `tests/`: Unit tests directory

**License**
----------

This project is licensed under the MIT License. See `LICENSE` for details.