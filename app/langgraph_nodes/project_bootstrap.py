# node 2

from pathlib import Path
from app.utils.colors import GREEN, CYAN, YELLOW, RESET

FOLDER_STRUCTURE = [
    "app",
    "app/api/routes",
    "app/models",
    "app/services",
    "tests"
]

ESSENTIAL_FILES = {
    "main.py": "# Entry point for FastAPI app\n\nfrom fastapi import FastAPI\n\napp = FastAPI()\n",
    "database.py": "# DB connection setup placeholder\n",
}

ROOT_FILES = {
    "requirements.txt": "\n".join([
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "alembic",
        "python-dotenv",
        "pytest",
        "asyncpg"
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
    print(f"\n{YELLOW}🛠️  Bootstrapping project for: {CYAN}{state['project_name']}{RESET}")

    project_name = state["project_name"]
    root_path = Path("generated_projects") / project_name
    root_path.mkdir(parents=True, exist_ok=True)

    # ✅ Create folders
    for folder in FOLDER_STRUCTURE:
        folder_path = root_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"{GREEN}  ✓ Created folder: {CYAN}{folder_path}{RESET}")

    # ✅ Create app files (inside app/)
    for file_name, content in ESSENTIAL_FILES.items():
        file_path = root_path / "app" / file_name
        with open(file_path, "w") as f:
            f.write(content)
        print(f"{GREEN}  ✓ Created app file: {CYAN}{file_path}{RESET}")

    # ✅ Create root-level files
    for file_name, content in ROOT_FILES.items():
        file_path = root_path / file_name
        with open(file_path, "w") as f:
            f.write(content)
        print(f"{GREEN}  ✓ Created root file: {CYAN}{file_path}{RESET}")

    print(f"\n{YELLOW}✅ Project bootstrap complete. Path: {CYAN}{root_path}{RESET}\n")

    return {
        **state,
        "project_path": str(root_path),
        "bootstrap_success": True
    }
