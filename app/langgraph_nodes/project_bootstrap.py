# Node 2

import os
from pathlib import Path

FOLDER_STRUCTURE = [
    "app",
    "app/api/routes",
    "app/models",
    "app/services",
    "tests"
]

ESSENTIAL_FILES = {
    "app/main.py": "# Entry point for FastAPI app\n\nfrom fastapi import FastAPI\n\napp = FastAPI()\n",
    "app/database.py": "# DB connection setup placeholder\n",
    "requirements.txt": "\n".join([
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "alembic",
        "python-dotenv",
        "pytest",
    ]),
    ".env": "# Add your environment variables here\n",
    "README.md": "# Auto-generated FastAPI project\n\nGenerated using LangGraph-powered AI system.",
    ".gitignore": ".env\n__pycache__/\n.venv/\n",
    "Dockerfile": "\n".join([
        "FROM python:3.12-slim",
        "WORKDIR /app",
        "COPY . .",
        "RUN pip install --no-cache-dir -r requirements.txt",
        'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]',
    ]),
}

def bootstrap_project_node(state: dict):
    """
    LangGraph node to create FastAPI folder structure inside project-specific folder
    """
    project_name = state["project_name"]
    root_path = Path("generated_projects") / project_name
    root_path.mkdir(parents=True, exist_ok=True)

    for folder in FOLDER_STRUCTURE:
        path = root_path / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created folder: {path}")

    for file_rel_path, content in ESSENTIAL_FILES.items():
        file_path = root_path / file_rel_path
        with open(file_path, "w") as f:
            f.write(content)
        print(f"  ✓ Created file: {file_path}")

    return {
        **state,
        "project_path": str(root_path),
        "bootstrap_success": True
    }

