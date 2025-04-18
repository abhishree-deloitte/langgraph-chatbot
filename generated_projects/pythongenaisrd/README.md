Here is the production-grade README.md for the FastAPI project:

**pythongenaisrd**
=====================

**Project Summary**
pythongenaisrd is a FastAPI project that provides a comprehensive platform for leave management, pod management, and dashboard features. The project is built using FastAPI, PostgreSQL (SQLAlchemy), Alembic, Pydantic, and Pytest.

**Setup & Installation**
-------------------------

### Prerequisites

* Python 3.9+
* PostgreSQL 13+
* pip

### Install dependencies

Run the following command to install the required dependencies:
```
pip install -r requirements.txt
```
### Environment Variables

Create a `.env` file in the root directory with the following variables:
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_NAME=your_database
SECRET_KEY=your_secret_key
```
Replace the placeholders with your actual database credentials and secret key.

**How to Run the Server**
-------------------------

### Development Mode

Run the following command to start the development server:
```
uvicorn app.main:app --reload
```
### Production Mode

Run the following command to start the production server:
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```
**API Documentation**
---------------------

### Swagger

Access the API documentation using Swagger at:
```
http://localhost:8000/api/docs
```
### Redoc

Access the API documentation using Redoc at:
```
http://localhost:8000/api/redoc
```
**Modular Code Structure**
-------------------------

The project follows a modular code structure, with separate directories for models, services, schemas, and API routes. This allows for easy maintenance and extension of the application.

**Generated Services and Schemas**
---------------------------------

The project uses Pydantic to generate services and schemas based on the database schema. This ensures consistency and reduces boilerplate code.

**Testing**
----------

The project uses Pytest for unit testing and integration testing. Run the following command to execute the tests:
```
pytest
```
**Database Migrations**
-----------------------

The project uses Alembic for database migrations. Run the following command to apply migrations:
```
alembic upgrade head
```
**License**
---------

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

**Contributing**
--------------

Contributions are welcome! Please open a pull request to contribute to the project.

**Acknowledgments**
----------------

This project was built using the following technologies:

* FastAPI
* PostgreSQL (SQLAlchemy)
* Alembic
* Pydantic
* Pytest

Special thanks to the maintainers of these projects for their hard work and dedication.