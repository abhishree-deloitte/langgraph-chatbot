# node 8

import os
import shutil
import subprocess
import time
import requests
from pathlib import Path
from app.utils.colors import GREEN, CYAN, YELLOW, RESET
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def zip_and_document_node(state: dict):
    project_path = Path(state["project_path"])
    project_name = state["project_name"]
    zip_output_path = Path("generated_projects") / f"{project_name}.zip"

    print(f"\n{YELLOW}📦 Documenting and Zipping project: {CYAN}{project_path}{RESET}")

    srs = state.get("srs_analysis", "No SRS analysis found.")
    structure = "\n".join([str(p.relative_to(project_path)) for p in project_path.rglob("*") if p.is_dir()])
    readme_prompt = f"""
You are a backend engineer assistant.
Generate a production-grade README.md for a FastAPI project.

Project Details:
- Project Name: {project_name}
- Project Structure:
{structure}
- SRS Summary:
{srs}
- Tech Stack: FastAPI, PostgreSQL (SQLAlchemy), Alembic, Pydantic, Pytest

Include:
- Project summary
- Setup & installation
- How to run the server
- API docs URL (swagger, redoc)
- .env instructions if needed
- Mention use of modular code and generated services/schemas

Output the entire README.md content — do not skip anything.
    """

    model = ChatOpenAI(
        model="llama3-70b-8192",
        temperature=0.3,
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
    )

    response = model([
        SystemMessage(content="You are a documentation expert."),
        HumanMessage(content=readme_prompt)
    ])
    lm_calls = state.get("llm_calls", 0) + 1

    readme_path = project_path / "README.md"
    readme_path.write_text(response.content.strip())
    print(f"{GREEN}  ✓ README.md generated using LLM{RESET}")

    if zip_output_path.exists():
        zip_output_path.unlink()

    shutil.make_archive(str(zip_output_path).replace(".zip", ""), 'zip', root_dir=project_path)
    print(f"{GREEN}✅ Zipped to: {CYAN}{zip_output_path}{RESET}\n")

    return {
        **state,
        "zip_path": str(zip_output_path),
        "readme_path": str(readme_path),
        "llm_calls": lm_calls,
    }
