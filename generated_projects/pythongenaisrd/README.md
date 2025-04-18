Here is a production-grade README.md for the FastAPI project:

**pythongenaisrd**
=====================

**Project Summary**
-----------------

pythongenaisrd is a FastAPI project that provides a robust and scalable API for managing leaves, pods, and user authentication. The project is built using FastAPI, PostgreSQL (with SQLAlchemy), Alembic, Pydantic, and Pytest.

**Setup & Installation**
------------------------

### Prerequisites

* Python 3.9+
* PostgreSQL 13+
* pip

### Installation

1. Clone the repository: `git clone https://github.com/your-username/pythongenaisrd.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a PostgreSQL database and update the `DATABASE_URL` environment variable in `.env` file
4. Run Alembic migrations: `alembic upgrade head`

**How to Run the Server**
-------------------------

1. Run the server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Open your web browser and navigate to `http://localhost:8000`

**API Documentation**
---------------------

API documentation is available at:

* Swagger: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

**Environment Variables**
-------------------------

Create a `.env` file with the following variables:

* `DATABASE_URL`: PostgreSQL database connection URL
* `SECRET_KEY`: Secret key for JSON Web Tokens (JWT)

**Modular Code and Generated Services/Schemas**
---------------------------------------------

This project uses modular code and generated services/schemas using Pydantic. The `app` directory is organized into the following subdirectories:

* `models`: Database models using SQLAlchemy
* `services`: Business logic services
* `db`: Database interactions using SQLAlchemy
* `schemas`: Pydantic models for API requests and responses
* `api`: API endpoints using FastAPI
* `routes`: API routes and endpoint definitions

**Testing**
----------

This project uses Pytest for unit testing. Run tests using: `pytest`

**License**
---------

This project is licensed under the MIT License. See `LICENSE` for details.

**Contributing**
--------------

Contributions are welcome! Please open a pull request to contribute to the project.

**Acknowledgments**
------------------

This project was generated using FastAPI and is maintained by [Your Name].